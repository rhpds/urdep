from datetime import datetime
from typing import List, Literal, Optional, get_args
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

from ..config import config
from . import NamespacedBaseWithName

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

class Action(NamespacedBaseWithName):
    __tablename__ = f"{config.db_name_prefix}action"
    __table_args__ = NamespacedBaseWithName._table_args(
        comment="actions represent provisoning and lifecycle activities for a subject",
        tablename=__tablename__,
    )

    actuator_uuid: Mapped[UUID] = mapped_column(
        ForeignKey(f"{config.db_name_prefix}actuator.uuid", ondelete='CASCADE'),
        comment="actuator responsible for this action",
    )
    actuator: Mapped["Actuator"] = relationship(
        back_populates="actions",
    )

    parent_uuid: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey(f"{config.db_name_prefix}action.uuid"),
        comment="link to parent action if processing as a component of another action",
    )
    parent: Mapped[Optional["Action"]] = relationship(
        back_populates="children",
        remote_side="Action.uuid",
    )
    children: Mapped[List["Action"]] = relationship(
        back_populates="parent",
    )

    subject_uuid: Mapped[UUID] = mapped_column(
        ForeignKey(f"{config.db_name_prefix}subject.uuid", ondelete='CASCADE'),
        comment="subject of this action",
    )
    subject: Mapped["Subject"] = relationship(
        back_populates="actions",
    )

    meta: Mapped[Optional[JSONB]] = mapped_column(JSONB)
    vars: Mapped[Optional[JSONB]] = mapped_column(JSONB)
    actuator_data: Mapped[Optional[JSONB]] = mapped_column(JSONB)
    data: Mapped[Optional[JSONB]] = mapped_column(JSONB)
    messages: Mapped[Optional[str]] = mapped_column(Text)

    kind: Mapped[ActionKind] = mapped_column(
        Enum(
            *get_args(ActionKind),
            name=f"{config.db_name_prefix}action_kind",
            create_constraint=True,
            validate_strings=True,
        ),
    )

    action_state: Mapped[ActionState] = mapped_column(
        Enum(
            *get_args(ActionState),
            name=f"{config.db_name_prefix}action_state",
            create_constraint=True,
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
