import asyncio

from aiohttp import web

from chats.chat_asyncio import AsyncioChat
from chats.chat_ws_asyncio import AioChat


def main(port1=8000, port2=8080, connections=None):
    server = AsyncioChat(connections=connections, port=port1)
    server1 = AioChat(connections=server.chat.connections, port=port2)
    app = server1.init_app()

    server.chat.set_outside_request(server1.chat.from_outside)
    server1.chat.set_outside_request(server.chat.from_outside)

    loop = asyncio.get_event_loop()
    loop.create_task(asyncio.start_server(server.handle_client, '127.0.0.1', port1))
    loop.create_task(web.run_app(app, port=port2, host='127.0.0.1'))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()


if __name__ == '__main__':
    main()
