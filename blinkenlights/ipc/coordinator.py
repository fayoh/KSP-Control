import asyncio
import pickle

class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport
    def data_received(self, data):
        try:
            message = pickle.loads(data)
            data2 = pickle.dumps(message)
            self.transport.write(data2)
        except pickle.PickleError as e:
            print('Ignoring malformed data', data, e.strerror)

    def connection_lost(self, exc):
        print('The client closed the connection')


def start(loop):
    global coordinator_server
    coro = loop.create_unix_server(EchoServerClientProtocol,
                                   '/tmp/coord.socket')
    coordinator_server = loop.run_until_complete(coro)


def stop():
    pass  # TODO: We must be able to dig out server somewhere?
    coordinator_server.close()
