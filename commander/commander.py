#!/usr/bin/python3
import asyncio
import signal
import sys
import os
import ipc.commanderserver
import ipc.kspconn


def my_interrupt_handler():
    print('Stopping')
    for task in asyncio.Task.all_tasks():
        task.cancel()
    loop.stop()

class Commander:
    def __init__(self):
        self.commanderserver = ipc.commanderserver.CommanderServer(
        '/tmp/commander.socket', self)
        self.kspconnection = ipc.kspconn.KSPConnection(commander=self)

    def start(self):
        self.commanderserver.start()
        self.kspconnection.start()

    def stop(self):
        self.commanderserver.stop()
        self.kspconnection.stop()

    def handle_data_from_coordinator(self, message):
        self.kspconnection.handle_data_from_coordinator(message)

    def send_data_to_coordinator(self, message):
        self.commanderserver.send_data_to_coordinator(message)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, my_interrupt_handler)
    loop.add_signal_handler(signal.SIGHUP, my_interrupt_handler)

    commander = Commander()
    commander.start()

    try:
        loop.run_forever()
    except asyncio.CancelledError:
        print('Tasks has been canceled')
    finally:
        commander.stop()
        loop.close()
