import krpc
import asyncio
import common.protocol as protocol

class KSPConnection:
    # TODO: Implement config parser
    def __init__(self,  config, commander):
        self.name = config.get('Name', "command center")
        self.address = config.get('KSPIp', '127.0.0.1')
        self.rpc_port = int(config.get('RpcPort', 50000))
        self.stream_port = int(config.get('StreamPort', 50001))
        self.commander = commander
        self.conn = None

    def start(self):
        asyncio.async(self.do_start())

    @asyncio.coroutine
    def do_start(self):
        while True:
            try:
                self.conn = krpc.connect(
                    name=self.name,
                    address=self.address,
                    rpc_port=self.rpc_port,
                    stream_port=self.stream_port)
            except:
                print("Failed to connect to KSP, trying again in 5 seconds.")
                yield from asyncio.sleep(5)
            else:
                print("Connected to KSP.")
                self.commander.send_data_to_coordinator(
                    (protocol.MessageType.STATUS_MSG, protocol.Status.OK))
                break

    def handle_data_from_coordinator(self, message):
        pass

    def stop(self):
        if self.conn != None:
            self.conn.close()
