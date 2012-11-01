# -*- coding: utf-8 -*-

from PyQt4 import QtGui,QtCore
import os, re, subprocess, sys
from anki.utils import stripHTML
from urllib import quote_plus
import awesometts.config as config
import awesometts.util as util
from subprocess import Popen, PIPE, STDOUT


if subprocess.mswindows:
	vbs_launcher = os.path.join(os.environ['SYSTEMROOT'], "syswow64", "cscript.exe")
	if not os.path.exists(vbs_launcher) :
		vbs_launcher = os.path.join(os.environ['SYSTEMROOT'], "system32", "cscript.exe")
	sapi5_path = os.path.join(os.path.dirname(__file__),"sapi5.vbs")
	

	exec_command = subprocess.Popen([vbs_launcher, sapi5_path, '-vl'], startupinfo=util.si, stdout=subprocess.PIPE)
	voicelist = exec_command.stdout.read().split('\n')
	exec_command.wait()

	lasttoremove = 0
	for key, value in enumerate(voicelist):
		if '--Voice List--' in value:
			lasttoremove = key
			break
	for key in range(lasttoremove+1):
		voicelist.pop(0)
		
	def playsapi5TTS(text, voice):
		text = re.sub("\[sound:.*?\]", "", stripHTML(text.replace("\n", "")))
		param = [vbs_launcher, sapi5_path,'-hex', '-voice', util.dumpUnicodeStr(voice), util.dumpUnicodeStr(text)]
		if config.subprocessing:
			subprocess.Popen(param, startupinfo=util.si, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
		else:
			subprocess.Popen(param, startupinfo=util.si, stdin=PIPE, stdout=PIPE, stderr=STDOUT).communicate()

	def playfromtagsapi5TTS(fromtag):
		for item in fromtag:
			match = re.match("(.*?):(.*)", item, re.M|re.I)
			playsapi5TTS(match.group(2), match.group(1))

	def playfromHTMLtagsapi5TTS(fromtag):
		for item in fromtag:
			text = item.string
			voice = item['voice']
			playsapi5TTS(text, voice)

	def recordsapi5TTS(text, voice):
		text = re.sub("\[sound:.*?\]", "", stripHTML(text.replace("\n", "")))
		filename_wav = util.generateFileName(text.encode('utf-8'), 'sapi5', 'iso-8859-1', '.wav').decode('utf-8').encode(sys.getfilesystemencoding())
		filename_mp3 = util.generateFileName(text.encode('utf-8'), 'sapi5', 'iso-8859-1', '.mp3').decode('utf-8').encode(sys.getfilesystemencoding())
		subprocess.Popen([vbs_launcher, sapi5_path, '-hex', '-o', filename_wav, '-voice', util.dumpUnicodeStr(voice), util.dumpUnicodeStr(text)], startupinfo=util.si, stdin=PIPE, stdout=PIPE, stderr=STDOUT).wait()
		subprocess.Popen(['lame.exe', '--quiet', filename_wav, filename_mp3], startupinfo=util.si, stdin=PIPE, stdout=PIPE, stderr=STDOUT).wait()
		os.unlink(filename_wav)
		return filename_mp3.decode(sys.getfilesystemencoding())

	def filegenerator_layout(form):
		global DefaultSAPI5Voice
		verticalLayout = QtGui.QVBoxLayout()
		textEditlabel = QtGui.QLabel()
		textEditlabel.setText("Voice:")
		form.comboBoxsapi5 = QtGui.QComboBox()
		form.comboBoxsapi5.addItems([d for d in voicelist])
		form.comboBoxsapi5.setCurrentIndex(DefaultSAPI5Voice) # get Default

		verticalLayout.addWidget(textEditlabel)
		verticalLayout.addWidget(form.comboBoxsapi5)
		return verticalLayout
	
	def recordsapi5TTS_form(form, text):
		global DefaultSAPI5Voice
		DefaultSAPI5Voice = form.comboBoxsapi5.currentIndex() #set new Default
		return recordsapi5TTS(text, voicelist[form.comboBoxsapi5.currentIndex()])

	def filegenerator_run(form):
		global DefaultSAPI5Voice
		DefaultSAPI5Voice = form.comboBoxsapi5.currentIndex() #set new Default
		return recordsapi5TTS(unicode(form.texttoTTS.toPlainText()), voicelist[form.comboBoxsapi5.currentIndex()])

	def filegenerator_preview(form):
		return playsapi5TTS(unicode(form.texttoTTS.toPlainText()), voicelist[form.comboBoxsapi5.currentIndex()])

	DefaultSAPI5Voice = 0

	TTS_service = {'sapi5' : {
	'name': 'SAPI 5',
	'play' : playsapi5TTS,
	'playfromtag' : playfromtagsapi5TTS,
	'playfromHTMLtag' : playfromHTMLtagsapi5TTS,
	'record' : recordsapi5TTS_form,
	'filegenerator_layout': filegenerator_layout,
	'filegenerator_preview': filegenerator_preview,
	'filegenerator_run': filegenerator_run}}


