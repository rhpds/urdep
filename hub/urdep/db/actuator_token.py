from sqlalchemy_utils import StringEncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine
from sqlalchemy import (
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from ..config import config
from . import GlobalBaseWithName

class ActuatorToken(GlobalBaseWithName):
    __tablename__ = f"{config.db_name_prefix}actuator_token"
    __table_args__ = GlobalBaseWithName._table_args(
        comment="Actuator access token for API access",
    )

    token: Mapped[str] = mapped_column(
        StringEncryptedType(String, config.db_encryption_key, AesEngine, 'pkcs5', length=255),
        comment="Encrypted token value for use by actuator",
        index=True,
        nullable=False,
        unique=True,
    )
