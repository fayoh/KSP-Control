import asyncio

class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        try:
            message = data.decode()
        except Exception:
            print('Ignoring malformed data')
        else:
            print('Data received: {!r}'.format(message))
            print('Send: {!r}'.format(message))
            self.transport.write(data)

    def connection_lost(self, exc):
        print('The client closed the connection')



def start(loop):
    global coordinator_server
    coro = loop.create_server(EchoServerClientProtocol,
                              '127.0.0.1',
                              8888)
    coordinator_server = loop.run_until_complete(coro)

def stop():
    pass #TODO: We must be able to dig out server somewhere?
    coordinator_server.close()
