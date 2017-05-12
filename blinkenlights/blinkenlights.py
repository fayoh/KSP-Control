#!/usr/bin/python3

import asyncio
import configparser
import logging
import blink.blinkgenerator
import blinkenio.controller
import common.protocol as protocol
from common.service import AbstractService
from common.coordinatorclient import CoordinatorClient

class Blinkenlights(AbstractService):
    def __init__(self, config):
        self.blinkgenerator = blink.blinkgenerator.BlinkGenerator(
            float(config.get('BlinkHz', 2)))
        self.iocontroller = blinkenio.controller.Controller()
        super(Blinkenlights, self).__init__(config)

    def start(self):
        asyncio.async(self.blinkgenerator.start())
        self.iocontroller.start()

    def stop(self):
        self.blinkgenerator.stop()
        self.iocontroller.stop()

    def handle_data_from_coordinator(self, message):
        pass

    def send_status(self):
        if self.blinkgenerator.ok and self.iocontroller.ok:
            self.send_data_to_coordinator(
                protocol.create_message(protocol.MessageType.STATUS_MSG,
                                        protocol.Status.OK))
        else:
            self.send_data_to_coordinator(
                protocol.create_message(protocol.MessageType.STATUS_MSG,
                                        protocol.Status.DEGRADED))

    def handle_connect(self):
        pass

    def handle_disconnect(self):
        pass

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('common/config.ini')

    blinkenlights = Blinkenlights(config['blinkenlights'])

