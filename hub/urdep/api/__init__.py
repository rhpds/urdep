#
# The urdep API handles incoming requests from outside integrations and
# actuators.
# Many instances of the API should run concurrently.
#
import os

import uvicorn

from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

import urdep

from ..config import config
#from .log_middleware import LogMiddleware

#app = FastAPI()
#app.add_middleware(LogMiddleware)

#class HealthStatus(BaseModel):
#    ok: bool = True
#
#@app.get("/health", response_model=HealthStatus)
#async def get_health():
#    """Hello"""
#    return {"ok": True}

def run():
    port = int(os.getenv('URDEP_API_PORT', 8080))
    uvicorn.run(
        app="urdep.api.server:app",
        host=config.api_host,
        port=config.api_port,
        reload=True if config.environment != "production" else False,
        workers=1,
        log_config=None,
    )

