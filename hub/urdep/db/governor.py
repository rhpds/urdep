from typing import List, Optional
from uuid import UUID

from sqlalchemy import (
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.dialects.postgresql import(
    JSONB,
)

from . import BaseWithNamespacedName, Database

class Governor(BaseWithNamespacedName):
    __tablename__ = f"{Database.db_name_prefix}governor"
    __table_args__ = BaseWithNamespacedName._table_args(
        comment="governors configure management of subjects",
        tablename=__tablename__,
    )

    provision_actuator_uuid: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(f"{Database.db_schema}.{Database.db_name_prefix}actuator.uuid")
    )
    provision_actuator: Mapped[Optional["Actuator"]] = relationship()

    start_actuator_uuid: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(f"{Database.db_schema}.{Database.db_name_prefix}actuator.uuid")
    )
    start_actuator: Mapped[Optional["Actuator"]] = relationship()

    stop_actuator_uuid: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(f"{Database.db_schema}.{Database.db_name_prefix}actuator.uuid")
    )
    stop_actuator: Mapped[Optional["Actuator"]] = relationship()

    status_actuator_uuid: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(f"{Database.db_schema}.{Database.db_name_prefix}actuator.uuid")
    )
    status_actuator: Mapped[Optional["Actuator"]] = relationship()

    destroy_actuator_uuid: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(f"{Database.db_schema}.{Database.db_name_prefix}actuator.uuid")
    )
    destroy_actuator: Mapped[Optional["Actuator"]] = relationship()

    meta: Mapped[Optional[JSONB]] = mapped_column(JSONB)
    vars: Mapped[Optional[JSONB]] = mapped_column(JSONB)

    components: Mapped[List["GovernorComponent"]] = relationship(
        backref="governor",
        passive_deletes=True,
    )

    linked_by_components: Mapped[List["GovernorComponent"]] = relationship(
        backref="linked_governor",
    )

    subjects: Mapped[List["Subject"]] = relationship(
        backref="governor",
    )
