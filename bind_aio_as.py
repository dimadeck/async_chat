from multiprocessing import Process
from time import sleep

from base_server.connected import Connected
from chat_asyncio import main as as_main
from chat_tornado import main as tor_main
from chat_twisted import main as tw_main


class A:
    def __init__(self, func, port, connections):
        self.func = func
        self.connections = connections
        self.port = port

    def __call__(self, sleep_time=0.5):
        self.func(port=self.port, connections=self.connections)
        sleep(sleep_time)


if __name__ == '__main__':
    connections = Connected()
    ports = [8000, 8080, 8888]

    a = A(as_main, ports.pop(), connections)
    b = A(tor_main, ports.pop(), connections)
    c = A(tw_main, ports.pop(), connections)

    p1 = Process(target=a)
    p2 = Process(target=b)
    p3 = Process(target=c)

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()
