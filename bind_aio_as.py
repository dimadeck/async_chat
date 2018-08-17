from multiprocessing import Process
from time import sleep
from chat_asyncio import main as as_main
from chat_tornado import main as tor_main
from chat_twisted import main as tw_main

from base_server.connected import Connected


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
    c = A(tw_main, connections)

    p1 = Process(target=a)
    p2 = Process(target=b)
    p3 = Process(target=c)

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()
