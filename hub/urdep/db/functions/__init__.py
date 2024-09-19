import os
import pathlib
import re

from alembic_utils.pg_function import PGFunction

db_name_prefix = os.getenv('DB_NAME_PREFIX', 'urdep_')
pg_functions = []

for path in (pathlib.Path(__file__).parent).iterdir():
    if path.name.endswith('.sql'):
        with open(path) as fh:
            sql = fh.read()
            sql = re.sub(r' urdep_', f" {db_name_prefix}", sql)
            match = re.match(r'CREATE OR REPLACE FUNCTION urdep_([^\s]+)\s+(.*)', sql, re.DOTALL)
            pg_functions.append(
                PGFunction(
                  schema="public",
                  signature=f"{db_name_prefix}{match.group(1)}",
                  definition=match.group(2),
                )
            )
