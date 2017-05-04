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
    global blinkenlight_client
    loop = asyncio.get_event_loop()
    print('Connecting to blinkenlights')
    while True:
        try:
            global blinkenlight_client
            blinkenlight_client = yield from loop.create_unix_connection(
                EchoClientProtocol,
                '/tmp/coord.socket')
        except OSError as e:
            print('Connection to blinkenlights failed, retrying in 5 seconds')
            yield from asyncio.sleep(5)
        else:
            print('Connection to blinkenlights established')
            break


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self):
        self.message = []
        for i in range(100):
            self.message.append((LED_DICT[LED(i%43+1)],
                                 LED_STATES_DICT[LED_STATES(i%4+1)], False))

    def connection_made(self, transport):
        self.msgs_left=9
        self.start_time=time.perf_counter()
        self.transport = transport
        self.transport.write(pickle.dumps(self.message))
    def data_received(self, data):
        if self.msgs_left > 0:
            try:
                received = pickle.loads(data)
                if received != self.message:
                    print('msg corrupted', received, self.message)
                self.transport.write(pickle.dumps(received))
                self.msgs_left -=1
            except Exception as e:
                print('bad data received', data, e)
        else:
            end_time = time.perf_counter()
            elapsed_time=end_time-self.start_time
            print('done, time: ', elapsed_time)
            self.transport.close()
    def connect(self):
        asyncio.async(connect())

    def connection_lost(self, exc):
        print('The server closed the connection')
        loop = asyncio.get_event_loop()
        loop.call_later(5, self.connect)


def start():
    print('IPC client towards Blinkenlight starting')
    asyncio.async(connect())


def stop():
    pass
