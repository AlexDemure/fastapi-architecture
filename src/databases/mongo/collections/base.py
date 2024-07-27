from typing import TypeVar

from motor.motor_asyncio import AsyncIOMotorCollection

CollectionType = TypeVar("CollectionType", bound=AsyncIOMotorCollection)
