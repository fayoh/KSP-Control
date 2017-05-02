#!/usr/bin/python3

import asyncio, signal
from  blink  import blink
from  ipc import coordinator_receiver

loop = asyncio.get_event_loop()

def my_interrupt_handler():
    print('Stopping')
    for task in asyncio.Task.all_tasks():
        task.cancel()
    loop.stop()

loop.add_signal_handler(signal.SIGINT, my_interrupt_handler)

blink.start()
coordinator_receiver.start(loop)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
except asyncio.CancelledError:
    print('Tasks has been canceled')
finally:
    coordinator_receiver.stop()
    loop.close()
