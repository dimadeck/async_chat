import asyncio


class V1:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def compute(x, y):
        print(f'{x} + {y} = ...')
        yield from asyncio.sleep(1.0)
        return x + y

    @staticmethod
    def print_sum(x, y):
        result = yield from V1.compute(x, y)
        print(f'{x} + {y} = {result}')

    def engine(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.print_sum(self.x, self.y))
        loop.close()
