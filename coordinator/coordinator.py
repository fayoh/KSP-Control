#!/usr/bin/python3

import asyncio
import signal
import sys
import os
import ipc.commanderclient
import ipc.blinkenlightsclient
import common.devices


def my_interrupt_handler():
    print('Stopping')
    for task in asyncio.Task.all_tasks():
        task.cancel()
    loop.stop()  # only necessary when we run run_forever


class Coordinator:
    def __init__(self):
        commandersocket = '/tmp/commander.socket'
        blinkenlightssocket = '/tmp/blinkenlights.socket'
        self.blinkenlightsclient = ipc.blinkenlightsclient.BlinkenlightsClient(
            blinkenlightssocket, self)
        self.commanderclient = ipc.commanderclient.CommanderClient(
            commandersocket, self)

    def start(self):
        self.blinkenlightsclient.start()
        self.commanderclient.start()

    def stop(self):
        self.blinkenlightsclient.stop()
        self.commanderclient.stop()

    def handle_data_from_blinkenlights(self, message):
        pass

    def handle_data_from_commander(self, message):
        pass

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, my_interrupt_handler)
    loop.add_signal_handler(signal.SIGHUP, my_interrupt_handler)

    coordinator = Coordinator()
    coordinator.start()

    try:
        loop.run_forever()
    except asyncio.CancelledError:
        print('Tasks has been canceled')
    finally:
        coordinator.stop()
        loop.close()
