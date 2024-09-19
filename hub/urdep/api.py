#
# The urdep API handles incoming requests from outside integrations and
# actuators.
# Many instances of the API should run concurrently.
#
import os

import aiohttp
from aiohttp import web

import urdep

async def on_startup(app):
    await urdep.on_startup()

async def on_cleanup(app):
    pass

routes = web.RouteTableDef()
@routes.post('/api/login')
async def post_api_login(request):
    return web.json_response({
        "ok": True,
    })

app = web.Application()
app.add_routes(routes)
app.on_startup.append(on_startup)
app.on_cleanup.append(on_cleanup)

def run():
    port = int(os.getenv('URDEP_API_PORT', 8080))
    web.run_app(app, port=port)
