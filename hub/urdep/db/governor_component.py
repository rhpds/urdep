from typing import Literal, get_args
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    Enum,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from ..config import config
from . import NamespacedBase

GovernorComponentActionHandling = Literal[
    "before",   # Pass action handling to the linked governor before handling
    "after",    # Pass action handling to the linked governor after handling
    "delegate", # Pass action handling to the linked governor instead of handling
    "disable",  # Do not pass action handling to linked governor
]

class GovernorComponent(NamespacedBase):
    __tablename__ = f"{config.db_name_prefix}governor_component"
    __table_args__ = NamespacedBase._table_args(
        CheckConstraint(r"(name ~ '^[A-Za-z_]([A-Za-z0-9_]*[A-Za-z0-9_])?$')", name="name_format"),
        UniqueConstraint('governor_uuid', 'name', name=f"{__tablename__}_name"),
        comment="Assocation of governors which reference others as components",
    )

    governor_uuid: Mapped[UUID] = mapped_column(
        ForeignKey(f"{config.db_name_prefix}governor.uuid", ondelete='CASCADE')
    )
    governor: Mapped["Governor"] = relationship(
        back_populates="components",
        foreign_keys=[governor_uuid],
    )

    linked_governor_uuid: Mapped[UUID] = mapped_column(
        ForeignKey(f"{config.db_name_prefix}governor.uuid")
    )
    linked_governor: Mapped["Governor"] = relationship(
        foreign_keys=[linked_governor_uuid],
    )

    name: Mapped[str] = mapped_column(String(255),
        comment="Unique component name from governor",
    )
    
    provision_handling: Mapped[GovernorComponentActionHandling] = mapped_column(
        Enum(
            *get_args(GovernorComponentActionHandling),
            name=f"{config.db_name_prefix}governor_component_action_handling",
            create_constraint=True,
            validate_strings=True,
        )
    )

    start_handling: Mapped[GovernorComponentActionHandling] = mapped_column(
        Enum(
            *get_args(GovernorComponentActionHandling),
            name=f"{config.db_name_prefix}governor_component_action_handling",
            create_constraint=True,
            validate_strings=True,
        )
    )

    stop_handling: Mapped[GovernorComponentActionHandling] = mapped_column(
        Enum(
            *get_args(GovernorComponentActionHandling),
            name=f"{config.db_name_prefix}governor_component_action_handling",
            create_constraint=True,
            validate_strings=True,
        )
    )

    status_handling: Mapped[GovernorComponentActionHandling] = mapped_column(
        Enum(
            *get_args(GovernorComponentActionHandling),
            name=f"{config.db_name_prefix}governor_component_action_handling",
            create_constraint=True,
            validate_strings=True,
        )
    )

    destroy_handling: Mapped[GovernorComponentActionHandling] = mapped_column(
        Enum(
            *get_args(GovernorComponentActionHandling),
            name=f"{config.db_name_prefix}governor_component_action_handling",
            create_constraint=True,
            validate_strings=True,
        )
    )
