from typing import List

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from . import BaseWithName, Database

class Actuator(BaseWithName):
    __tablename__ = f"{Database.db_name_prefix}actuator"
    __table_args__ = BaseWithName._table_args(
        comment="Actuators are configured by governors to perform actions for subjects",
    )

    actions: Mapped[List["Action"]] = relationship(
        backref="actuator",
    )
