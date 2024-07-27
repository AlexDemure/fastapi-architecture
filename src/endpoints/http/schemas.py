from typing import Any
from typing import Self
from typing import Union

from pydantic import BaseModel
from pydantic import conint
from pydantic import conlist

from src.domain import models


class Created(BaseModel):
    id: Union[int, str]

    @classmethod
    def serialize(cls, item: models.Model) -> Self:
        return cls(id=item.id)


class Update(BaseModel):
    @property
    def deserialize(self) -> dict:
        return self.dict(exclude_defaults=True)


class Search(BaseModel):
    class Filter(BaseModel):
        field: str
        value: Union[int, str, list]

    class Sorting(BaseModel):
        field: str
        type: str

    class Pagination(BaseModel):
        page: conint(gt=0, le=1000) = 1
        size: conint(gt=0, le=100) = 10

        @property
        def deserialize(self) -> dict:
            return dict(limit=self.size, offset=(self.page - 1) * self.size if self.page > 0 else 0)

    filters: conlist(Filter) = []
    sorting: conlist(Sorting) = []
    pagination: Pagination = Pagination()

    @property
    def deserialize(self) -> dict:
        return dict(
            filters=[dict(item) for item in self.filters],
            sorting=[dict(item) for item in self.sorting],
            pagination=self.pagination.deserialize,
        )


class Paginated(BaseModel):
    total: int
    items: list[Any]
