from typing import List

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from ..config import config
from . import GlobalBaseWithName

class Actuator(GlobalBaseWithName):
    __tablename__ = f"{config.db_name_prefix}actuator"
    __table_args__ = GlobalBaseWithName._table_args(
        comment="Actuators are configured by governors to perform actions for subjects",
    )

    actions: Mapped[List["Action"]] = relationship(
        back_populates="actuator",
    )

    @classmethod
    def create(cls, name: str):
        return cls(
            name=name,
        )
