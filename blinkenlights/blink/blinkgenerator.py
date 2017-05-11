import asyncio


class BlinkGenerator:

    def __init__(self, blinkfrequency):
        self.blinkfrequency = blinkfrequency
        self.ok = False

    def start(self):
        self.task = asyncio.async(self.blink())
        self.ok = True

    def stop(self):
        self.task.cancel()
        self.ok = False

    @asyncio.coroutine
    def blink(self):
        sleep = 1/self.blinkfrequency
        while True:
            yield from asyncio.sleep(sleep)
            print('Blink')
