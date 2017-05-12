import krpc
import asyncio
import logging
from common.autonumber import AutoNumber
import common.protocol as protocol

class KSPConnection:
    # TODO: Detect disconnect from krpc-server
    def __init__(self,  config, commander):
        self.name = config.get('Name', "command center")
        self.address = config.get('KSPIp', '127.0.0.1')
        self.rpc_port = int(config.get('RpcPort', 50000))
        self.stream_port = int(config.get('StreamPort', 50001))
        self.commander = commander
        self.conn = None
        self.logger = logging.getLogger(self.get_name())
        self.ok = False
        self.streams = {}
        self.state = {}
        self.current_scene = None

    @asyncio.coroutine
    def start(self):
        while True:
            try:
                # TODO: this does not time-out but just hangs the loop
                # if the server is up but not accepting connections
                self.conn = krpc.connect(
                    name=self.name,
                    address=self.address,
                    rpc_port=self.rpc_port,
                    stream_port=self.stream_port)
            except:
                self.logger.info(
                    "Failed to connect to KSP, trying again in 5 seconds.")
                yield from asyncio.sleep(5)
            else:
                self.logger.info("Connected to KSP.")
                self.ok = True
                try:
                    self.commander.send_status()
                except protocol.NoConnectionError:
                    # If we connect to ksp before the coordinator
                    # status will be sent on connection event
                    pass
                finally:
                    break
        self.initialise()

    def initialise(self):
        self.enter_new_scene(self.conn.krpc.current_game_scene)

    @asyncio.coroutine
    def send_on_connection(self, message):
        yield from self.commander.connectionevent.wait()
        self.commander.send_data_to_coordinator(message)

    def handle_data_from_coordinator(self, message):
        pass

    def stop(self):
        if self.conn != None:
            self.conn.close()

    def handle_disconnect(self):
        self.logger.error("Handle disconnect is not implemented")

    def get_name(self):
        return self.__class__.__name__

    def get_scene(self):
        if self.state[protocol.KrpcInfo.GAME_SCENE] == self.conn.krpc.GameScene.flight:
            return protocol.GameScene.FLIGHT
        else:
           return protocol.GameScene.SPACE_CENTER

    # State handlers
    def enter_new_scene(self, new_scene):
       self.exit_current_scene()
       self.state[protocol.KrpcInfo.GAME_SCENE] = new_scene
       datatype = protocol.KrpcInfo.GAME_SCENE
       if new_scene == self.conn.krpc.GameScene.flight:
           self.current_scene = asyncio.async(self.flight())
           msgdata = (datatype, protocol.GameScene.FLIGHT)
       else:
           self.current_scene = asyncio.async(self.space_center())
           msgdata = (datatype, protocol.GameScene.SPACE_CENTER)

       message = protocol.create_message(
           protocol.MessageType.KRPC_INFO_MSG,msgdata)
       try:
           self.commander.send_data_to_coordinator(message)
       except protocol.NoConnectionError:
           asyncio.async(self.send_on_connection(message))



    def exit_current_scene(self):
        pass

    @asyncio.coroutine
    def space_center(self):
        self.logger.debug("Entering space center")
        while True:
            yield from asyncio.sleep(0.11) # TODO in config
            scene = self.conn.krpc.current_game_scene
            if self.state[protocol.KrpcInfo.GAME_SCENE] != scene:
                break
        self.enter_new_scene(scene)

    @asyncio.coroutine
    def flight(self):
        self.logger.debug("Entering flight")
        while True:
            yield from asyncio.sleep(0.1) # TODO in config
            scene = self.conn.krpc.current_game_scene
            if self.state[protocol.KrpcInfo.GAME_SCENE] != scene:
                break
        self.enter_new_scene(scene)

    def exit_scene(self):
        self.logger.info("Exciting state %s", )
