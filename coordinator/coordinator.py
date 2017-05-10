#!/usr/bin/python3

import asyncio
import signal
import sys
import os
import configparser
import logging
import ipc.coordinatorserver
import common.devices


def my_interrupt_handler():
    for task in asyncio.Task.all_tasks():
        task.cancel()
    loop.stop()


class Coordinator:
    def __init__(self, config):
        self.config = config
        self.coordinatorserver = ipc.coordinatorserver.CoordinatorServer(
            config['SocketPath'], self)

    def start(self):
        self.coordinatorserver.start()

    def stop(self):
        self.coordinatorserver.stop()

    def handle_data_from_blinkenlights(self, message):
        pass

    def handle_data_from_commander(self, message):
        pass

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, my_interrupt_handler)
    loop.add_signal_handler(signal.SIGHUP, my_interrupt_handler)

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info('Coordinator starting')

    config = configparser.ConfigParser()
    config.read('common/config.ini')

    coordinator = Coordinator(config['coordinator'])
    coordinator.start()

    try:
        loop.run_forever()
    except asyncio.CancelledError:
        logger.info('Tasks has been canceled')
    finally:
        logger.info('Shutting down')
        coordinator.stop()
        loop.close()
