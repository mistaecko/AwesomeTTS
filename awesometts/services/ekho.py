# -*- coding: utf-8 -*-

#import awesometts.config as config

from PyQt4 import QtGui,QtCore

#Supported Languages       
# code , Language
slanguages = [
['Cantonese', 'Chinese Cantonese'],
['Hakka', 'Chinese Hakka'],
['Mandarin', 'Chinese Mandarin'],
['Hangul', 'Korean']
]


import re, subprocess
from anki.utils import stripHTML
from urllib import quote_plus
import awesometts.config as config
import awesometts.util as util
from subprocess import Popen, PIPE, STDOUT
from random import randint, seed



def playEkhoTTS(text, language):
	text = re.sub("\[sound:.*?\]", "", stripHTML(text.replace("\n", "")).encode('utf-8'))
	subprocess.Popen(['ekho', '-v', language, text], stdin=PIPE, stdout=PIPE, stderr=STDOUT).communicate()

def playfromtagEkhoTTS(fromtag):
	for item in fromtag:
		match = re.match("(.*?):(.*)", item, re.M|re.I)
		playEkhoTTS(match.group(2), match.group(1))

def playfromHTMLtagEkhoTTS(fromtag):
	for item in fromtag:
		text = text = ''.join(item.findAll(text=True))
		voice = item['voice']
		playEkhoTTS(text, voice)

def get_language_id(language_code):
	x = 0
	for d in slanguages:
		if d[0]==language_code:
			return x
		x = x + 1


def recordEkhoTTS(text, language):
	text = re.sub("\[sound:.*?\]", "", stripHTML(text.replace("\n", "")).encode('utf-8'))
	filename = util.generateFileName(text, 'ekho', 'iso-8859-1', '.wav')
	subprocess.Popen(['ekho', '-v', language, '-t', 'wav', '-o', filename, text], stdin=PIPE, stdout=PIPE, stderr=STDOUT).communicate()
	return filename.decode('utf-8')

def filegenerator_layout(form):
	global DefaultEkhoVoice
	verticalLayout = QtGui.QVBoxLayout()
	textEditlabel = QtGui.QLabel()
	textEditlabel.setText("Language:")
	form.comboBoxEkho = QtGui.QComboBox()
	form.comboBoxEkho.addItems([d[1] for d in slanguages])
	form.comboBoxEkho.setCurrentIndex(DefaultEkhoVoice) # get Default

	verticalLayout.addWidget(textEditlabel)
	verticalLayout.addWidget(form.comboBoxEkho)
	return verticalLayout

def recordEkhoTTS_form(form, text):
	global DefaultEkhoVoice
	DefaultEkhoVoice = form.comboBoxEkho.currentIndex() #set new Default
	return recordEkhoTTS(text, slanguages[form.comboBoxEkho.currentIndex()][0])

def filegenerator_run(form):
	global DefaultEkhoVoice
	DefaultEkhoVoice = form.comboBoxEkho.currentIndex() #set new Default
	return recordEkhoTTS(unicode(form.texttoTTS.toPlainText()), slanguages[form.comboBoxEkho.currentIndex()][0])

def filegenerator_preview(form):
	return playEkhoTTS(unicode(form.texttoTTS.toPlainText()), slanguages[form.comboBoxEkho.currentIndex()][0])


DefaultEkhoVoice = get_language_id('Mandarin')


if not subprocess.mswindows:
	TTS_service = {'ekho' : {
	'name': 'Ekho',
	'play' : playEkhoTTS,
	'playfromtag' : playfromtagEkhoTTS,
	'playfromHTMLtag' : playfromHTMLtagEkhoTTS,
	'record' : recordEkhoTTS_form,
	'filegenerator_layout': filegenerator_layout,
	'filegenerator_preview': filegenerator_preview,
	'filegenerator_run': filegenerator_run}}
