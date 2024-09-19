from . import BaseWithName, Database

class ActuatorToken(BaseWithName):
    __tablename__ = f"{Database.db_name_prefix}actuator_token"
    __table_args__ = BaseWithName._table_args(
        comment="Actuator access token for API access",
    )
