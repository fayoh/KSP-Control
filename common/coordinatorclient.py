import asyncio
import time
import pickle
import sys
import os
import common.protocol as protocol


class CoordinatorClient:
    class CoordinatorClientProtocol(asyncio.Protocol):
        def __init__(self, coordinatorclient):
            self.coordinatorclient = coordinatorclient
            self.coordinatorclient.protocol = self

        def connection_made(self, transport):
            self.transport = transport
            # TODO: shall we be proper and implement a confirmation fom
            # the coordinator?
            data = pickle.dumps(protocol.create_message(
                protocol.MessageType.IDENTIFY,
                self.coordinatorclient.identity))
            self.transport.write(data)
            self.coordinatorclient.service.connectionevent.set()
            print("Connected to coordinator")

        def data_received(self, data):
            try:
                message = pickle.loads(data)
                if not protocol.is_correct_message(message):
                    raise Exception()
                self.coordinatorclient.handle_data_from_coordinator(message)
            except Exception as e:
                print('Ignoring malformed data', data, e)
            else:
                self.coordinatorclient.handle_data_from_coordinator(message)

        def send_data(self, message):
            data = pickle.dumps(message)
            self.transport.write(data)

        def connection_lost(self, exc):
            print('The server closed the connection')
            asyncio.async(self.coordinatorclient.connect())

    def __init__(self, socketpath, service):
        self.socketpath = socketpath
        self.service = service
        if service.type == 'commander':
            self.identity = protocol.Identity.COMMANDER
        if service.type == 'blinkenlights':
            self.identity = protocol.Identity.BLINKENLIGHTS
        self.protocol = None

    @asyncio.coroutine
    def connect(self):
        loop = asyncio.get_event_loop()
        print('Connecting to coordinator')
        while True:
            try:
                yield from loop.create_unix_connection(
                    lambda: self.CoordinatorClientProtocol(self),
                    self.socketpath)
            except OSError as e:
                print('Connection to coordinator failed, '
                      'retrying in 5 seconds')
                yield from asyncio.sleep(5)
            else:
                break

    def start(self):
        print('IPC client towards coordinator starting')
        asyncio.async(self.connect())

    def stop(self):
        pass

    def handle_data_from_coordinator(self, message):
        self.service.handle_data_from_coordinator(message)

    def send_data_to_coordinator(self, message):
        # TODO: error checking here as well?
        self.protocol.send_data(message)