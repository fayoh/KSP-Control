#!/usr/bin/python3

import asyncio, signal, os
from  blink  import blink
import  ipc.coordinator

loop = asyncio.get_event_loop()

def my_interrupt_handler():
    print('Stopping')
    for task in asyncio.Task.all_tasks():
        task.cancel()
    loop.stop()

loop.add_signal_handler(signal.SIGINT, my_interrupt_handler)
loop.add_signal_handler(signal.SIGHUP, my_interrupt_handler)

blink.start()
ipc.coordinator.start(loop)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
except asyncio.CancelledError:
    print('Tasks has been canceled')
finally:
    ipc.coordinator.stop()
    os.remove('/tmp/coord.socket')
    loop.close()
