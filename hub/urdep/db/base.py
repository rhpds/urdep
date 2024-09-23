from datetime import datetime
from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    relationship,
)
from uuid import UUID

from ..config import config

class Base(DeclarativeBase):
    """Generic base which adds standard UUID identifier and creation timestamp."""
    __abstract__ = True

    uuid: Mapped[UUID] = mapped_column(
        comment="Unique identifier",
        primary_key=True,
        server_default=text("GEN_RANDOM_UUID()"),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        comment="Creation timestamp",
        server_default=text("(NOW() AT TIME ZONE 'utc')"),
    )

    @classmethod
    def _table_args(cls, *args, **kwargs):
        return (
            *args,
            {
                **kwargs,
            }
        )

class GlobalBaseWithName(Base):
    """Named global with unique name"""
    __abstract__ = True

    name: Mapped[str] = mapped_column(String(255),
        comment="Unique name",
        index=True,
        unique=True,
    )

    @classmethod
    def _table_args(cls, *args, **kwargs):
        return (
            CheckConstraint(r"(name ~ '^[A-Za-z]([A-Za-z0-9\-.]*[A-Za-z0-9])?$')", name="name_format"),
            {
                **kwargs,
            }
        )

class NamespacedBase(Base):
    """Namespaced resource without a name"""
    __abstract__ = True

    namespace_uuid: Mapped[UUID] = mapped_column(
        ForeignKey(f"{config.db_name_prefix}namespace.uuid"),
        index=True,
    )

    @declared_attr
    def namespace(cls) -> Mapped["namespace"]:
        return relationship("Namespace")

    @classmethod
    def _table_args(cls, *args, **kwargs):
        return (
            *args,
            {
                **kwargs,
            }
        )

class NamespacedBaseWithName(NamespacedBase):
    __abstract__ = True

    namespace_uuid: Mapped[UUID] = mapped_column(
        ForeignKey(f"{config.db_name_prefix}namespace.uuid"),
        index=True,
    )

    @declared_attr
    def namespace(cls) -> Mapped["namespace"]:
        return relationship("Namespace")

    name: Mapped[str] = mapped_column(String(255),
        comment="Unique name within namespace",
        index=True,
    )

    @classmethod
    def _table_args(cls, tablename=None, *args, **kwargs):
        return (
            CheckConstraint(r"(name ~ '^[A-Za-z]([A-Za-z0-9\-.]*[A-Za-z0-9])?$')", name="name_format"),
            UniqueConstraint('namespace_uuid', 'name', name=f"{tablename}_namespace_name"),
            {
                **kwargs,
            }
        )
