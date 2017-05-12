import asyncio
from contextlib import suppress

class BlinkGenerator:

    def __init__(self, blinkfrequency):
        self.blinkfrequency = blinkfrequency
        self.ok = False

    @asyncio.coroutine
    def start(self):
        asyncio.async(self.blink())
        self.ok = True

    def stop(self):
        self.ok = False

    @asyncio.coroutine
    def blink(self):
        sleep = 1/self.blinkfrequency
        while True:
                yield from asyncio.sleep(sleep)
                print('Blink')
