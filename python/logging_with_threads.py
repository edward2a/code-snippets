#! /usr/bin/env python3

import logging
import time

from threading import Thread

format = '%(asctime)s.%(msecs)03dZ %(levelname)s: (%(threadName)s) %(message)s'
date_format = '%Y-%m-%dT%H:%M:%S'
logging.Formatter.converter = time.gmtime
logging.basicConfig(level=logging.DEBUG, format=format, datefmt=date_format)
log = logging.getLogger()

class HelloWorld(Thread):
    def run(self, **kwargs):
        log.debug('Hello, World! I AM A THREAD!.')

def hw():
    log.warning('I am a function.')


log.info('Test message.')
hw()
t = HelloWorld()
t.start()
t.join()

