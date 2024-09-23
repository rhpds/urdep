import logging

from datetime import datetime, timezone

from pythonjsonlogger import jsonlogger

from .config import config

class UrDepJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(UrDepJsonFormatter, self).add_fields(log_record, record, message_dict)

        log_record.pop('taskName', None)
        log_record.pop('color_message', None)
        if not log_record.get('timestamp'):
            now = datetime.now(timezone.utc).strftime('%FT%TZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname

def setup_logging():
    logger = logging.getLogger('urdep')
    logHandler = logging.StreamHandler()
    formatter = UrDepJsonFormatter()
    logHandler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(logHandler)
    logger.propagate = False
    logger.root.handlers = [logHandler]
    logger.root.setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").disabled = True

from .db import Actuator, Transactional
from .db.session import set_session_context, reset_session_context, session
from uuid import uuid4
@Transactional()
async def create_actuator():
    actuator = Actuator.create(
        name='test',
    )
    session.add(actuator)

async def on_startup():
    setup_logging()
    logger = logging.getLogger('urdep')
    logger.info("HERE")
    session_id = str(uuid4())
    context = set_session_context(session_id=session_id)
    try:
        await create_actuator()
    finally:
        await session.remove()
        reset_session_context(context=context)


async def on_shutdown():
    pass
