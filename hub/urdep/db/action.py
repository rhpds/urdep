from datetime import datetime
from typing import Literal, Optional, get_args
from uuid import UUID

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Text,
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

ActionKind = Literal[
    "provision",
    "start",
    "stop",
    "status",
    "destroy",
]

ActionState = Literal[
    "new",        # Action is newly created and no processing has begun
    "waiting",    # Action waiting for linked subject or other condition
    "pending",    # Action waiting for actuator
    "running",    # Actuator is handling action
    "failed",     # Actuator reported failure for action
    "successful", # Action completed successfully
]

class Action(BaseWithNamespacedName):
    __tablename__ = f"{Database.db_name_prefix}action"
    __table_args__ = BaseWithNamespacedName._table_args(
        comment="actions represent provisoning and lifecycle activities for a subject",
        tablename=__tablename__,
    )

    actuator_uuid: Mapped[UUID] = mapped_column(
        ForeignKey(f"{Database.db_schema}.{Database.db_name_prefix}actuator.uuid", ondelete='CASCADE'),
        comment="actuator responsible for this action",
    )
    subject_uuid: Mapped[UUID] = mapped_column(
        ForeignKey(f"{Database.db_schema}.{Database.db_name_prefix}subject.uuid", ondelete='CASCADE'),
        comment="subject of this action",
    )

    meta: Mapped[Optional[JSONB]] = mapped_column(JSONB)
    vars: Mapped[Optional[JSONB]] = mapped_column(JSONB)
    actuator_data: Mapped[Optional[JSONB]] = mapped_column(JSONB)
    data: Mapped[Optional[JSONB]] = mapped_column(JSONB)
    messages: Mapped[Optional[str]] = mapped_column(Text)

    kind: Mapped[ActionKind] = mapped_column(
        Enum(
            *get_args(ActionKind),
            name=f"{Database.db_name_prefix}action_kind",
            create_constraint=True,
            inherit_schema=True,
            validate_strings=True,
        ),
    )

    action_state: Mapped[ActionState] = mapped_column(
        Enum(
            *get_args(ActionState),
            name=f"{Database.db_name_prefix}action_state",
            create_constraint=True,
            inherit_schema=True,
            validate_strings=True,
        ),
        server_default="new",
    )

    began: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        comment="when action handling began",
    )
    completed: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        comment="when action handling completed",
    )
