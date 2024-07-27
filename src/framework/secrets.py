from src.tools.jwt import JWT

from .settings import settings

jwt = JWT(
    key=settings.JWT_SECRET_KEY,
    algorithm=settings.JWT_ALGORITHM,
    access_expired_seconds=settings.JWT_ACCESS_EXPIRED_SECONDS,
    refresh_expired_seconds=settings.JWT_REFRESH_EXPIRED_SECONDS,
)
