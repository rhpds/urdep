import os

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from alembic_utils.replaceable_entity import register_entities

from urllib.parse import quote_plus
from urdep.db import Base

from urdep.db.functions import pg_functions
from urdep.db.triggers import pg_triggers

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# Register functions
register_entities(pg_functions)

# Work around bug that causes triggers to attempt to create before their tables
if not os.getenv('SKIP_TRIGGERS'):
    register_entities(pg_triggers)

db_hostname = os.getenv('DB_HOSTNAME')
db_name = os.getenv('DB_NAME', 'urdep')
db_password = os.getenv('DB_PASSWORD')
db_port = int(os.getenv('DB_PORT', 5432))
db_username = os.getenv('DB_USERNAME')
config.set_main_option('sqlalchemy.url', f"postgresql://{db_username}:{quote_plus(db_password)}@{db_hostname}:{db_port}/{db_name}")

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """

    url = f"postgresql://{db_username}:{quote_plus(db_password)}@{db_hostname}:{db_port}/{db_name}"
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
