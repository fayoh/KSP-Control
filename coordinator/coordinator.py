#!/usr/bin/python3

import asyncio, signal
from ipc import blinkenlights_client

def my_interrupt_handler():
    print('Stopping')
    for task in asyncio.Task.all_tasks():
        task.cancel()
    loop.stop() #only necessary when we run run_forever


loop = asyncio.get_event_loop()

loop.add_signal_handler(signal.SIGINT, my_interrupt_handler)

blinkenlights_client.start()

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
except asyncio.CancelledError:
    ipc_send.stop()
    print('Tasks has been canceled')
finally:
    loop.close()
