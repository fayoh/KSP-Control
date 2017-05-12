#!/usr/bin/python3

import asyncio
import signal
import sys
import os
import configparser
import logging
import common.protocol as protocol
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
        self.logger = logging.getLogger(self.get_name())

    def start(self):
        self.logger.info('Coordinator starting')
        self.coordinatorserver.start()

    def stop(self):
        self.logger.info('Shutting down')
        self.coordinatorserver.broadcast(
            protocol.create_message(protocol.MessageType.STATUS_MSG,
                                    protocol.Status.SHUTDOWN))
        self.coordinatorserver.stop()

    def handle_data_from_blinkenlights(self, message):
        message_type = protocol.get_message_type(message)
        message_data = protocol.get_message_data(message)
        if message_type == protocol.MessageType.STATUS_MSG:
            self.logger.debug("Blinkenlights entered state %s",
                              message_data.name)

    def handle_data_from_commander(self, message):
        message_type = protocol.get_message_type(message)
        message_data = protocol.get_message_data(message)
        if message_type == protocol.MessageType.STATUS_MSG:
            self.logger.debug("Commander entered state %s",
                              message_data.name)
    def get_name(self):
        return self.__class__.__name__


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, my_interrupt_handler)
    loop.add_signal_handler(signal.SIGHUP, my_interrupt_handler)

    logging.basicConfig(level=logging.DEBUG)

    config = configparser.ConfigParser()
    config.read('common/config.ini')

    coordinator = Coordinator(config['coordinator'])
    coordinator.start()

    try:
        loop.run_forever()
    except asyncio.CancelledError:
        pass
    finally:
        coordinator.stop()
        loop.close()
