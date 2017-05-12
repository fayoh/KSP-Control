import asyncio
import logging
import signal
from contextlib import suppress
from common.coordinatorclient import CoordinatorClient
import common.protocol as protocol


class AbstractService:
    def __init__(self, config):
        self.config = config
        self.connectionevent = asyncio.Event()
        self.coordinatorclient = CoordinatorClient(
            config['SocketPath'], self)
        self.logger = logging.getLogger(self.get_name())
        logging.basicConfig(level=logging.DEBUG)
        self.loop = asyncio.get_event_loop()
        self.loop.add_signal_handler(signal.SIGINT, self.my_interrupt_handler)
        self.loop.add_signal_handler(signal.SIGHUP, self.my_interrupt_handler)
        self.abstract_start()
        self.tasks = []

    def abstract_start(self):
        self.logger.info("Starting")
        self.coordinatorclient.start()
        self.start()
        try:
            self.loop.run_forever()
        except asyncio.CancelledError:
            print("cancelled")
        finally:
            self.abstract_stop()
            for task in asyncio.Task.all_tasks():
                task.cancel()
                with suppress(asyncio.CancelledError):
                    self.loop.run_until_complete(task)
            self.loop.close()

    def start(self):
        raise NotImplementedError()

    def abstract_stop(self):
        self.logger.info("Shutting down")

        try:
            self.send_data_to_coordinator(
                protocol.create_message(protocol.MessageType.STATUS_MSG,
                                        protocol.Status.SHUTDOWN))
        except protocol.NoConnectionError:
            pass
        self.coordinatorclient.stop()
        self.stop()

    def stop(self):
        raise NotImplementedError()

    def handle_data_from_coordinator(self, message):
        raise NotImplementedError()

    def send_data_to_coordinator(self, message):
        # The exception should probably be propagated upwards
        # for better handling
        try:
            self.coordinatorclient.send_data_to_coordinator(message)
        except protocol.NoConnectionError:
            self.logger.debug("Failed to send data, no connection")

    def abstract_handle_connect(self):
        self.send_status()
        self.handle_connect()

    def handle_connect(self):
        raise NotImplementedError()

    def send_status(self):
        raise NotImplementedError()

    def handle_disconnect(self):
        raise NotImplementedError()

    def get_name(self):
        return self.__class__.__name__

    def my_interrupt_handler(self):
        self.loop.stop()
