# -*- coding: utf-8 -*-

'''voicelist = [
"--Female--",
"Agnes", 
"Kathy",
"Princess",
"Vicki",
"Victoria",
"Voices",

"",
"--Male--",
"Bruce",
"Fred",
"Junior",
"Ralph",

"",
"--Novelty--",
"Albert",
"Bad News", 
"Bahh",
"Bells",
"Boing",
"Bubbles",
"Cellos",
"Deranged",
"Good News",
"Hysterical",
"Pipe Organ",
"Trinoids",
"Whisper",
"Zarvox"] '''


from PyQt4 import QtGui,QtCore
import os, re, subprocess
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
		text = re.sub("\[sound:.*?\]", "", stripHTML(text.replace("\n", "")).encode('utf-8'))
		subprocess.Popen([vbs_launcher, sapi5_path, '-voice', voice, text], startupinfo=util.si, stdin=PIPE, stdout=PIPE, stderr=STDOUT).communicate()

	def playfromtagsapi5TTS(fromtag):
		print fromtag
		for item in fromtag:
			match = re.match("(.*?):(.*)", item, re.M|re.I)
			playsapi5TTS(match.group(2), match.group(1))

	def recordsapi5TTS(text, voice):
		text = re.sub("\[sound:.*?\]", "", stripHTML(text.replace("\n", "")).encode('utf-8'))
		filename_wav = util.generateFileName(text, 'sapi5', 'iso-8859-1', '.wav')
		filename_mp3 = util.generateFileName(text, 'sapi5', 'iso-8859-1', '.mp3')
		subprocess.Popen([vbs_launcher, sapi5_path, '-o', filename_wav, '-voice', voice, text], startupinfo=util.si, stdin=PIPE, stdout=PIPE, stderr=STDOUT).wait()
		subprocess.Popen(['lame.exe', '--quiet', filename_wav, filename_mp3], startupinfo=util.si, stdin=PIPE, stdout=PIPE, stderr=STDOUT).wait()
		os.unlink(filename_wav)
		return filename_mp3.decode('utf-8')

	def filegenerator_layout(form):
		verticalLayout = QtGui.QVBoxLayout()
		textEditlabel = QtGui.QLabel()
		textEditlabel.setText("Voice:")
		form.comboBoxsapi5 = QtGui.QComboBox()
		form.comboBoxsapi5.addItems([d for d in voicelist])

		verticalLayout.addWidget(textEditlabel)
		verticalLayout.addWidget(form.comboBoxsapi5)
		return verticalLayout

	def filegenerator_run(form):
		return recordsapi5TTS(unicode(form.texttoTTS.toPlainText()), voicelist[form.comboBoxsapi5.currentIndex()])

	def filegenerator_preview(form):
		return playsapi5TTS(unicode(form.texttoTTS.toPlainText()), voicelist[form.comboBoxsapi5.currentIndex()])

	TTS_service = {'sapi5' : {
	'name': 'SAPI 5',
	'play' : playsapi5TTS,
        'playfromtag' : playfromtagsapi5TTS,
	'record' : recordsapi5TTS,
	'filegenerator_layout': filegenerator_layout,
	'filegenerator_preview': filegenerator_preview,
	'filegenerator_run': filegenerator_run}}


