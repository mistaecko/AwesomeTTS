# -*- coding: utf-8 -*-

import os, sys, re, subprocess
from anki.utils import stripHTML
from urllib import quote_plus
import awesometts.config as config

file_max_length = 255 # Max filename length for Unix

def generateFileName(text, service, winencode='iso-8859-1', extention=".mp3"):
	if config.quote_mp3: #re.sub removes \/:*?"<>|[]. from the file name
		file = quote_plus(re.sub('[\\\/\:\*\?"<>|\[\]\.]*', "",text)).replace("%", "")+extention
		if len(file) > file_max_length:
			file = file[0:file_max_length-len(extention)] + extention
	else:
		file = re.sub('[\\\/\:\*\?"<>|\[\]\.]*', "",text)+ extention
		if len(file) > file_max_length:
			file = file[0:file_max_length-len(extention)] + extention
		if subprocess.mswindows:
			file = file.decode('utf-8').encode(slanguages[get_language_id(language)][2])
	return file

# mplayer for MS Windows
if subprocess.mswindows:
	file_max_length = 100 #guess of a filename max length for Windows (filename +path = 255)
	dir = os.path.dirname(os.path.abspath(sys.argv[0]))
	os.environ['PATH'] += ";" + dir
	si = subprocess.STARTUPINFO()
	try:
		si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
	except:
		# python2.7+
		si.dwFlags |= subprocess._subprocess.STARTF_USESHOWWINDOW
else:
	si = None #for plataforms other than MS Windows
	
def dumpUnicodeStr(src):
	return ''.join(["%04X" % ord(x) for x in src])
