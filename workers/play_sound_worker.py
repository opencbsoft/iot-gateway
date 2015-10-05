"""
    Play a sound file 0.1
    It should play the file that is stored in the pool store data

    FIELDS
    file = file_name
    left = True/False (optional)
    right = True/False (optional)

"""

from subprocess import call
import os

from generic_worker import *

'''
    REQUIEREMENTS
    - amixer and an audio card (for left/right balancing)
    - mpg123 for playing sound files
'''


# local settings
POOL_NAME = 'play_sound'
DEFAULT_SOUND_VOLUME = 80


def on_message(client, user_data, msg):
    data = json.loads(msg.payload)
    if data.get('file'):
        if os.path.isfile(STORAGE_ROOT+'/'+POOL_NAME+'/'+data.get('file')):
            if data.get('left', False):
                call(['amixer', "-q", 'sset', 'Speaker', '0%,{0}%'.format(DEFAULT_SOUND_VOLUME)])
            elif data.get('right', False):
                call(['amixer', "-q", 'sset', 'Speaker', '{0}%,0%'.format(DEFAULT_SOUND_VOLUME)])
            call(["mpg123", "-q", STORAGE_ROOT+'/'+POOL_NAME+'/'+data.get('file')])
            call(['amixer', "-q", 'sset', 'Speaker', '{0}%,{0}%'.format(DEFAULT_SOUND_VOLUME)])


#create a daemon and run the worker
main_app(__name__, POOL_NAME, on_message)