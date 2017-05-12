#!/usr/bin/python3
import asyncio
import signal
import sys
import os
import configparser
import logging
import common.protocol as protocol
from common.coordinatorclient import CoordinatorClient
from kspconn.kspconn import KSPConnection


def my_interrupt_handler():
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
        self.logger = logging.getLogger(self.get_name())

    def start(self):
        self.logger.info("Starting")
        self.coordinatorclient.start()
        self.kspconnection.start()

    def stop(self):
        self.logger.info("Shutting down")

        try:
            self.send_data_to_coordinator(
                protocol.create_message(protocol.MessageType.STATUS_MSG,
                                        protocol.Status.SHUTDOWN))
        except protocol.NoConnectionError:
            pass

        self.coordinatorclient.stop()
        self.kspconnection.stop()

    def handle_data_from_coordinator(self, message):
        self.kspconnection.handle_data_from_coordinator(message)

    def send_data_to_coordinator(self, message):
        try:
            self.coordinatorclient.send_data_to_coordinator(message)
        except protocol.NoConnectionError:
            self.logger.debug("Failed to send data, no connection")

    def handle_connect(self):
        self.send_status()
        # TODO: why does this not reach the coordinator on reconnect?
        #    Make minimum viable example and test
        # message = protocol.create_message(
        #     protocol.MessageType.KRPC_INFO_MSG,
        #     (protocol.KrpcInfo.GAME_SCENE,
        #      self.kspconnection.get_scene()))
        # self.send_data_to_coordinator(message)

    def send_status(self):
        self.logger.debug("send status")
        if self.kspconnection.ok:
            self.send_data_to_coordinator(
                protocol.create_message(protocol.MessageType.STATUS_MSG,
                                        protocol.Status.OK))
        else:
            self.send_data_to_coordinator(
                protocol.create_message(protocol.MessageType.STATUS_MSG,
                                        protocol.Status.DEGRADED))

    def handle_disconnect(self):
        self.kspconnection.handle_disconnect()

    def get_name(self):
        return self.__class__.__name__


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, my_interrupt_handler)
    loop.add_signal_handler(signal.SIGHUP, my_interrupt_handler)

    # TODO: Get level from args
    logging.basicConfig(level=logging.DEBUG)


    config = configparser.ConfigParser()
    config.read('common/config.ini')
    commander = Commander(config['commander'])

    commander.start()

    try:
        loop.run_forever()
    except asyncio.CancelledError:
        pass
    finally:
        commander.stop()
        loop.close()
