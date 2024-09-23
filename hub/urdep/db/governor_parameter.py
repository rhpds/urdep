from typing import Optional
from uuid import UUID

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    String,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import(
    JSONB,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from ..config import config
from . import NamespacedBase

class GovernorParameter(NamespacedBase):
    __tablename__ = f"{config.db_name_prefix}governor_parameter"
    __table_args__ = NamespacedBase._table_args(
        CheckConstraint(r"(name ~ '^[A-Za-z_]([A-Za-z0-9_]*[A-Za-z0-9_])?$')", name="name_format"),
        UniqueConstraint('governor_uuid', 'name', name=f"{__tablename__}_name"),
        comment="parameter supported by a governor",
    )

    governor_uuid: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(f"{config.db_name_prefix}governor.uuid")
    )
    governor: Mapped[Optional["Governor"]] = relationship(
        foreign_keys=[governor_uuid],
    )

    name: Mapped[str] = mapped_column(String(255),
        comment="Unique parameter name for governor",
    )

    default: Mapped[Optional[JSONB]] = mapped_column(JSONB)
    openapi_schema: Mapped[Optional[JSONB]] = mapped_column(JSONB)
    required: Mapped[bool] = mapped_column(default=False, server_default=text("FALSE"))
