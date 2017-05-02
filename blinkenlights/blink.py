import asyncio

@asyncio.coroutine
def blink():
    while True:
        yield from asyncio.sleep(0.5)
        print('Blink')
