import asyncio


@asyncio.coroutine
def blink():
    while True:
        yield from asyncio.sleep(0.5)
        print('Blink')


def start():
    asyncio.get_event_loop().call_soon(lambda: asyncio.async(blink()))
