#!/usr/bin/env python3
"""
    Text to speech from google 0.1
    It should speak the text that you send to it

    FIELDS
    message = the text to be spoken
    left = True/False (optional)
    right = True/False (optional)

"""

import json
from subprocess import call

from generic_worker import *

'''
    REQUIEREMENTS
    - amixer and an audio card (for left/right balancing)
    - mpg123 for playing sound files
'''


# local settings
POOL_NAME = 'speak'
DEFAULT_SOUND_VOLUME = 80


def on_message(client, user_data, msg):
    print(msg.payload)
    data = json.loads(msg.payload)
    if data.get('left', False):
        call(['amixer', "-q", 'sset', 'PCM', '0%,{0}%'.format(DEFAULT_SOUND_VOLUME)])
    elif data.get('right', False):
        call(['amixer', "-q", 'sset', 'PCM', '{0}%,0%'.format(DEFAULT_SOUND_VOLUME)])
    call(["mpg123", "-q", "http://translate.google.com/translate_tts?tl=%s&q=%s&ie=%s&total=1&idx=0&client=t" % ("en", data.get('message', 'No message was set'), "UTF-8")])
    call(['amixer', "-q", 'sset', 'PCM', '{0}%,{0}%'.format(DEFAULT_SOUND_VOLUME)])

#create a daemon and run the worker
worker = IotWorker(POOL_NAME, on_message)

