import asyncio

from aiohttp import web

from chats import AsServer, AsWsServer
from chats.chat_asyncio import AsyncioChat
from chats.chat_ws_asyncio import AioChat
from kernel.fork_chat_kernel import ChatKernel
from kernel.fork_sender import Sender


def main(port1=8000, port2=8080):
    sender = Sender()

    chat1 = ChatKernel(AsServer, port1, sender=sender)
    server1 = AsyncioChat(chat1)

    chat2 = ChatKernel(AsWsServer, port2, sender=sender)
    server2 = AioChat(chat2)
    app = server2.init_app()

    try:
        loop = asyncio.get_event_loop()
        loop.create_task(asyncio.start_server(server1.handle_client, '127.0.0.1', port1))
        loop.create_task(web.run_app(app, port=port2, host='127.0.0.1'))
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            loop.close()
    except RuntimeError:
        pass


if __name__ == '__main__':
    main()
