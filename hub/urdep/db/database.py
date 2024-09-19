import logging
import os

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from urllib.parse import quote_plus

logger = logging.getLogger('urdep')

class Database():
    db_hostname = os.getenv('DB_HOSTNAME')
    db_max_overflow = int(os.getenv('DB_MAX_OVERFLOW', 30))
    db_name = os.getenv('DB_NAME', 'urdep')
    db_name_prefix = os.getenv('DB_NAME_PREFIX', 'urdep_')
    db_password = os.getenv('DB_PASSWORD')
    db_pool_recycle = int(os.getenv('DB_POOL_RECYCLE', 600))
    db_pool_size = int(os.getenv('DB_POOL_SIZE', 5))
    db_pool_size = int(os.getenv('DB_POOL_SIZE', 5))
    db_pool_timeout = int(os.getenv('DB_POOL_TIMEOUT', 45))
    db_port = int(os.getenv('DB_PORT', 5432))
    db_schema = os.getenv('DB_SCHEMA', 'public')
    db_username = os.getenv('DB_USERNAME')
    db_url = f"postgresql+asyncpg://{db_username}:{quote_plus(db_password)}@{db_hostname}:{db_port}/{db_name}"

    @classmethod
    async def on_startup(cls):
        cls.engine = create_async_engine(cls.db_url,
            pool_pre_ping=True,
            pool_size=cls.db_pool_size,
            max_overflow=cls.db_max_overflow,
            pool_recycle=cls.db_pool_recycle,
            pool_timeout=cls.db_pool_timeout,
            future=True,
            echo=False,
        )

    #@classmethod
    #@asynccontextmanager
    #async def get_session(cls) -> AsyncSession:
    #    await cls.wait_for_pool()

    #    session = cls.async_session()
    #    try:
    #        yield session
    #        await session.commit()
    #    except Exception as e:
    #        await session.rollback()
    #        raise e
    #    finally:
    #        await session.close()



