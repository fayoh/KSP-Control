import asyncio
import time
import pickle
import sys
import os
from common.devices import LED
from common.devices import LEDStates
from common.devices import LED_DICT
from common.devices import LED_STATES_DICT


class CommanderClient:
    class CommanderProtocol(asyncio.Protocol):
        def __init__(self, commanderclient):
            self.commanderclient = commanderclient

        def connection_made(self, transport):
            self.transport = transport
            print("Connection to commander established")

        def data_received(self, data):
            try:
                received = pickle.loads(data)
            except Exception as e:
                print('bad data received', data, e)

        def connection_lost(self, exc):
            print('The server closed the connection will reconnect')
            asyncio.async(self.commanderclient.connect())


    def __init__(self, domainsocket, coordinator):
        self.domainsocket = domainsocket
        self.coordinator = coordinator
        self.transport = None

    @asyncio.coroutine
    def connect(self):
        loop = asyncio.get_event_loop()
        print('Connecting to commander')
        while True:
            try:
                client = yield from loop.create_unix_connection(
                    lambda: self.CommanderProtocol(self), self.domainsocket)
                (self.transport, self.protocol)  = client
            except OSError as e:
                print('Connection to commander failed, retrying in 5 seconds')
                yield from asyncio.sleep(5)
            else:
                break

    def start(self):
        print('IPC client towards Commander starting')
        asyncio.async(self.connect())

    def stop(self):
        if self.transport:
            self.transport.close()
