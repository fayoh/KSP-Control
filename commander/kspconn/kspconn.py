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
        self.statemethods = {}
        self.current_scene = None

    def start(self):
        asyncio.async(self.do_start())

    @asyncio.coroutine
    def do_start(self):
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
        scene = self.conn.krpc.current_game_scene
        if scene == self.conn.krpc.GameScene.flight:
            self.enter_new_state(scene.name, protocol.GameScene.FLIGHT)
        else:
            self.enter_new_state(scene.name, protocol.GameScene.SPACE_CENTER)
        self.state[protocol.KrpcInfo.GAME_SCENE] = scene

    def enter_new_state(self, name, new_scene):
        self.exit_state()
        self.state[protocol.KrpcInfo.GAME_SCENE] = new_scene
        self.current_scene = asyncio.async(self.statemethods[new_scene]())
        message = protocol.create_message(
            protocol.MessageType.KRPC_INFO_MSG,
            (protocol.KrpcInfo.GAME_SCENE, self.krpc_to_internal[new_scene]))
        try:
            self.commander.send_data_to_coordinator(message)
        except protocol.NoConnectionError:
            asyncio.async(self.send_on_connection(message))

    def get_scene(self):
        return self.krpc_to_internal[self.state[protocol.KrpcInfo.GAME_SCENE]]

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

    # State handlers
    @asyncio.coroutine
    def space_center(self):
        self.logger.debug("Entering space center")
        while True:
            yield from asyncio.sleep(0.1) # TODO in config
            scene = self.conn.krpc.current_game_scene
            if self.state[protocol.KrpcInfo.GAME_SCENE] != scene:
                break
        self.enter_new_state(scene)

    @asyncio.coroutine
    def flight(self):
        self.logger.debug("Entering flight")
        while True:
            yield from asyncio.sleep(0.1) # TODO in config
            scene = self.conn.krpc.current_game_scene
            if self.state[protocol.KrpcInfo.GAME_SCENE] != scene:
                break
        self.enter_new_state(scene)

    def exit_state(self):
        self.logger.info("Exciting state %s", )
