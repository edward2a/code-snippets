#! /usr/bin/env python3

import argparse
import logging
import logging.handlers
import time

from multiprocessing import Process
from multiprocessing import Queue
from time import sleep

class QueueLogger(object):
    q_log = None

    def queue_logger(self):
        _format = '%(asctime)s.%(msecs)03dZ %(levelname)s: (%(processName)s) %(message)s'
        date_format = '%Y-%m-%dT%H:%M:%S'
        fmt = logging.Formatter(fmt=_format, datefmt=date_format)
        fmt.converter = time.gmtime

        handler = logging.handlers.QueueHandler(self.q_log)
        handler.setFormatter(fmt)
        log = logging.getLogger('root')
        log.addHandler(handler)
        log.setLevel(logging.INFO)
        return log

class DataWorker(Process, QueueLogger):
    def __init__(self, q_data, q_log):
        self.q_data = q_data
        self.q_log = q_log
        super().__init__()

    def run(self):
        log = self.queue_logger()
        log.info('Initializing process...')
        log.info('Done.')
        while True:
            log.info('Log message.')
            sleep(1)

class WebhookWorker(Process, QueueLogger):
    def __init__(self, q_data, q_log):
        self.q_data = q_data
        self.q_log = q_log
        super().__init__()

    def run(self):
        log = self.queue_logger()
        log.info('Initializing process...')
        log.info('Done.')
        while True:
            log.info('Log message.')
            sleep(10)

class EventWorker(Process, QueueLogger):
    def __init__(self, q_data, q_log):
        self.q_data = q_data
        self.q_log = q_log
        super().__init__()

    def run(self):
        log = self.queue_logger()
        log.info('Initializing process...')
        log.info('Done.')
        while True:
            log.info('Log message.')
            sleep(5)

def setup_logger(q):
    #_format = '%(asctime)s.%(msecs)03dZ %(levelname)s: (%(processName)s) %(message)s'
    #date_format = '%Y-%m-%dT%H:%M:%S'
    #fmt = logging.Formatter(fmt=_format, datefmt=date_format)
    #fmt.converter = time.gmtime

    handler = logging.StreamHandler()
    listener = logging.handlers.QueueListener(q, handler)
    #root = logging.getLogger()
    #root.addHandler(handler)
    #root.setLevel(logging.INFO)
    log_handler = logging.handlers.QueueHandler(q)
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)

    return (log, listener)

if __name__ == '__main__':
    q_data = Queue(-1)
    q_log = Queue(-1)
    log, log_listener = setup_logger(q_log)
    log_listener.start()
    log.info('Initializing...')

    w_data = DataWorker(q_data, q_log)
    w_webhook = WebhookWorker(q_data, q_log)
    w_event = EventWorker(q_data, q_log)
    log.info('Done.')

    w_data.start()
    w_webhook.start()
    w_event.start()

    sleep(300)
    w_data.terminate()
    w_webhook.terminate()
    w_event.terminate()
    w_data.close()
    w_webhook.close()
    w_event.close()
    log_listener.stop()


