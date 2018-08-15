from aiohttp_web import main as aio_main
from chat_asyncio import main as as_main
from base_server.connected import Connected


def main():
    connections = Connected()
    as_main(connections)
    aio_main(connections)


if __name__ == '__main__':
    main()
