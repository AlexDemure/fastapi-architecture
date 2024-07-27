from datetime import datetime
from datetime import timedelta
from uuid import uuid4

import jwt

from .enums import TokenPurpose
from .exceptions import JWTError
from .schemas import Token
from .schemas import TokenStructure


class JWT:
    key: str = None
    algorithm: str = None
    access_expired_seconds: int = None
    refresh_expired_seconds: int = None

    def __init__(self, key: str, algorithm: str, access_expired_seconds: int, refresh_expired_seconds: int) -> None:
        self.key = key
        self.algorithm = algorithm
        self.access_expired_seconds = access_expired_seconds
        self.refresh_expired_seconds = refresh_expired_seconds

    def generate(self, subject: str) -> Token:
        now = datetime.utcnow()

        jwt_identifier = str(uuid4())

        return Token(
            access=jwt.encode(
                dict(
                    sub=subject,
                    purpose=TokenPurpose.access.value,
                    exp=now + timedelta(seconds=self.access_expired_seconds),
                    jti=jwt_identifier,
                ),
                self.key,
                algorithm=self.algorithm,
            ),
            refresh=jwt.encode(
                dict(
                    sub=subject,
                    purpose=TokenPurpose.refresh.value,
                    exp=now + timedelta(seconds=self.access_expired_seconds),
                    jti=jwt_identifier,
                ),
                self.key,
                algorithm=self.algorithm,
            ),
        )

    def decode(self, token: str, purpose: TokenPurpose) -> TokenStructure:
        try:
            token_structure = TokenStructure(
                **jwt.decode(
                    token,
                    key=self.key,
                    algorithms=[self.algorithm],
                )
            )
            if token_structure.purpose is not purpose:
                raise jwt.PyJWTError("JWT purpose is wrong")
        except jwt.PyJWTError:
            raise JWTError

        return token_structure
