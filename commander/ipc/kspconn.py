import krpc
import asyncio


class KSPConnection:
    def __init__(self,
                 commander,
                 name="",
                 address='127.0.0.1',
                 rpc_port=50000,
                 stream_port=50001):
        self.name = name
        self.address = address
        self.rpc_port = rpc_port
        self.stream_port = stream_port
        self.commander = commander
        self.ksp_conn_starting = None
        self.conn = None

    def start(self):
        future = asyncio.Future()
        self.kspconn_starting = asyncio.async(
            self.do_start(future))
        future.add_done_callback(self.kspconn_done)

    @asyncio.coroutine
    def do_start(self, future):
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
                self.kspconn_starting = None
                break

    def kspconn_done(self, future):
        print("Connection to ksp established")

    def handle_data_from_coordinator(self, message):
        pass

    def stop(self):
        if self.kspconn_starting != None:
            self.kspconn_starting.cancel()
        if self.conn != None:
            self.conn.close()
