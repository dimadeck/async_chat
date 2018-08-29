from multiprocessing import Process
from time import sleep

from chats.chat_asyncio import main as as_main
from chats.chat_tornado import main as tor_main
from chats.chat_twisted import main as tw_main
from chats.chat_ws_asyncio import main as aio_ws_main
from chats.chat_ws_tornado import main as tor_ws_main
from chats.chat_ws_twisted import main as tw_ws_main


class Connect:
    def __init__(self, server, port):
        self.server = server
        self.port = port

    def __call__(self, sleep_time=0.5):
        self.server(port=self.port)
        sleep(sleep_time)


class LaunchProcesses:
    def __init__(self, servers, ports):
        self.processes = []
        self.ports = ports
        self.servers = servers

    def engine(self):
        self.create_process()
        self.start_processes()
        self.join_processes()

    def create_process(self):
        for server in self.servers:
            port = self.get_port()
            target = Connect(server, port)
            self.processes.append(Process(target=target))

    def get_port(self):
        return self.ports.pop()

    def start_processes(self):
        for process in self.processes:
            process.start()

    def join_processes(self):
        for process in self.processes:
            process.join()


def setup(mode):
    settings = None
    if mode == 'tcp_all':
        settings = {'servers': [as_main, tor_main, tw_main],
                    'ports': [8000, 8080, 8888]}
    elif mode == 'as':
        settings = {'servers': [as_main, aio_ws_main],
                    'ports': [8080, 8000]}
    elif mode == 'tor':
        settings = {'servers': [tor_main, tor_ws_main],
                    'ports': [8080, 8000]}
    elif mode == 'tw':
        settings = {'servers': [tw_main, tw_ws_main],
                    'ports': [8080, 8000]}
    elif mode == 'ws_all':
        settings = {'servers': [aio_ws_main, tor_ws_main, tw_ws_main],
                    'ports': [8000, 8080, 8888]}
    return settings


def main(mode):
    # manager = Manager()
    # ns = manager.Namespace()
    # ns.mess = 0

    settings = setup(mode)
    try:
        LaunchProcesses(**settings).engine()
    except KeyboardInterrupt:
        pass
