from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

import urdep
from .log_middleware import LogMiddleware

from .status.adapter.input.api import router as status_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await urdep.on_startup()
    yield
    await urdep.on_shutdown()

def create_app() -> FastAPI:
    app = FastAPI(
        title="UrDep",
        description="UrDep API",
        lifespan=lifespan,
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    app.add_middleware(LogMiddleware)
    init_routers(app)
    return app

def init_routers(app: FastAPI) -> None:
    app.include_router(status_router)

app = create_app()
