import paho.mqtt.client as mqtt
from paho.mqtt import publish
import json
import configparser
import os

from .settings import *


class IotWorker(object):

    def __init__(self, pool_name, on_message):
        self.client = mqtt.Client()
        self.client.connect(QUEUE_HOSTNAME, QUEUE_PORT, 60)
        self.pool_name = pool_name
        self.client.on_connect = self.on_connect
        self.client.on_message = on_message
        self.client.loop_forever()

    def on_connect(self, client, user_data, flags, rc):
        self.client.subscribe(self.pool_name)


def iot_publish(topic, data):
    publish.single(topic, json.dumps(data), hostname=QUEUE_HOSTNAME, port=QUEUE_PORT)


def load_config(pool_name):
    config = configparser.ConfigParser()
    if os.path.isfile(STORAGE_ROOT+'/'+pool_name+'/storage.ini'):
        config.read(STORAGE_ROOT+'/'+pool_name+'/storage.ini')
    else:
        config['DEFAULT']['pool_name'] = pool_name
        with open(STORAGE_ROOT+'/'+pool_name+'/storage.ini', 'w') as configfile:
            config.write(configfile)
    return config['DEFAULT']


def save_config(pool_name, data):
    config = configparser.ConfigParser()
    config['DEFAULT'] = data
    with open(STORAGE_ROOT+'/'+pool_name+'/storage.ini', 'w') as configfile:
        config.write(configfile)
