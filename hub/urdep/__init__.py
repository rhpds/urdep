import logging

from datetime import datetime, timezone

from pythonjsonlogger import jsonlogger

import urdep.db

logger = None

class UrDepJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(UrDepJsonFormatter, self).add_fields(log_record, record, message_dict)

        log_record.pop('taskName')
        if not log_record.get('timestamp'):
            now = datetime.now(timezone.utc).strftime('%FT%TZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname

def setup_logging():
    global logger
    logger = logging.getLogger('urdep')
    logHandler = logging.StreamHandler()
    formatter = UrDepJsonFormatter()
    logHandler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(logHandler)

async def on_startup():
    setup_logging()
    await urdep.db.on_startup()
