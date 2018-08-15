import aiohttp
import aiohttp_jinja2
from aiohttp import web

VERSION = 'aioChat'


async def index(request):
    ws_current = web.WebSocketResponse()
    ws_ready = ws_current.can_prepare(request)
    if not ws_ready.ok:
        return aiohttp_jinja2.render_template('index.html', request, {})
    await ws_current.prepare(request)
    name = await get_name(ws_current)
    print(f'{name} joined.')
    await send_to(ws_current, action='connect', name=name)
    await send_all(request, action='join', name=name)
    add_connection(request, ws_current, name)
    await chat_engine(request, ws_current, name)
    await close_connection(request, name)
    print(f'{name} disconnected.')
    return ws_current


async def send_all(request, **kwargs):
    for connection in request.app['websockets'].values():
        await connection.send_json(kwargs)


async def send_to(connection, **kwargs):
    await connection.send_json(kwargs)


async def get_name(connection):
    name = await connection.receive()
    return name.data


def add_connection(request, connection, name):
    request.app['websockets'][name] = connection


async def chat_engine(request, connection, name):
    while True:
        msg = await connection.receive()
        if msg.type == aiohttp.WSMsgType.text:
            await send_all(request, action='sent', name=name, text=msg.data)
        else:
            break


async def close_connection(request, name):
    del request.app['websockets'][name]
    await send_all(request, action='disconnect', name=name)
