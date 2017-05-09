import asyncio
import pickle
import functools
import os
import concurrent.futures


class CommanderServer:
    class  CoordinatorProtocol(asyncio.Protocol):
        def __init__(self, commander_server):
            self.commander_server = commander_server
            self.transport = None

        def connection_made(self, transport):
            print("Connection established with coordinator")
            self.transport = transport
            self.commander_server.connection = self

        def data_received(self, data):
            try:
                message = pickle.loads(data)
            except pickle.PickleError as e:
                print('Ignoring malformed data', data, e.strerror)
            else:
                self.commander_server.handle_data_from_coordinator(
                    message)

        def connection_lost(self, exc):
            print('The client closed the connection')

        def send_data(self, message):
            data = pickle.dumps(message)
            self.transport.write(data)

    def __init__(self, domainsocket, commander):
        self.connection = None
        self.domainsocket = domainsocket
        self.commander = commander
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=3,)
        self.loop = asyncio.get_event_loop()
        self.server = self.loop.create_unix_server(
            lambda: self.CoordinatorProtocol(self), self.domainsocket)


    def start(self):
        try:
            os.remove(self.domainsocket)
        except:
            pass
        finally:
            self.loop.run_until_complete(self.server)
            print("Server started")

    def stop(self):
        if self.connection:
            self.send_data_to_coordinator('the end')
        self.server.close()
        self.executor.shutdown(wait=False)
        os.remove(self.domainsocket)

    def handle_data_from_coordinator(self, message):
        self.commander.handle_data_from_coordinator(message)

    def send_data_to_coordinator(self, message):
        self.connection.send_data(message)
