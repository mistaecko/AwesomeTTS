# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
import os,sqlite3

conffile = os.path.join(os.path.dirname(os.path.realpath(__file__)), "conf.db")
 
conn = sqlite3.connect(conffile, isolation_level=None)
conn.row_factory = sqlite3.Row

cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='general'")

tblexit = cursor.fetchall()


if len (tblexit) < 1:
	cursor.execute("CREATE TABLE general (automaticQuestions numeric, automaticAnswers numeric, file_howto_name numeric, file_max_length numeric, file_extension text, subprocessing numeric, TTS_KEY_Q numeric, TTS_KEY_A numeric)")
	cursor.execute("INSERT INTO general VALUES (0, 0, 1, 100, 'mp3', 1, ?, ?)", (Qt.Key_F3, Qt.Key_F4))

cursor.execute("SELECT * FROM general")

r = cursor.fetchone()


# Key to get the [TTS::] tags in the Question field pronounced
TTS_KEY_Q=r['TTS_KEY_Q']

# Key to get the [TTS::] tags in the Answer field pronounced
TTS_KEY_A=r['TTS_KEY_A']


automaticQuestions = r['automaticQuestions']
automaticAnswers = r['automaticAnswers']
quote_mp3 = r['file_howto_name']
subprocessing = r['subprocessing']
file_max_length = r['file_max_length']
file_extension = r['file_extension']

def saveConfig(config):
	cursor.execute("UPDATE general SET automaticQuestions=?, automaticAnswers=?, file_howto_name=?, file_max_length=?, file_extension=?, subprocessing=?, TTS_KEY_Q=?, TTS_KEY_A=? ", (config.automaticQuestions, config.automaticAnswers, config.quote_mp3, config.file_max_length, config.file_extension, config.subprocessing, config.TTS_KEY_Q, config.TTS_KEY_A))


TTS_service = {}
