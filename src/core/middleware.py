from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from structlog import get_logger


async def test_middleware(request: Request, call_next: RequestResponseEndpoint) -> Response:
    logger = get_logger()

    logger.debug(f"Request URL: {request.url}")
    return await call_next(request)


utils = [
    Middleware(BaseHTTPMiddleware, dispatch=test_middleware),
]
