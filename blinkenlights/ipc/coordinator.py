import asyncio
import pickle
import time
import concurrent.futures
import functools
import threading

lock = threading.Lock()

def blocking(num):
    with (lock):
        time.sleep(1)
        print('banan', num)


# Create a limited thread pool.
executor = concurrent.futures.ThreadPoolExecutor(max_workers=3,)


class  EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport
        self.counter = 0
    def data_received(self, data):
        asyncio.get_event_loop().run_in_executor(executor, functools.partial(blocking, self.counter))
        self.counter +=1
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
    executor.shutdown(wait=False)
    coordinator_server.close()
