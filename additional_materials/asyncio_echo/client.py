import asyncio


async def tcp_echo_client(loop):
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888,
                                                   loop=loop)
    message = input()
    print(f'Send: {message}')
    writer.write(message.encode())

    data = await reader.read(100)
    print(f'Received: {data.decode("utf-8")}')

    print('Close')
    writer.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(tcp_echo_client(loop))
loop.close()
