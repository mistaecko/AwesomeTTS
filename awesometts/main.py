# -*- coding: utf-8 -*-
# Author:  Arthur Helfstein Fragoso
# Email: arthur@life.net.br
#
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
#   AwesomeTTS plugin for Anki 2.0
version = '1.0 Alpha 3'
#
#
#   To use the on the fly function, use the [TTS] or [ATTS] tag, you can still use the [GTTS] tag
#
#  [TTS:service_name:voice_or_language_code:text_to_tts]
# or
#  [ATTS:service_name:voice_or_language_code:text_to_tts]
#
# example: 
#
# Unix Espeak service:
#
#  [TTS:espeak:en:hello I'm a plugin]
#
# OSX Say service:
#
#  [TTS:say:Fred:hello I'm a plugin]
#
# GoogleTTS:
#
#  [TTS:g:en:hello I'm a plugin]
# or
#  [GTTS:en:hello I'm a plugin]
#
#
#  you can also generate the audio when editing a card.
#
# other functions will be added later.
#
#   Any problems, comments, please email me: arthur@life.net.br 
#
#
#  Edited on 2012-09-06
#  
########################### Settings #######################################
from PyQt4.QtCore import *
TTS_read_field = {}
TTS_tags_only, TTS_if_no_tag_read_whole = [1,2]


import awesometts.config as config

import os, subprocess, re, sys, urllib, imp
from aqt import mw, utils
from anki import sound
from anki.sound import playFromText
from anki.utils import stripHTML
from subprocess import Popen, PIPE, STDOUT
from urllib import quote_plus
from anki.hooks import wrap,addHook
from PyQt4 import QtGui,QtCore
from PyQt4.QtGui import *
from aqt.reviewer import Reviewer

import awesometts.forms as forms

TTS_service = {}

import awesometts.services


modules = {}
#modulespath = os.path.dirname(__file__)+"/services/"
modulespath = os.path.dirname(__file__)+"/services/"
modulesfiles = os.listdir(modulespath)
for i in range(len(modulesfiles)):
	name = modulesfiles[i].split('.')
	if len(name) > 1:
		if name[1] == 'py' and name[0] != '__init__':
			modules[name[0]] = imp.load_source(name[0], modulespath+name[0]+'.py')
			if hasattr(modules[name[0]], 'TTS_service'):
				TTS_service.update(modules[name[0]].TTS_service)
			else:
				del modules[name[0]]
		
#for path in glob.glob(os.path.dirname(__file__)+"/services/[!_]*.py"):
#	name, ext = os.path.splitext(os.path.basename(path))
#	modules[name] = imp.load_source(name, path)
#	TTS_service.update(modules[name].TTS_service)


print TTS_service


language_generator = config.TTS_language
file_max_length = 255 # Max filename length for Unix

# Prepend http proxy if one is being used.  Scans the environment for
# a variable named "http_proxy" for all operating systems
# proxy code contributted by Scott Otterson
proxies = urllib.getproxies()

if len(proxies)>0 and "http" in proxies:
	proxStr = re.sub("http:", "http_proxy:", proxies['http'])
	TTS_ADDRESS = proxStr + "/" + TTS_ADDRESS







######## utils
def get_language_id(language_code):
	x = 0
	for d in slanguages:
		if d[0]==language_code:
			return x
		x = x + 1


	

def playTTSFromText(text):
	tospeak = getTTSFromText(text)
	for service in tospeak:
		TTS_service[service]['playfromtag'](tospeak[service])

def getTTSFromText(text):
	tospeak = {}
	for match in re.findall("\[(G)TTS:(.*?)\]|\[A?TTS:(.*?):(.*?)\]", text, re.M|re.I):
		service = match[0].lower() if match[0] else match[2].lower()
		value = match[1] if match[0] else match[3]
		if not tospeak.has_key(service):
			tospeak.update({ service: [value] })
		else:
			tospeak[service].append(value)
	return tospeak


###########  TTS_read to recite the tts on-the-fly

