import asyncio
import pickle
import functools
import os
import concurrent.futures
import logging
import common.protocol as protocol
from common.protocol import MessageType
from common.protocol import Status

class CoordinatorServer:
    class  CoordinatorProtocol(asyncio.Protocol):
        def __init__(self, coordinator_server):
            self.coordinator_server = coordinator_server
            self.transport = None
            self.client = None
            self.logger = logging.getLogger(__name__)

        def connection_made(self, transport):
            self.transport = transport

        def data_received(self, data):
            try:
                message = pickle.loads(data)
                protocol.assert_correct_message(message)
            except pickle.PickleError as e:
                self.logger.warn('Ignoring malformed data', data, e)
            else:
                msgtype = protocol.get_message_type(message)

                if self.client == None:
                    self.identify(message)
                else:
                    self.coordinator_server.handle_data_from_client(
                        self.client, message)

        def connection_lost(self, exc):
            if self.client is not None:
                self.coordinator_server.remove_connection(self.client)

        def send_data(self, message):
            data = pickle.dumps(message)
            self.transport.write(data)

        def identify(self, message):
            msgtype = protocol.get_message_type(message)
            if msgtype == protocol.MessageType.IDENTIFY:
                msgdata = protocol.get_message_data(message)
                if isinstance(msgdata, protocol.Identity):
                    self.client = msgdata
                    self.coordinator_server.add_client(msgdata, self)
            else:
                logger.debug("Data received before identification", message)

    def __init__(self, socketpath, coordinator):
        self.socketpath = socketpath
        self.coordinator = coordinator
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=3,)
        self.loop = asyncio.get_event_loop()
        self.server = self.loop.create_unix_server(
            lambda: self.CoordinatorProtocol(self), self.socketpath)
        self.clients = {}
        self.logger = logging.getLogger(__name__)

    def start(self):
        try:
            os.remove(self.socketpath)
        except:
            pass
        finally:
            self.loop.run_until_complete(self.server)
            self.logger.info("Server started")

    def stop(self):
        self.broadcast(
            protocol.create_message(MessageType.STATUS_MSG, Status.SHUTDOWN))
        self.server.close()
        self.executor.shutdown(wait=False)
        os.remove(self.socketpath)

    def add_client(self, name, client):
        self.logger.info("Connection made from %s", name.name)
        self.clients[name] = client

    def remove_connection(self, name):
        self.logger.info("%s disconnected", name.name)
        del self.clients[name]

    def handle_data_from_client(self, client, message):
        if client == protocol.Identity.BLINKENLIGHTS:
            self.coordinator.handle_data_from_blinkenlights(message)
        elif client == protocol.Identity.COMMANDER:
            self.coordinator.handle_data_from_commander(message)
        else:
            raise UnknownClientError

    def send_data_to_blinkenlights(self, message):
        protocol.assert_correct_message(message)
        self.clients[protocol.Identity.BLINKENLIGHTS].send_data(message)

    def send_data_to_commander(self, message):
        protocol.assert_correct_message(message)
        self.clients[protocol.Identity.COMMANDER].send_data(message)

    def broadcast(self, message):
        protocol.assert_correct_message(message)
        for client in self.clients.values():
            client.send_data(message)
