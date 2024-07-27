from pydantic import BaseModel

from .enums import TokenPurpose


class Token(BaseModel):
    access: str
    refresh: str


class TokenStructure(BaseModel):
    sub: str
    purpose: TokenPurpose
    exp: int
    jti: str
