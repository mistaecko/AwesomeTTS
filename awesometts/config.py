# -*- coding: utf-8 -*-

from PyQt4.QtCore import *

# Key to get the [TTS::] tags in the Question field pronounced
TTS_KEY_Q=Qt.Key_F3

# Key to get the [TTS::] tags in the Answer field pronounced
TTS_KEY_A=Qt.Key_F4


#all the available keys are in http://doc.trolltech.com/qtjambi-4.4/html/com/trolltech/qt/core/Qt.Key.html


#sorry, the TTS won't recite it automatically when there is a sound file in the Question/Answer

# Option to automatically recite the Question field as it appears:
automaticQuestions = False        # disable the automatic recite
#automaticQuestions = True         # recite [TTS::] tags in the Questions as it appears


# Option to automatically recite the Answers field as it appears
automaticAnswers = False          # disable the automatic recite
#automaticAnswers = True           # recite [TTS::] tags in the Answers as it appears




# quote (encode) special characters for mp3 file names:
# Windows users should have their mp3 files quoted (True), if you want to try, the system encoding should be the same as the language you are learning. and in the Table slanguage, the right charset should be set there. (it may not work, do this only if you know what you are doing. If you want it really want it, install Linux! :D
# Unix users don't need to quote (encode) special characters. so you can set it as False if you want.
# it will work alright sync with AnkiMobile, but it won't work with AnkiWeb
quote_mp3 = True	# spC3A9cial.mp3 E381AFE38184.mp3 E4BDA0E5A5BD.mp3
#quote_mp3 = False  # spécial.mp3 はい.mp3　你好.mp3


#subprocessing is enabled by default
# on MS Windows XP or older or on Mac OSX, there is a bug of cutting the ending of a speech occasionally, so you may want to disable it.
#if it's disable(false), Anki will be frozen while GoogleTTS recites the speech. 
#subprocessing = False
subprocessing = True



TTS_service = {}
