#!/usr/bin/env python3
"""
    POST ON IFTT.com
    It should post the event on iftt.com

    FIELDS
    event =
    value1 =
    value2 =
    value3 =
"""

from subprocess import call
import os
import json
import requests

from generic_worker import *
from iftt_settings import *

# local settings
POOL_NAME = 'iftt_post'


def on_message(client, user_data, msg):
    data = json.loads(msg.payload)
    payload = dict()
    if data.get('value1'):
        payload['value1'] = data.get('value1')
    if data.get('value2'):
        payload['value2'] = data.get('value2')
    if data.get('value3'):
        payload['value3'] = data.get('value3')
    requests.post("https://maker.ifttt.com/trigger/{0}/with/key/{1}".format(data.get('event'), IFTT_KEY), data=payload)


#create a daemon and run the worker
main_app(__name__, POOL_NAME, on_message)