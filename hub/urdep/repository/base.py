from typing import TypeVar, Type, Generic

from sqlalchemy import select, update, delete

from ..db import Base, session
from core.repository.enum import SynchronizeSessionEnum

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepo(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_by_uuid(self, uuid: int) -> ModelType | None:
        query = select(self.model).where(self.model.uuid == uuid)
        return await session.execute(query).scalars().first()

    async def update_by_uuid(
        self,
        uuid: int,
        params: dict,
        synchronize_session: SynchronizeSessionEnum = False,
    ) -> None:
        query = (
            update(self.model)
            .where(self.model.uuid == uuid)
            .values(**params)
            .execution_options(synchronize_session=synchronize_session)
        )
        await session.execute(query)

    async def delete(self, model: ModelType) -> None:
        await session.delete(model)

    async def delete_by_uuid(
        self,
        uuid: int,
        synchronize_session: SynchronizeSessionEnum = False,
    ) -> None:
        query = (
            delete(self.model)
            .where(self.model.uuid == uuid)
            .execution_options(synchronize_session=synchronize_session)
        )
        await session.execute(query)

    async def save(self, model: ModelType) -> ModelType:
        saved = await session.add(model)
        return saved
