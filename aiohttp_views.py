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

    name = await ws_current.receive()
    name = name.data

    print(f'{name} joined.')

    await ws_current.send_json({'action': 'connect', 'name': name})
    await ws_current.send_json({'action': 'get_version', 'version': VERSION})
    for ws in request.app['websockets'].values():
        await ws.send_json({'action': 'join', 'name': name})
    request.app['websockets'][name] = ws_current

    while True:
        msg = await ws_current.receive()
        if msg.type == aiohttp.WSMsgType.text:
            for ws in request.app['websockets'].values():
                await ws.send_json(
                    {'action': 'sent', 'name': name, 'text': msg.data})
        else:
            break

    del request.app['websockets'][name]
    print(f'{name} disconnected.')
    for ws in request.app['websockets'].values():
        await ws.send_json({'action': 'disconnect', 'name': name})

    return ws_current
