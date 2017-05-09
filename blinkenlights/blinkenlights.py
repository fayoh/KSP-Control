#!/usr/bin/python3

import asyncio
import signal
import os
import sys
import ipc.blinkenlightsserver
import blink.blinkgenerator
import blinkenio.controller
import common.devices


class Blinkenlights:
    def __init__(self):
        self.blinkenlightsserver = ipc.blinkenlightsserver.BlinkenlightsServer(
            '/tmp/blinkenlights.socket', self)
        self.blinkgenerator = blink.blinkgenerator.BlinkGenerator()
        self.iocontroller = blinkenio.controller.Controller()

    def start(self):
        self.blinkenlightsserver.start()
        self.blinkgenerator.start()
        self.iocontroller.start()

    def stop(self):
        self.blinkenlightsserver.stop()
        self.blinkgenerator.stop()
        self.iocontroller.stop()

    def handle_data_from_coordinator(self, message):
        pass

    def send_data_to_coordinator(self, message):
        pass

def my_interrupt_handler():
    print('Stopping')
    for task in asyncio.Task.all_tasks():
        task.cancel()
    loop.stop()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, my_interrupt_handler)
    loop.add_signal_handler(signal.SIGHUP, my_interrupt_handler)

    blinkenlights = Blinkenlights()
    blinkenlights.start()

    try:
        loop.run_forever()
    except asyncio.CancelledError:
        print('Tasks has been canceled')
    finally:
        blinkenlights.stop()
        loop.close()
