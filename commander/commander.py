#!/usr/bin/python3
import asyncio
import configparser
import logging
import common.protocol as protocol
from common.service import AbstractService
from kspconn.kspconn import KSPConnection



class Commander(AbstractService):
    def __init__(self, config):
        self.kspconnection = KSPConnection(config, commander=self)
        super(Commander, self).__init__(config)

    def start(self):
        self.kspconnection.start()

    def stop(self):
        self.coordinatorclient.stop()
        self.kspconnection.stop()

    def handle_data_from_coordinator(self, message):
        self.kspconnection.handle_data_from_coordinator(message)


    def handle_connect(self):
        pass
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


if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read('common/config.ini')
    commander = Commander(config['commander'])
