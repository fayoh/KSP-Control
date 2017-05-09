import asyncio
import pickle
import functools
import os
import concurrent.futures

class BlinkenlightsServer:
    class  CoordinatorProtocol(asyncio.Protocol):
        def __init__(self, blinkenlights_server):
            self.blinkenlights_server = blinkenlights_server
            self.Transport = None

        def connection_made(self, transport):
            print('Connection established with coordinator')
            self.transport = transport
            self.blinkenlights_server.connection = self

        def data_received(self, data):
            try:
                message = pickle.loads(data)
            except pickle.PickleError as e:
                print('Ignoring malformed data', data, e.strerror)

        def send_data(self, message):
            data = pickle.loads(message)
            self.transport.write(data)

        def connection_lost(self, exc):
            print('The client closed the connection')


    def __init__(self, domainsocket, blinkenlights):
        self.connection = None
        self.domainsocket = domainsocket
        self.blinkenlights = blinkenlights
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=3,)
        self.loop = asyncio.get_event_loop()
        self.server = self.loop.create_unix_server(
            functools.partial(self.CoordinatorProtocol, self),
            self.domainsocket)

    def start(self):
        try:
            os.remove(self.domainsocket)
        except:
            pass
        finally:
            self.loop.run_until_complete(self.server)
            print("Server started")



    def stop(self):
        self.server.close()
        self.executor.shutdown(wait=False)
        os.remove(self.domainsocket)
