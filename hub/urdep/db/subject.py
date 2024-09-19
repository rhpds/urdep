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

from . import BaseWithNamespacedName, Database

SubjectDesiredState = Literal[
    "started",
    "stopped",
    "destroyed",
]

SubjectCurrentState = Literal[
    "new",               # Subject is newly created and no processing has begun
    "provision-waiting", # Provision action waiting for linked subject or other condition
    "provision-pending", # Provision action created and waiting for actuator
    "provisioning",      # Actuator is handling provision action
    "provision-failed",  # Actuator reported failure to provision
    "start-waiting",     # Start action waiting for linked subject or other condition
    "start-pending",     # Start action has been created and is waiting for actuator
    "starting",          # Actuator is handling start action
    "start-failed",      # Actuator reported failure to start
    "started",           # Started as a result of successful provision or start action
    "stop-waiting",      # Stop action waiting for linked subject or other condition
    "stop-pending",      # Stop action created and waiting for actuator
    "stopping",          # Actuator is handling stop action
    "stop-failed",       # Actuator reported failure to stop
    "stopped",           # Stopped as result of successful stop action
    "destroy-waiting",   # Destroy action waiting for linked subject or other condition
    "destroy-pending",   # Destroy action created and waiting for actuator
    "destroying",        # Actuator is handling destroy action
    "destroy-failed",    # Actuator reported failure to destroy
    "destroyed"          # Successfully destroyed
]

class Subject(BaseWithNamespacedName):
    __tablename__ = f"{Database.db_name_prefix}subject"
    __table_args__ = BaseWithNamespacedName._table_args(
        comment="subjects represent anything managed by an actuator",
        tablename=__tablename__,
    )

    governor_uuid: Mapped[UUID] = mapped_column(
        ForeignKey(f"{Database.db_schema}.{Database.db_name_prefix}governor.uuid"),
        comment="governor configures how the subject is managed",
    )

    meta: Mapped[Optional[JSONB]] = mapped_column(JSONB)
    parameters: Mapped[Optional[JSONB]] = mapped_column(JSONB)
    vars: Mapped[Optional[JSONB]] = mapped_column(JSONB)

    actions: Mapped[List["Action"]] = relationship(
        backref="subject",
        passive_deletes=True,
    )

    current_state: Mapped[SubjectCurrentState] = mapped_column(
        Enum(
            *get_args(SubjectCurrentState),
            name=f"{Database.db_name_prefix}subject_current_state",
            create_constraint=True,
            inherit_schema=True,
            validate_strings=True,
        ),
        server_default="new",
    )

    desired_state: Mapped[SubjectDesiredState] = mapped_column(
        Enum(
            *get_args(SubjectDesiredState),
            name=f"{Database.db_name_prefix}subject_desired_state",
            create_constraint=True,
            inherit_schema=True,
            validate_strings=True,
        ),
        server_default="started",
    )

    provision_began: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        comment="when provision handling began",
    )
    provision_completed: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        comment="when provision completed",
    )
    provision_data: Mapped[Optional[JSONB]] = mapped_column(JSONB)
    provision_messages: Mapped[Optional[str]] = mapped_column(Text)

    start_began: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        comment="when last start handling began",
    )
    start_completed: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        comment="when last start completed",
    )
    start_data: Mapped[Optional[JSONB]] = mapped_column(JSONB)
    start_messages: Mapped[Optional[str]] = mapped_column(Text)

    stop_began: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        comment="when last stop handling began",
    )
    stop_completed: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        comment="when last stop completed",
    )
    stop_data: Mapped[Optional[JSONB]] = mapped_column(JSONB)
    stop_messages: Mapped[Optional[str]] = mapped_column(Text)

    status_began: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        comment="when last status handling began",
    )
    status_completed: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        comment="when last status completed",
    )
    status_data: Mapped[Optional[JSONB]] = mapped_column(JSONB)
    status_messages: Mapped[Optional[str]] = mapped_column(Text)

    destroy_began: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        comment="when last destroy attempt began",
    )
    destroy_completed: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        comment="when last destroy attempt completed",
    )
    destroy_data: Mapped[Optional[JSONB]] = mapped_column(JSONB)
    destroy_messages: Mapped[Optional[str]] = mapped_column(Text)
