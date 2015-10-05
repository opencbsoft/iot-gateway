"""
    IOTEO Cameras 0.1
    It should receive the status it wants to be applied to the cameras defined in ioteo_settings

    FIELDS
    action = power-on
    action = power-off
"""
import sys
import time

import json
import requests
import logging

from generic_worker import IotWorker, Daemon
from ioteo_settings import *

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


class IotDaemon(Daemon):
        def run(self):
            # Or simply merge your code with MyDaemon.
            worker = IotWorker(POOL_NAME, on_message)

if __name__ == "__main__":
        daemon = IotDaemon('/tmp/daemon-iot.pid')
        if len(sys.argv) == 2:
            if 'start' == sys.argv[1]:
                daemon.start()
            elif 'stop' == sys.argv[1]:
                daemon.stop()
            elif 'restart' == sys.argv[1]:
                daemon.restart()
            else:
                print ("Unknown command")
                sys.exit(2)
            sys.exit(0)
        else:
            print ("usage: %s start|stop|restart" % sys.argv[0])
            sys.exit(2)