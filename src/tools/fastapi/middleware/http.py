import json
import re
from typing import Union

from fastapi import Request
from fastapi import status
from fastapi.responses import StreamingResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp

EXCLUDE_PATHS = {
    r".+\/-/liveness",
    r".+\/-/readiness",
    r".+\/docs",
    r".+\/redoc",
    r".+\/openapi.json",
    r".+\/favicon.ico",
}


class HTTPMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        exclude_paths: list[str],
        logger=None,
    ) -> None:
        super().__init__(app)
        self.app = app
        self.exclude_paths = exclude_paths
        self.logger = logger

    async def dispatch(self, request: Request, call_next) -> Response:
        if self.exclude_paths:
            matches = next((path for path in self.exclude_paths if re.match(path, str(request.url))), None)
            if matches:
                return await call_next(request)

        return await self.handle(request, call_next)

    async def handle(self, request: Request, call_next) -> Response:  # noqa:C901
        context = self.context(request)

        if request.method in {"PATCH", "POST", "PUT"}:
            context["body"] = await self.parse_body(request)

        await self.logger.info(f"HTTP Request: {request.method.upper()} {str(request.url)}", **context)

        try:
            response = await call_next(request)
        except Exception as e:
            context["code"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            await self.logger.error(f"HTTP Error: {request.method.upper()} {str(request.url)}", **context)
            raise e

        content = await self.parse_response(response)

        context["response"] = content

        context["code"] = response.status_code

        await self.logger.info(f"HTTP Response: {request.method.upper()} {str(request.url)}", **context)

        return Response(
            content=content,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )

    @classmethod
    def context(cls, request: Request) -> dict:
        headers = dict(request.headers.items())

        hidden = [
            "authorization",
        ]
        for key in hidden:
            if headers.get(key, None):
                headers[key] = "*"

        return {
            "version": request.scope["http_version"],
            "ip": f"{request.client.host}:{request.client.port}",
            "method": request.method,
            "url": str(request.url),
            "headers": headers,
            "query": dict(request.query_params),
            "body": {},
            "response": {},
        }

    @classmethod
    async def parse_body(cls, request: Request) -> Union[str, bytes]:
        async def __receive() -> dict:
            return {"type": "http.request", "body": body}

        body: bytes = await request.body()

        request._receive = __receive

        payload = body
        if not payload:
            return payload

        if request.headers.get("Content-Type") == "application/json":
            try:
                payload = json.loads(body.decode("utf-8").replace("\n", ""))
            except json.JSONDecodeError:
                # FastAPI - сам по стеку поднимет 422 Error: Unprocessable Entity
                ...

        return payload

    @classmethod
    async def parse_response(cls, response: StreamingResponse) -> Union[bytes, str]:
        content = b""
        async for chunk in response.body_iterator:
            content += chunk
        try:
            return content.decode("utf-8")
        except UnicodeDecodeError:
            return content
