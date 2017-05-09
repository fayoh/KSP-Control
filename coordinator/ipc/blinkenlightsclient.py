import asyncio
import time
import pickle
import sys
import os
from common.devices import LED
from common.devices import LEDStates
from common.devices import LED_DICT
from common.devices import LED_STATES_DICT


class BlinkenlightsClient:
    class BlinkenlightsClientProtocol(asyncio.Protocol):
        def __init__(self, blinkenlightsclient):
            self.blinkenlightsclient = blinkenlightsclient
            self.blinkenlightsclient.client = self

        def connection_made(self, transport):
            pass

        def data_received(self, data):
            pass

        def send_data(self, message):
            data = pickle.dumps(message)
            self.transport.write(data)

        def connection_lost(self, exc):
            print('The server closed the connection')
            asyncio.async(self.blinkenlightsclient.connect())

    def __init__(self, domainsocket, coordinator):
        self.domainsocket = domainsocket
        self.coordinator = coordinator
        self.transport = None

    @asyncio.coroutine
    def connect(self):
        loop = asyncio.get_event_loop()
        print('Connecting to blinkenlights')
        while True:
            try:
                client = yield from loop.create_unix_connection(
                    lambda: self.BlinkenlightsClientProtocol(self),
                    self.domainsocket)
            except OSError as e:
                print('Connection to blinkenlights failed, '
                      'retrying in 5 seconds')
                yield from asyncio.sleep(5)
            else:
                break

    def start(self):
        print('IPC client towards Blinkenlight starting')
        asyncio.async(self.connect())

    def stop(self):
        if self.transport:
            self.transport.close()

    def handle_data_from_blinkenlights(self, message):
        pass

    def send_data_to_blinkenlights(self, message):
        self.client.send_data(message)
