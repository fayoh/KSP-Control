import asyncio
import time
import pickle
import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), '../../' ))
from common.devices import LED
from common.devices import LED_STATES
from common.devices import LED_DICT
from common.devices import LED_STATES_DICT

@asyncio.coroutine
def connect():
    global commander_client
    loop = asyncio.get_event_loop()
    print('Connecting to commander')
    while True:
        try:
            commander_client = yield from loop.create_unix_connection(
                EchoClientProtocol,
                '/tmp/commander.socket')
        except OSError as e:
            print('Connection to commander failed, retrying in 5 seconds')
            yield from asyncio.sleep(5)
        else:
            print('Connection to commander established')
            break


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self):
        self.message="banan"
    def connection_made(self, transport):
        self.transport = transport
        self.transport.write(pickle.dumps(self.message))
    def data_received(self, data):
        try:
            received = pickle.loads(data)
            if received != self.message:
                print('msg corrupted', received, self.message)
                self.transport.write(pickle.dumps(received))
        except Exception as e:
            print('bad data received', data, e)

    def connect(self):
        asyncio.async(connect())

    def connection_lost(self, exc):
        print('The server closed the connection reconnect in 5 seconds')
        loop = asyncio.get_event_loop()
        loop.call_later(5, self.connect)


def start():
    print('IPC client towards Commander starting')
    asyncio.async(connect())


def stop():
    pass
