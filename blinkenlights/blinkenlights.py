#!/usr/bin/python3

import asyncio
import signal
import os
import sys
import configparser
import logging
import blink.blinkgenerator
import blinkenio.controller
import common.devices
import common.protocol as protocol
from common.coordinatorclient import CoordinatorClient

class Blinkenlights:
    def __init__(self, config):
        # TODO: Implement base class Service, setting type and event
        self.type = 'blinkenlights'
        self.config = config
        self.connectionevent = asyncio.Event()
        self.coordinatorclient = CoordinatorClient(
            config['SocketPath'], self)
        self.blinkgenerator = blink.blinkgenerator.BlinkGenerator(
            float(config.get('BlinkHz', 2)))
        self.iocontroller = blinkenio.controller.Controller()
        self.logger = logging.getLogger(self.get_name())

    def get_name(self):
        return self.__class__.__name__

    def start(self):
        self.logger.info("Starting")
        self.coordinatorclient.start()
        self.blinkgenerator.start()
        self.iocontroller.start()

    def stop(self):
        self.logger.info("Shutting down")
        self.send_data_to_coordinator(
            protocol.create_message(protocol.MessageType.STATUS_MSG,
                                    protocol.Status.SHUTDOWN))
        self.coordinatorclient.stop()
        self.blinkgenerator.stop()
        self.iocontroller.stop()

    def handle_data_from_coordinator(self, message):
        pass

    def send_data_to_coordinator(self, message):
        # Maybe we should let the exception propagate and get handled higher up?
        try:
            self.coordinatorclient.send_data_to_coordinator(message)
        except protocol.NoConnectionError:
            self.logger.debug("Failed to send data, no connection")

    def handle_connect(self):
        self.send_status()

    def send_status(self):
        if self.blinkgenerator.ok and self.iocontroller.ok:
            self.send_data_to_coordinator(
                protocol.create_message(protocol.MessageType.STATUS_MSG,
                                        protocol.Status.OK))
        else:
            self.send_data_to_coordinator(
                protocol.create_message(protocol.MessageType.STATUS_MSG,
                                        protocol.Status.DEGRADED))

    def handle_disconnect(self):
        pass

def my_interrupt_handler():
    for task in asyncio.Task.all_tasks():
        task.cancel()
    loop.stop()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, my_interrupt_handler)
    loop.add_signal_handler(signal.SIGHUP, my_interrupt_handler)

    # TODO: Get level from args
    logging.basicConfig(level=logging.DEBUG)

    config = configparser.ConfigParser()
    config.read('common/config.ini')

    blinkenlights = Blinkenlights(config['blinkenlights'])
    blinkenlights.start()

    try:
        loop.run_forever()
    except asyncio.CancelledError:
        pass
    finally:
        blinkenlights.stop()
        loop.close()
