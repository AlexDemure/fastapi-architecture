from typing import Self

from pydantic import BaseModel

from src.domain import models
from src.endpoints.http.schemas import Created


class GetDummyResponse(BaseModel):
    id: int

    @classmethod
    def serialize(cls, item: models.Dummy) -> Self:
        return cls(id=item.id)


class PostDummyResponse(Created):
    id: int


class GetDummyDocumentResponse(BaseModel):
    id: str

    @classmethod
    def serialize(cls, item: models.DummyDocument) -> Self:
        return cls(id=item.id)


class PostDummyDocumentResponse(Created):
    id: str
