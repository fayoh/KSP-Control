#!/usr/bin/python3

import asyncio, signal
import blink

def my_interrupt_handler():
    print('Stopping')
    for task in asyncio.Task.all_tasks():
        task.cancel()

loop = asyncio.get_event_loop()

loop.add_signal_handler(signal.SIGINT, my_interrupt_handler)

try:
    loop.run_until_complete(asyncio.wait([
        blink.blink()
    ]))
except KeyboardInterrupt:
    pass
except asyncio.CancelledError:
    print('Tasks has been canceled')
finally:
    loop.close()
