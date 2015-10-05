import paho.mqtt.client as mqtt
from paho.mqtt import publish
import json
import configparser
import os

from settings import *

"""Generic linux daemon base class for python 3.x."""

import sys, os, time, atexit, signal


class Daemon:
    """A generic daemon class.
    Usage: subclass the daemon class and override the run() method.
    """

    def __init__(self, pidfile):
        self.pidfile = pidfile

    def daemonize(self):
        """Deamonize class. UNIX double fork mechanism."""

        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('fork #1 failed: {0}\n'.format(err))
            sys.exit(1)

        # decouple from parent environment
        os.chdir('/')
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('fork #2 failed: {0}\n'.format(err))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')

        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)

        pid = str(os.getpid())
        with open(self.pidfile, 'w+') as f:
            f.write(pid + '\n')

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """Start the daemon."""

        # Check for a pidfile to see if the daemon already runs
        try:
            with open(self.pidfile, 'r') as pf:

                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if pid:
            message = "pidfile {0} already exist. " + \
                      "Daemon already running?\n"
            sys.stderr.write(message.format(self.pidfile))
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """Stop the daemon."""

        # Get the pid from the pidfile
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if not pid:
            message = "pidfile {0} does not exist. " + \
                      "Daemon not running?\n"
            sys.stderr.write(message.format(self.pidfile))
            return  # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            e = str(err.args)
            if e.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print(str(err.args))
                sys.exit(1)

    def restart(self):
        """Restart the daemon."""
        self.stop()
        self.start()

    def run(self):
        """You should override this method when you subclass Daemon.

		It will be called after the process has been daemonized by
		start() or restart()."""


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
    if os.path.isfile(STORAGE_ROOT + '/' + pool_name + '/storage.ini'):
        config.read(STORAGE_ROOT + '/' + pool_name + '/storage.ini')
    else:
        config['DEFAULT']['pool_name'] = pool_name
        with open(STORAGE_ROOT + '/' + pool_name + '/storage.ini', 'w') as configfile:
            config.write(configfile)
    return config['DEFAULT']


def save_config(pool_name, data):
    config = configparser.ConfigParser()
    config['DEFAULT'] = data
    with open(STORAGE_ROOT + '/' + pool_name + '/storage.ini', 'w') as configfile:
        config.write(configfile)
