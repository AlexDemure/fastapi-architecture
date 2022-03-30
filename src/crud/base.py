from typing import Generic, Optional, Type

from src.models.base import ModelType
from src.schemas.base import CreateSchemaType, UpdateSchemaType


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def create(self, data: CreateSchemaType) -> ModelType:
        return await self.model.create(**data.dict())

    async def get(self, object_id: int) -> Optional[ModelType]:
        return await self.model.get_or_none(id=object_id)

    async def update(self, data: UpdateSchemaType) -> None:
        object_model = await self.model.filter(id=data.id).first()
        for key, value in data.updated_fields.items():
            setattr(object_model, key, value)

        await object_model.save(update_fields=data.updated_fields.keys())

    async def remove(self, object_id: int) -> None:
        await self.model.filter(id=object_id).delete()
