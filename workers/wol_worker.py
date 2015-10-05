#!/usr/bin/env python3
"""
    Wake on Lan 0.1
    It should receive the mac of the network device to wake up

    FIELDS
    mac = ff.ff.ff.ff.ff.ff
"""

from subprocess import call
import os
from wakeonlan import wol

from generic_worker import *

'''
    REQUIEREMENTS
    wakeonlan https://github.com/remcohaszing/pywakeonlan
'''


# local settings
POOL_NAME = 'wake_on_lan'


def on_message(client, user_data, msg):
    data = json.loads(msg.payload)
    if 'mac' in data:
        wol.send_magic_packet(data['mac'])


#create a daemon and run the worker
main_app(__name__, POOL_NAME, on_message)