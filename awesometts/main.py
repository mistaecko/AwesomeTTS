# -*- coding: utf-8 -*-
# Author:  Arthur Helfstein Fragoso
# Email: arthur[at]life.net.br
#
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
#   AwesomeTTS plugin for Anki 2.0
version = '1.0 Beta 3'
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
#   Any problems, comments, please email me: arthur[at]life.net.br 
#
#
#  Edited on 2012-10-16
#  
########################### Settings #######################################
from PyQt4.QtCore import *


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


def ATTS_Factedit_button(self):
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
		self.addMedia(filename)

def ATTS_Fact_edit_setupFields(self):
	AwesomeTTS = QPushButton(self.widget)
	AwesomeTTS.setFixedHeight(20)
	AwesomeTTS.setFixedWidth(20)
	AwesomeTTS.setCheckable(True)
	AwesomeTTS.connect(AwesomeTTS, SIGNAL("clicked()"), lambda self=self: ATTS_Factedit_button(self))
	AwesomeTTS.setIcon(QIcon(":/icons/speaker.png"))
	AwesomeTTS.setToolTip(_("AwesomeTTS :: MP3 File Generator"))
	AwesomeTTS.setShortcut(_("Ctrl+g"))
	AwesomeTTS.setFocusPolicy(Qt.NoFocus)
	#AwesomeTTS.setEnabled(False)
	self.iconsBox.addWidget(AwesomeTTS)
	AwesomeTTS.setStyle(self.plastiqueStyle)


addHook("setupEditorButtons", ATTS_Fact_edit_setupFields)


############################ MP3 Mass Generator

srcField = -1
dstField = -1


#take a break, so we don't fall in Google's blacklist. Code contributed by Dusan Arsenijevic
def take_a_break(ndone, ntotal):      
	t = 500;
	while True:
		mw.progress.update(label="Generated %s of %s, \n sleeping for %s seconds...." % (ndone+1, ntotal, t))
		time.sleep(1)
		t = t-1
		if t==0: break

def generate_audio_files(factIds, frm, service, srcField_name, dstField_name):
	returnval = {'fieldname_error': 0}
	nelements = len(factIds)
	batch = 900
	
	for c, id in enumerate(factIds):
		if service == 'g' and (c+1)%batch == 0: # GoogleTTS has to take a break once in a while
			take_a_break(c, nelements)
		note = mw.col.getNote(id)
		
		if not (srcField_name in note.keys() and dstField_name in note.keys()):
			returnval['fieldname_error'] += 1
			continue
		
		mw.progress.update(label="Generating MP3 files...\n%s of %s\n%s" % (c+1, nelements,note[srcField_name]))
		
		filename = TTS_service[service]['record'](frm, note[srcField_name])
		
		if frm.radioOverwrite.isChecked():
			if frm.checkBoxSndTag.isChecked():
				note[dstField_name] = '[sound:'+ filename +']'
			else:
				note[dstField_name] = filename
		else:
			note[dstField_name] += ' [sound:'+ filename +']'
		note.flush()
		
	return returnval


def onGenerate(self):
	global TTS_language, dstField, srcField
	sf = self.selectedNotes()
	if not sf:
		utils.showInfo("Select the notes and then use the MP3 Mass Generator")
		return
	import anki.find
	fields = sorted(anki.find.fieldNames(self.col, downcase=False))
	d = QDialog(self)
	frm = forms.massgenerator.Ui_Dialog()
	frm.setupUi(d)
	d.setWindowModality(Qt.WindowModal)
	
	frm.label_version.setText("Version "+ version)
	
	fieldlist = []
	for f in mw.col.models.all():
		for a in f['flds']:
			fieldlist.append(a['name'])
	
	frm.sourceFieldComboBox.addItems(fieldlist)
	frm.sourceFieldComboBox.setCurrentIndex(srcField)

	frm.destinationFieldComboBox.addItems(fieldlist)
	frm.destinationFieldComboBox.setCurrentIndex(dstField)

	#service list start
	serv_list = [TTS_service[service]['name'] for service in TTS_service]
	frm.comboBoxService.addItems(serv_list)
	
	for service in TTS_service:
		tostack = QWidget(frm.stackedWidget)
		tostack.setLayout(TTS_service[service]['filegenerator_layout'](frm))
		frm.stackedWidget.addWidget(tostack)
	
	QtCore.QObject.connect(frm.comboBoxService, QtCore.SIGNAL("currentIndexChanged(QString)"), lambda selected,frm=frm,serv_list=serv_list: filegenerator_onCBoxChange(selected, frm, serv_list))
	#service list end
	
	
	if not d.exec_():
		return

	srcField = frm.sourceFieldComboBox.currentIndex()
	dstField = frm.destinationFieldComboBox.currentIndex()
	#languageField = frm.languageComboBox.currentIndex()

	if srcField == -1 or dstField == -1 :
		return
	
	service = getService_byName(serv_list[frm.comboBoxService.currentIndex()])

	self.mw.checkpoint(_("AwesomeTTS MP3 Mass Generator"))
	self.mw.progress.start(immediate=True, label="Generating MP3 files...")
	
	self.model.beginReset()

	result = generate_audio_files(sf, frm, service, fieldlist[srcField], fieldlist[dstField])

	self.model.endReset()
	self.mw.progress.finish()
	nupdated = len(sf) - result['fieldname_error']
	utils.showInfo((ngettext(
		"%s note updated",
		"%s notes updated", nupdated) % (nupdated))+  
		
		((ngettext(
		"\n%s fieldname error. A note doesn't have the Source Field '%s' or the Destination Field '%s'",
		"\n%s fieldname error. Those notes don't have the Source Field '%s' or the Destination Field '%s'", result['fieldname_error'])
		% (result['fieldname_error'], fieldlist[srcField], fieldlist[dstField])) if result['fieldname_error'] > 0 else "")
		)


def setupMenu(editor):
	a = QAction("AwesomeTTS MP3 Mass Generator", editor)
	editor.form.menuEdit.addAction(a)
	editor.connect(a, SIGNAL("triggered()"), lambda e=editor: onGenerate(e))

addHook("browser.setupMenus", setupMenu)

######################################### Keys and AutoRead

## Check pressed key
def newKeyHandler(self, evt):
	pkey = evt.key()
	if (self.state == 'answer' or self.state == 'question'):
		if (pkey == config.TTS_KEY_Q):
			playTTSFromText(self.card.q())  #read the TTS tags
		elif (self.state=='answer' and pkey == config.TTS_KEY_A):
			playTTSFromText(self.card.a()) #read the TTS tags
	evt.accept()



def ATTSautoread(toread, automatic):
	if not sound.hasSound(toread):
		if automatic:
			playTTSFromText(toread)

def ATTS_OnQuestion(self):
	ATTSautoread(self.card.q(), config.automaticQuestions)

def ATTS_OnAnswer(self):
	ATTSautoread(self.card.a(), config.automaticAnswers)



Reviewer._keyHandler = wrap(Reviewer._keyHandler, newKeyHandler, "before")
Reviewer._showQuestion = wrap(Reviewer._showQuestion, ATTS_OnQuestion, "after")
Reviewer._showAnswer  = wrap(Reviewer._showAnswer, ATTS_OnAnswer, "after")
        
