#!/usr/bin/python3
import asyncio
import signal
import sys
import os
import ipc.coordinator

sys.path.append(os.path.join(os.path.dirname(__file__), '..' ))
import common.devices


def my_interrupt_handler():
    print('Stopping')
    for task in asyncio.Task.all_tasks():
        task.cancel()
    loop.stop()  # only necessary when we run run_forever


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    ipc.coordinator.start()
#    kspconn.start()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    except asyncio.CancelledError:
        ipc.coordinator.stop()
        print('Tasks has been canceled')
    finally:
        loop.close()
