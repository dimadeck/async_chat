from multiprocessing import Process
from time import sleep

from aiohttp_web import main as aio_main
from kernel.connected import Connected
from chat_asyncio import main as as_main
from chat_tornado import main as tor_main
from chat_twisted import main as tw_main


class Connect:
    def __init__(self, server, port, connections):
        self.server = server
        self.connections = connections
        self.port = port

    def __call__(self, sleep_time=0.5):
        self.server(port=self.port, connections=self.connections)
        sleep(sleep_time)


class LaunchProcesses:
    def __init__(self, servers, connections, ports):
        self.processes = []
        self.ports = ports
        self.connections = connections
        self.servers = servers

    def engine(self):
        self.create_process()
        self.start_processes()
        self.join_processes()

    def create_process(self):
        for server in self.servers:
            port = self.get_port()
            target = Connect(server, port, self.connections)
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
    connections = Connected()
    if mode == 'tcp_all':
        settings = {'servers': [as_main, tor_main, tw_main],
                    'connections': connections,
                    'ports': [8000, 8080, 8888]}
    elif mode == 'as_aio':
        settings = {'servers': [as_main, aio_main],
                    'connections': connections,
                    'ports': [8080, 8000]}
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
