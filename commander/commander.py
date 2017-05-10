#!/usr/bin/python3
import asyncio
import signal
import sys
import os
import configparser
from common.coordinatorclient import CoordinatorClient
from kspconn.kspconn import KSPConnection


def my_interrupt_handler():
    print('Stopping')
    for task in asyncio.Task.all_tasks():
        task.cancel()
    loop.stop()

class Commander:
    def __init__(self, config):
        self.type = 'commander'
        self.config = config
        self.connectionevent = asyncio.Event()
        self.coordinatorclient = CoordinatorClient(
            config['SocketPath'], self)
        self.kspconnection = KSPConnection(config, commander=self)

    def start(self):
        self.coordinatorclient.start()
        self.kspconnection.start()

    def stop(self):
        self.coordinatorclient.stop()
        self.kspconnection.stop()

    def handle_data_from_coordinator(self, message):
        self.kspconnection.handle_data_from_coordinator(message)

    def send_data_to_coordinator(self, message):
        self.coordinatorclient.send_data_to_coordinator(message)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, my_interrupt_handler)
    loop.add_signal_handler(signal.SIGHUP, my_interrupt_handler)

    config = configparser.ConfigParser()
    config.read('common/config.ini')

    commander = Commander(config['commander'])
    commander.start()

    try:
        loop.run_forever()
    except asyncio.CancelledError:
        print('Tasks has been canceled')
    finally:
        commander.stop()
        loop.close()
