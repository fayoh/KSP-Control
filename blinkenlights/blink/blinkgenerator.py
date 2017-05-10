import asyncio


class BlinkGenerator:

    def __init__(self, blinkfrequency):
        self.blinkfrequency = blinkfrequency

    def start(self):
        self.task = asyncio.async(self.blink())

    def stop(self):
        self.task.cancel()

    @asyncio.coroutine
    def blink(self):
        sleep = 1/self.blinkfrequency
        while True:
            yield from asyncio.sleep(sleep)
            print('Blink')
