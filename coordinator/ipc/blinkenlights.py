import asyncio


@asyncio.coroutine
def connect():
    global blinkenlight_client
    loop = asyncio.get_event_loop()
    print('Connecting to blinkenlights')
    while True:
        try:
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
        self.message = "message"

    def connection_made(self, transport):
        transport.write(self.message.encode())
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

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
