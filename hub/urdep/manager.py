#
# The urdep manager handles state transitions and maintenance tasks.
# Only one instance of the manager should run.
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
@routes.get('/api/health')
async def get_api_health(request):
    return web.json_response({
        "ok": True,
    })

app = web.Application()
app.add_routes(routes)
app.on_startup.append(on_startup)
app.on_cleanup.append(on_cleanup)

def run():
    port = int(os.getenv('URDEP_MANAGER_PORT', 8081))
    web.run_app(app, port=port)