#    db_version = semver.Version.parse("0.1.0")
#    pool = None
#    pgsql_pool_max = int(os.environ.get('PGSQL_POOL_MAX', 6))
#    pgsql_pool_min = int(os.environ.get('PGSQL_POOL_MIN', 3))
#    db_name_prefix = os.environ.get('TABLE_NAME_PREFIX', 'urdep_')
#
#    action_table_name = f"{db_name_prefix}action"
#    actuator_table_name = f"{db_name_prefix}actuator"
#    config_table_name = f"{db_name_prefix}config"
#    governor_table_name = f"{db_name_prefix}governor"
#    governor_linked_component_table_name = f"{db_name_prefix}governor_linked_component"
#    subject_table_name = f"{db_name_prefix}subject"
#
#    @classmethod
#    async def create_functions(cls):
#        for path in (pathlib.Path(__file__).parent / 'db').iterdir():
#            if path.name.startswith('create_function_') and path.name.endswith('.sql'):
#                name = cls.db_name_prefix + path.name[16:-4]
#                await cls.create_function_from_file(path, name)
#
#    @classmethod
#    async def create_tables(cls):
#        items = []
#        for path in (pathlib.Path(__file__).parent / 'db').iterdir():
#            match = re.match(r'(\d+)_create_table_(\w+)\.sql$', path.name)
#            if match:
#                priority = int(match.group(1))
#                name = cls.db_name_prefix + match.group(2)
#                items.append((priority, name, path))
#        items.sort(key=lambda x: x[0])
#        for item in items:
#            name = item[1]
#            path = item[2]
#            await cls.create_table_from_file(path, name)
#
#    @classmethod
#    async def create_triggers(cls):
#        for path in (pathlib.Path(__file__).parent / 'db').iterdir():
#            if path.name.startswith('create_trigger_') and path.name.endswith('.sql'):
#                name = cls.db_name_prefix + path.name[15:-4]
#                await cls.create_trigger_from_file(path, name)
#
#    @classmethod
#    async def create_types(cls):
#        for path in (pathlib.Path(__file__).parent / 'db').iterdir():
#            if path.name.startswith('create_type_') and path.name.endswith('.sql'):
#                name = cls.db_name_prefix + path.name[12:-4]
#                await cls.create_type_from_file(path, name)
#
#    @classmethod
#    async def create_function_from_file(cls, filename: str, name: str):
#        logger.info(f"Creating function {name}")
#        await cls.execute_sql_from_file(filename)
#
#    @classmethod
#    async def create_table_from_file(cls, filename: str, name: str):
#        logger.info(f"Creating table {name}")
#        try:
#            await cls.execute_sql_from_file(filename)
#        except psycopg.errors.DuplicateTable:
#            logger.warning(f"Table {name} already exists")
#
#    @classmethod
#    async def create_trigger_from_file(cls, filename: str, name: str):
#        logger.info(f"Creating trigger {name}")
#        await cls.execute_sql_from_file(filename)
#
#    @classmethod
#    async def create_type_from_file(cls, filename: str, name: str):
#        logger.info(f"Creating type {name}")
#        try:
#            await cls.execute_sql_from_file(filename)
#        except psycopg.errors.DuplicateObject:
#            logger.warning(f"Type {name} already exists")
#
#    @classmethod
#    async def set_db_version(cls):
#        async with cls.pool.connection() as conn:
#            async with conn.cursor() as cur:
#                await cur.execute(
#                    f"INSERT INTO {cls.config_table_name} (name, value) "
#                    f"VALUES ('version', %s)"
#                    f"ON CONFLICT (name) DO UPDATE SET value=%s",
#                    (str(cls.db_version), str(cls.db_version))
#                )
#
#    @classmethod
#    async def dbinit(cls):
#        cls.pool = AsyncConnectionPool(cls.pgsql_conn_str(),
#            max_size=cls.pgsql_pool_max,
#            min_size=cls.pgsql_pool_min,
#            open=False,
#        )
#        await cls.pool.open()
#        current_db_version = await cls.get_db_version()
#        if current_db_version == None:
#            await cls.create_types()
#            await cls.create_tables()
#            await cls.create_functions()
#            await cls.create_triggers()
#            await cls.set_db_version()
#            logger.info(f"Current DB version initialized as {cls.db_version}")
#        elif current_db_version != cls.db_version:
#            await cls.upgrade_tables(current_db_version)
#            logger.info(f"Current DB version upgrade to {cls.db_version}")
#        else:
#            logger.info(f"Current DB version is {cls.db_version}")
#            await cls.create_types()
#            await cls.create_tables()
#            await cls.create_functions()
#            await cls.create_triggers()
#
#
#    @classmethod
#    async def execute_sql_from_file(cls, filename: str):
#        path = pathlib.Path(__file__).parent / filename
#        with open(path) as fh:
#            sql = fh.read()
#            # Replace table names
#            sql = re.sub(r' urdep_', f" {cls.db_name_prefix}", sql)
#            async with cls.pool.connection() as conn:
#                async with conn.cursor() as cur:
#                    await cur.execute(sql)
#
#    @classmethod
#    async def get_db_version(cls):
#        async with cls.pool.connection() as conn:
#            async with conn.cursor() as cur:
#                try:
#                    await cur.execute(f"SELECT value FROM {cls.config_table_name} WHERE name='version'")
#                    ret = await cur.fetchone()
#                    if not ret:
#                        return None
#                    return semver.Version.parse(ret[0])
#                except psycopg.errors.UndefinedTable:
#                    return None
#
#    @classmethod
#    async def upgrade_tables(cls, current_db_version):
#        """Upgrade tables as necessary from current version."""
#        logger.info(f"Upgrading database tables from {current_db_version} to {cls.db_version}")
#        raise Exception("FIXME - VERSION UPGRADE IMPLEMENTED")
