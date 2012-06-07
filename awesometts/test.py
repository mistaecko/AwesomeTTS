import re


import os
import glob

import config


for f in glob.glob(os.path.dirname(__file__)+"/services/*.py"):
	__import__("services." + os.path.basename(f)[:-3])




def playTTSFromText(text):
	tospeak = getTTSFromText(text)
	for service in tospeak:
		config.TTS_service[service]['play'](tospeak[service])

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




playTTSFromText("[gtts:aaaa]  [GTTS:bbbb] [ATTS:say:ccc] [TTS:say:wwww]")




