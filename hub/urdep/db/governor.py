from typing import List, Optional
from uuid import UUID

from sqlalchemy import (
    ForeignKey,
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
from . import NamespacedBaseWithName

class Governor(NamespacedBaseWithName):
    __tablename__ = f"{config.db_name_prefix}governor"
    __table_args__ = NamespacedBaseWithName._table_args(
        comment="governors configure management of subjects",
        tablename=__tablename__,
    )

    provision_actuator_uuid: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(f"{config.db_name_prefix}actuator.uuid")
    )
    provision_actuator: Mapped[Optional["Actuator"]] = relationship(
        foreign_keys=[provision_actuator_uuid],
    )

    start_actuator_uuid: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(f"{config.db_name_prefix}actuator.uuid")
    )
    start_actuator: Mapped[Optional["Actuator"]] = relationship(
        foreign_keys=[start_actuator_uuid],
    )

    stop_actuator_uuid: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(f"{config.db_name_prefix}actuator.uuid")
    )
    stop_actuator: Mapped[Optional["Actuator"]] = relationship(
        foreign_keys=[stop_actuator_uuid],
    )

    status_actuator_uuid: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(f"{config.db_name_prefix}actuator.uuid")
    )
    status_actuator: Mapped[Optional["Actuator"]] = relationship(
        foreign_keys=[status_actuator_uuid],
    )

    destroy_actuator_uuid: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(f"{config.db_name_prefix}actuator.uuid")
    )
    destroy_actuator: Mapped[Optional["Actuator"]] = relationship(
        foreign_keys=[destroy_actuator_uuid],
    )

    meta: Mapped[Optional[JSONB]] = mapped_column(JSONB)
    vars: Mapped[Optional[JSONB]] = mapped_column(JSONB)

    components: Mapped[List["GovernorComponent"]] = relationship(
        back_populates="governor",
        passive_deletes=True,
        foreign_keys="GovernorComponent.governor_uuid",
    )

    parameters: Mapped[List["GovernorParameter"]] = relationship(
        back_populates="governor",
    )

    subjects: Mapped[List["Subject"]] = relationship(
        back_populates="governor",
    )
