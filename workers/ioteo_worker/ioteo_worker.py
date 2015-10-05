"""
    IOTEO Cameras 0.1
    It should receive the status it wants to be applied to the cameras defined in ioteo_settings

    FIELDS
    action = power-on
    action = power-off
"""
import json
import requests
import logging

from ..generic_worker.generic_worker import IotWorker
from .ioteo_settings import *

'''
    REQUIEREMENTS

'''


# local settings
POOL_NAME = 'ioteo'
API_URL = "https://api.ioteo.net/main"
logging.getLogger("requests").setLevel(logging.CRITICAL)


def on_message(client, user_data, msg):
    data = json.loads(msg.payload)
    action = data.get('action', 'power-on')
    if action == 'power-on':
        action = False
    else:
        action = True
    auth_request = requests.get('{0}/login'.format(API_URL), params={'username': USERNAME, 'password': PASSWORD}, verify=False).json()
    if auth_request['success']:
        for camera_id in CAMERA_LIST:
            requests.get('{0}/set-configuration'.format(API_URL), params={'key': auth_request['key'], 'cam_id': camera_id, 'privacy': action}, verify=False).json()

worker = IotWorker(POOL_NAME, on_message)
