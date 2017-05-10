#!/usr/bin/python3

import asyncio
import signal
import sys
import os
import ipc.coordinatorserver
import common.devices


def my_interrupt_handler():
    print('Stopping')
    for task in asyncio.Task.all_tasks():
        task.cancel()
    loop.stop()  # only necessary when we run run_forever


class Coordinator:
    def __init__(self):
        # TODO: implement config parser
        socketpath = '/tmp/coordinator.socket'
        self.coordinatorserver = ipc.coordinatorserver.CoordinatorServer(
            socketpath, self)

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

    coordinator = Coordinator()
    coordinator.start()

    try:
        loop.run_forever()
    except asyncio.CancelledError:
        print('Tasks has been canceled')
    finally:
        coordinator.stop()
        loop.close()
