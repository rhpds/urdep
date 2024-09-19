from datetime import datetime
from sqlalchemy import (
    CheckConstraint,
    DateTime,
    String,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)
from uuid import UUID

from .database import Database

class Base(DeclarativeBase):
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
                "schema": Database.db_schema,
                **kwargs,
            }
        )

class BaseWithName(Base):
    __abstract__ = True

    name: Mapped[str] = mapped_column(String(255),
        comment="Unique name",
        index=True,
        nullable=False,
        unique=True,
    )

    @classmethod
    def _table_args(cls, *args, **kwargs):
        return (
            CheckConstraint(r"(name ~ '^[A-Za-z]([A-Za-z0-9\-.]*[A-Za-z0-9])?$')", name="name_format"),
            {
                "schema": Database.db_schema,
                **kwargs,
            }
        )

class BaseWithNamespacedName(Base):
    __abstract__ = True

    namespace: Mapped[str] = mapped_column(String(255),
        comment="Namespace for context with name",
        index=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255),
        comment="Unique name within namespace",
        index=True,
        nullable=False,
    )

    @classmethod
    def _table_args(cls, tablename=None, *args, **kwargs):
        return (
            CheckConstraint(r"(namespace ~ '^[A-Za-z]([A-Za-z0-9\-.]*[A-Za-z0-9])?$')", name="namespace_format"),
            CheckConstraint(r"(name ~ '^[A-Za-z]([A-Za-z0-9\-.]*[A-Za-z0-9])?$')", name="name_format"),
            UniqueConstraint('namespace', 'name', name=f"{tablename}_namespace_name"),
            {
                "schema": Database.db_schema,
                **kwargs,
            }
        )
