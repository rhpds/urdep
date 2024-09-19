from typing import Literal, get_args
from uuid import UUID

from sqlalchemy import (
    Enum,
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from . import Base, Database

GovernorComponentActionHandling = Literal[
    "before",   # Pass action handling to the linked governor before handling
    "after",    # Pass action handling to the linked governor after handling
    "delegate", # Pass action handling to the linked governor instead of handling
    "disable",  # Do not pass action handling to linked governor
]

class GovernorComponent(Base):
    __tablename__ = f"{Database.db_schema}.{Database.db_name_prefix}governor_component"

    governor_uuid: Mapped[UUID] = mapped_column(
        ForeignKey(f"{Database.db_schema}.{Database.db_name_prefix}governor.uuid", ondelete='CASCADE')
    )

    linked_governor_uuid: Mapped[UUID] = mapped_column(
        ForeignKey(f"{Database.db_schema}.{Database.db_name_prefix}governor.uuid")
    )
    
    provision_handling: Mapped[GovernorComponentActionHandling] = mapped_column(
        Enum(
            *get_args(GovernorComponentActionHandling),
            name=f"{Database.db_name_prefix}governor_component_action_handling",
            create_constraint=True,
            inherit_schema=True,
            validate_strings=True,
        )
    )

    start_handling: Mapped[GovernorComponentActionHandling] = mapped_column(
        Enum(
            *get_args(GovernorComponentActionHandling),
            name=f"{Database.db_name_prefix}governor_component_action_handling",
            create_constraint=True,
            inherit_schema=True,
            validate_strings=True,
        )
    )

    stop_handling: Mapped[GovernorComponentActionHandling] = mapped_column(
        Enum(
            *get_args(GovernorComponentActionHandling),
            name=f"{Database.db_name_prefix}governor_component_action_handling",
            create_constraint=True,
            inherit_schema=True,
            validate_strings=True,
        )
    )

    status_handling: Mapped[GovernorComponentActionHandling] = mapped_column(
        Enum(
            *get_args(GovernorComponentActionHandling),
            name=f"{Database.db_name_prefix}governor_component_action_handling",
            create_constraint=True,
            validate_strings=True,
        )
    )

    destroy_handling: Mapped[GovernorComponentActionHandling] = mapped_column(
        Enum(
            *get_args(GovernorComponentActionHandling),
            name=f"{Database.db_name_prefix}governor_component_action_handling",
            create_constraint=True,
            validate_strings=True,
        )
    )

GovernorComponent.__table_args__ = GovernorComponent._table_args(
    comment="Assocation of governors which reference others as components",
)
