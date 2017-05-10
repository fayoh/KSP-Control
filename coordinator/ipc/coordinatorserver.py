import asyncio
import pickle
import functools
import os
import concurrent.futures
import common.protocol as protocol
from common.protocol import MessageType
from common.protocol import Status

class CoordinatorServer:
    class  CoordinatorProtocol(asyncio.Protocol):
        def __init__(self, coordinator_server):
            self.coordinator_server = coordinator_server
            self.transport = None
            self.client = None

        def connection_made(self, transport):
            self.transport = transport

        def data_received(self, data):
            try:
                message = pickle.loads(data)
                if not protocol.is_correct_message(message):
                    raise Exception()
            except pickle.PickleError as e:
                print('Ignoring malformed data', data, e)
            else:
                msgtype = protocol.get_message_type(message)

                if self.client == None:
                    self.identify(message)
                else:
                    coordinator_server.handle_data_from(self.client, message)

        def connection_lost(self, exc):
            print('The client closed the connection')
            # TODO: remove connection from list

        def send_data(self, message):
            data = pickle.dumps(message)
            self.transport.write(data)

        def identify(self, message):
            msgtype = protocol.get_message_type(message)
            if msgtype == protocol.MessageType.IDENTIFY:
                msgdata = protocol.get_message_data(message)
                print(msgdata)
                if isinstance(msgdata, protocol.Identity):
                    self.client = msgdata
                    self.coordinator_server.add_connection(msgdata, self)

    def __init__(self, socketpath, coordinator):
        self.commanderconnection = None
        self.blinkenlightsconnection = None
        self.socketpath = socketpath
        self.coordinator = coordinator
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=3,)
        self.loop = asyncio.get_event_loop()
        self.server = self.loop.create_unix_server(
            lambda: self.CoordinatorProtocol(self), self.socketpath)
        self.connections = {}

    def start(self):
        try:
            os.remove(self.socketpath)
        except:
            pass
        finally:
            self.loop.run_until_complete(self.server)
            print("Server started")

    def stop(self):
        self.broadcast(
            protocol.create_message(MessageType.STATUS_MSG, Status.SHUTDOWN))
        self.server.close()
        self.executor.shutdown(wait=False)
        os.remove(self.socketpath)

    def add_connection(self, name, connection):
        print("Connection made from ", name)
        self.connections[name] = connection

    def handle_data_from(self, message):
        self.coordinator.handle_data_from_coordinator(message)

    def send_data_to_blinkenlights(self, message):
        self.blinkenlightsconnection.send_data(message)

    def send_data_to_commander(self, message):
        self.commanderconnection.send_data(message)

    def broadcast(self, message):
        for connection in self.connections.values():
            connection.send_data(message)