def TTS_read(text, language=config.TTS_language):
	text = re.sub("\[sound:.*?\]", "", stripHTML(text.replace("\n", "")).encode('utf-8'))
	address = TTS_ADDRESS+'?tl='+language+'&q='+ quote_plus(text)
	if subprocess.mswindows:
		param = ['mplayer.exe', '-ao', 'win32', '-slave', '-user-agent', "'Mozilla/5.0'", address]
	else:
		param = ['mplayer', '-slave', '-user-agent', "'Mozilla/5.0'", address]
	if config.subprocessing:
		subprocess.Popen(param, startupinfo=si, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
	else:
		subprocess.Popen(param, startupinfo=si, stdin=PIPE, stdout=PIPE, stderr=STDOUT).communicate()



###################  TTS_record to generate MP3 files

def TTS_record(text, service, param=None):
	TTS_service[service]['record'](text, param)





############################ MP3 File Generator

def filegenerator_onCBoxChange(selected, form, serv_list):
	form.stackedWidget.setCurrentIndex(serv_list.index(selected))

def getService_byName(name):
	for service in TTS_service:
		if TTS_service[service]['name'] == name:
			return service


def GTTS_Factedit_button(self):
	global language_generator
	d = QDialog()
	form = forms.filegenerator.Ui_Dialog()
	form.setupUi(d)
	serv_list = [TTS_service[service]['name'] for service in TTS_service]
	form.comboBoxService.addItems(serv_list)

	for service in TTS_service:
		tostack = QWidget(form.stackedWidget)
		tostack.setLayout(TTS_service[service]['filegenerator_layout'](form))
		form.stackedWidget.addWidget(tostack)
	
	
	QtCore.QObject.connect(form.previewbutton, QtCore.SIGNAL("clicked()"), lambda form=form: TTS_service[getService_byName(serv_list[form.comboBoxService.currentIndex()])]['filegenerator_preview'](form))
	
	QtCore.QObject.connect(form.comboBoxService, QtCore.SIGNAL("currentIndexChanged(QString)"), lambda selected,form=form,serv_list=serv_list: filegenerator_onCBoxChange(selected, form, serv_list))


	if d.exec_():
		srv = getService_byName(serv_list[form.comboBoxService.currentIndex()])
		TTS_service[srv]['filegenerator_run'](form)
		filename = TTS_service[srv]['filegenerator_run'](form)
		print filename
		self.addMedia(filename)

def GTTS_Fact_edit_setupFields(self):
	AwesomeTTS = QPushButton(self.widget)
	AwesomeTTS.setFixedHeight(20)
	AwesomeTTS.setFixedWidth(20)
	AwesomeTTS.setCheckable(True)
	AwesomeTTS.connect(AwesomeTTS, SIGNAL("clicked()"), lambda self=self: GTTS_Factedit_button(self))
	AwesomeTTS.setIcon(QIcon(":/icons/speaker.png"))
	AwesomeTTS.setToolTip(_("AwesomeTTS :: MP3 File Generator"))
	AwesomeTTS.setShortcut(_("Ctrl+g"))
	AwesomeTTS.setFocusPolicy(Qt.NoFocus)
	#AwesomeTTS.setEnabled(False)
	self.iconsBox.addWidget(AwesomeTTS)
	AwesomeTTS.setStyle(self.plastiqueStyle)


addHook("setupEditorButtons", GTTS_Fact_edit_setupFields)





######################################### Keys and AutoRead

## Check pressed key
def newKeyHandler(self, evt):
	pkey = evt.key()
	if (self.state == 'answer' or self.state == 'question'):
		if (pkey == config.TTS_KEY_Q):
			playTTSFromText(self.card.q())  #read the GTTS tags
		elif (pkey == config.TTS_KEY_Q_ALL):
			if re.findall("\[(G)TTS:(.*?)\]|\[A?TTS:(.*?):(.*?)\]", self.card.q(), re.M|re.I):
				playTTSFromText(self.card.q()) #read the GTTS tags
			else:
				TTS_read(self.card.q(),config.TTS_language) #read the the whole field
		elif (self.state=='answer' and pkey == config.TTS_KEY_A):
			playTTSFromText(self.card.a()) #read the GTTS tags
		elif (self.state=='answer' and pkey == config.TTS_KEY_A_ALL):
			if re.findall("\[(G)TTS:(.*?)\]|\[A?TTS:(.*?):(.*?)\]", self.card.a(), re.M|re.I):
				playTTSFromText(self.card.a()) #read the GTTS tags
			else:
				TTS_read(self.card.a(),config.TTS_language)  #read the the whole field
		else:
			for key in TTS_read_field:
				if TTS_read_field[key] == pkey:
					TTS_read(self.card.note()[key],TTS_language)
					break
	evt.accept()



def GTTSautoread(toread, automatic):
	if not sound.hasSound(toread):
		if automatic == TTS_tags_only:
			playTTSFromText(toread)
		if automatic == TTS_if_no_tag_read_whole:
			if re.findall("\[(G)TTS:(.*?)\]|\[A?TTS:(.*?):(.*?)\]", toread, re.M|re.I):
				playTTSFromText(toread)
			else:
				TTS_read(toread,config.TTS_language)

def GTTS_OnQuestion(self):
	GTTSautoread(self.card.q(), config.automaticQuestions)

def GTTS_OnAnswer(self):
	GTTSautoread(self.card.a(), config.automaticAnswers)



Reviewer._keyHandler = wrap(Reviewer._keyHandler, newKeyHandler, "before")
Reviewer._showQuestion = wrap(Reviewer._showQuestion, GTTS_OnQuestion, "after")
Reviewer._showAnswer  = wrap(Reviewer._showAnswer, GTTS_OnAnswer, "after")
        
