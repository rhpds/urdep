from ..config import config
from . import GlobalBaseWithName

class Namespace(GlobalBaseWithName):
    __tablename__ = f"{config.db_name_prefix}namespace"
    __table_args__ = GlobalBaseWithName._table_args(
        comment="namespace for access control and efficient indexing"
    )
