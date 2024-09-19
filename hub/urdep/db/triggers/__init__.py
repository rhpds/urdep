import os
import pathlib
import re

from alembic_utils.pg_trigger import PGTrigger

db_name = os.getenv('DB_NAME', 'urdep')
db_name_prefix = os.getenv('DB_NAME_PREFIX', 'urdep_')
pg_triggers = []

for path in (pathlib.Path(__file__).parent).iterdir():
    if path.name.endswith('.sql'):
        with open(path) as fh:
            sql = fh.read()
            sql = re.sub(r' urdep_', f" {db_name_prefix}", sql)
            match = re.match(r'CREATE OR REPLACE TRIGGER urdep_([^\s]+)(.*\sON\s+([^\s]+).*)', sql, re.DOTALL)
            pg_triggers.append(
                PGTrigger(
                  schema="public",
                  signature=f"{db_name_prefix}{match.group(1)}",
                  on_entity=match.group(3),
                  definition=match.group(2),
                )
            )
