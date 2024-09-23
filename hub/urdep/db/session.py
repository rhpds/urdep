from contextlib import asynccontextmanager
from contextvars import ContextVar, Token
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session

from ..config import config

session_context: ContextVar[str] = ContextVar("session_context")

def get_session_context() -> str:
    return session_context.get()

def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)

def reset_session_context(context: Token) -> None:
    session_context.reset(context)

engine = create_async_engine(
    config.db_url,
    pool_pre_ping=True,
    pool_size=config.db_pool_size,
    max_overflow=config.db_max_overflow,
    pool_recycle=config.db_pool_recycle,
    pool_timeout=config.db_pool_timeout,
    future=True,
    echo=False,
)

class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None, **kw):
        return engine.sync_engine

_async_session_factory = async_sessionmaker(
    class_=AsyncSession,
    sync_session_class=RoutingSession,
    expire_on_commit=False,
)
session = async_scoped_session(
    session_factory=_async_session_factory,
    scopefunc=get_session_context,
)
# WTH?
#session.configure(bind=engine)

@asynccontextmanager
async def session_factory() -> AsyncGenerator[AsyncSession, None]:
    _session = async_sessionmaker(
        class_=AsyncSession,
        expire_on_commit=False,
    )()
    try:
        yield _session
    finally:
        await _session.close()
