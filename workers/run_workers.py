#!/usr/bin/env python3
from subprocess import call
import sys

from settings import *

for item in ACTIVE_WORKERS:
    print('Starting '+item+' worker...')
    call([sys.executable, item+'_worker.py', 'start'])
