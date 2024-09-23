from pydantic import Field
from pydantic_settings import BaseSettings
from urllib.parse import quote_plus

class Config(BaseSettings):
    environment: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8080

    db_encryption_key: str = "urdep"
    db_hostname: str = "localhost"
    db_max_overflow: int = 30
    db_name: str = "urdep"
    db_name_prefix: str = "urdep_"
    db_password: str = "urdep"
    db_pool_recycle: int = 600
    db_pool_size: int = 5
    db_pool_timeout: int = 45
    db_port: int = 5432
    db_username: str = "urdep"
    db_url: str = f"postgresql+asyncpg://{db_username}:{quote_plus(db_password)}@{db_hostname}:{db_port}/{db_name}"

config: Config = Config()
