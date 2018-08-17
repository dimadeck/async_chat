from multiprocessing import Process, Manager
from time import sleep

from base_server.connected import Connected
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


def main():
    connections = Connected()

    # manager = Manager()
    # ns = manager.Namespace()
    # ns.conn = connections

    setup = {'servers': [as_main, tor_main, tw_main],
             'connections': connections,
             'ports': [8000, 8080, 8888]}

    launch = LaunchProcesses(**setup)
    try:
        launch.engine()
    except KeyboardInterrupt:
        pass
