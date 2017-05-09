import asyncio


class BlinkGenerator:

    def start(self):
        self.task = asyncio.async(self.blink())

    def stop(self):
        self.task.cancel()

    @asyncio.coroutine
    def blink(self):
        while True:
            yield from asyncio.sleep(0.5)
            print('Blink')
