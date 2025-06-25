#! /usr/bin/env python3

import signal
import sys

from time import sleep


def shutdown(signal, frame):
    print('INFO: Shutting down...')
    sys.exit(0)

if __name__ == '__main__':
    counter = 0
    signal.signal(signal.SIGINT, shutdown)

    while True:
        print(f'INFO: loop iteration {counter}')
        counter += 1
        sleep(1)


