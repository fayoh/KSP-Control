import asyncio
import time
import pickle
import sys
import os
import logging
import common.protocol as protocol
from common.protocol import Identity

class CoordinatorClient:
    class CoordinatorClientProtocol(asyncio.Protocol):
        def __init__(self, coordinatorclient):
            self.coordinatorclient = coordinatorclient
            self.coordinatorclient.protocol = self
            self.logger = logging.getLogger(__name__)
            self.transport = None
            self.running = False

        def stop(self):
            self.running = False
            if self.transport is not None:
                self.transport.close()

        def connection_made(self, transport):
            self.running = True
            self.transport = transport
            # TODO: shall we be proper and implement a confirmation fom
            # the coordinator?
            identity = protocol.create_message(
                protocol.MessageType.IDENTIFY,
                self.coordinatorclient.identity)
            self.send_data(identity)
            self.coordinatorclient.service.connectionevent.set()
            self.logger.info("Connected to coordinator")
            self.coordinatorclient.service.abstract_handle_connect()

        def get_name(self):
            return self.__class__.__name__

        def data_received(self, data):
            try:
                message = pickle.loads(data)
                if not protocol.is_correct_message(message):
                    raise Exception()
                self.coordinatorclient.handle_data_from_coordinator(message)
            except Exception as e:
                self.logger.warning('Ignoring malformed data', data, e)
            else:
                self.coordinatorclient.handle_data_from_coordinator(message)

        def send_data(self, message):
            if self.transport == None:
                raise protocol.NoConnectionError
            protocol.assert_correct_message(message)
            data = pickle.dumps(message)
            self.transport.write(data)

        def connection_lost(self, exc):
            if self.running:
                self.logger.warning('Coordinator closed the connection')
                self.coordinatorclient.protocol = None
                self.transport.close()
                self.coordinatorclient.service.handle_disconnect()
                asyncio.ensure_future(self.coordinatorclient.connect())

    def __init__(self, socketpath, service):
        self.socketpath = socketpath
        self.service = service
        # TODO: Make a mapping from name to identity
        #   ...or make the service return an identity
        if service.get_name() == 'Commander':
            self.identity = Identity.COMMANDER
        if service.get_name() == 'Blinkenlights':
            self.identity = Identity.BLINKENLIGHTS
        self.protocol = None
        self.logger = logging.getLogger(__name__)


    async def connect(self):
        loop = asyncio.get_event_loop()
        while True:
            try:
                await loop.create_unix_connection(
                    lambda: self.CoordinatorClientProtocol(self),
                    self.socketpath)
            except OSError as e:
                self.logger.info('Connection to coordinator failed, '
                      'retrying in 5 seconds')
                await asyncio.sleep(5)
            else:
                return True

    def start(self):
        self.logger.info('IPC client towards coordinator starting')
        asyncio.ensure_future(self.connect())

    def stop(self):
        if self.protocol is not None:
            self.protocol.stop()

    def handle_data_from_coordinator(self, message):
        self.service.handle_data_from_coordinator(message)

    def send_data_to_coordinator(self, message):
        protocol.assert_correct_message(message)
        if self.protocol == None:
            raise protocol.NoConnectionError
        self.protocol.send_data(message)
