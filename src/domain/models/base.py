from typing import TypeVar
from typing import Union

from pydantic import BaseModel
from pydantic import ConfigDict

from src.databases.postgres.tables import TableType


class Model(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="allow")

    @classmethod
    def orm(cls, obj: Union[dict, TableType]) -> "Model":
        if isinstance(obj, dict):
            return cls.model_validate({"id": str(obj.pop("_id")), **obj})
        else:
            # from_attributes=True
            return cls.model_validate({k: v for k, v in obj.__dict__.items() if not k.startswith("_")})

    @classmethod
    def init(cls, *args, **kwargs) -> dict:
        raise NotImplementedError


ModelType = TypeVar("ModelType", bound=Model)
