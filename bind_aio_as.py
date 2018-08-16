from multiprocessing import Process
from time import sleep

from aiohttp_web import main as aio_main
from base_server.connected import Connected
from chat_asyncio import main as as_main
from chat_tornado import main as tor_main



class A:
    def __init__(self, func, connections):
        self.func = func
        self.connection = connections

    def __call__(self, sleep_time=0.5):
        self.func(connections)
        sleep(sleep_time)


if __name__ == '__main__':
    connections = Connected()

    a = A(as_main, connections)
    b = A(tor_main, connections)

    p1 = Process(target=a)
    p2 = Process(target=b)
    p1.start()
    p2.start()

    p1.join()
    p2.join()
