import asyncio
from contextlib import suppress

class BlinkGenerator:

    def __init__(self, blinkfrequency):
        self.blinkfrequency = blinkfrequency
        self.ok = False


    async def start(self):
        asyncio.ensure_future(self.blink())
        self.ok = True

    def stop(self):
        self.ok = False

    async def blink(self):
        sleep = 1/self.blinkfrequency
        while True:
            await asyncio.sleep(sleep)
            print('Blink')
