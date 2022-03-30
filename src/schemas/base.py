from typing import TypeVar

from pydantic import BaseModel

CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class UpdatedBase(BaseModel):
    id: int
    updated_fields: dict


class Message(BaseModel):
    msg: str


class DetailError(BaseModel):
    msg: str
    type: str


class MessageErrorSchema(BaseModel):

    detail: DetailError
