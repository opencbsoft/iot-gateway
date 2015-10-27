#!/usr/bin/env python3
"""
    IOTEO Cameras 0.1
    It should receive the status it wants to be applied to the cameras defined in ioteo_settings

    FIELDS
    action = power-on
    action = power-off
"""

from subprocess import call
import os

from generic_worker import *


'''
    REQUIEREMENTS

'''


# local settings
POOL_NAME = 'lights'
CPP_EXE = 'send'



def on_message(client, user_data, msg):
    data = json.loads(msg.payload)
    action = data.get('action', 'power-on')
    id = data.get('id')
    if id:
        if action == 'power-on':
             call([CPP_EXE, '2', '1', id, '1'])
        else:
            call([CPP_EXE, '2', '1', id, '0'])
#create a daemon and run the worker
main_app(__name__, POOL_NAME, on_message)