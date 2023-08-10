import json
import logging
import re
from datetime import datetime
from enum import Enum
from typing import Union

from fastapi import Request
from fastapi import Response
from fastapi.responses import StreamingResponse

from app.libs.utils import get_elapsed
from app.libs.utils import get_traceback

EXCLUDE_PATHS = {
    r".+\/live",
    r".+\/ready",
    r".+\/healthcheck",
    r".+\/docs",
    r".+\/openapi.json",
    r".+\/favicon.ico",
}


class Field(str, Enum):
    method = "method"
    query_params = "query_params"
    timestamp = "timestamp"
    levelname = "levelname"
    level = "level"
    url = "url"
    url_mask = "url_mask"
    request_path = "request_path"
    headers = "headers"
    request_data = "request_data"
    response_data = "response_data"
    status_code = "status_code"
    elapsed = "elapsed"

    exception = "exception"
    stacktrace = "stacktrace"

    def __call__(self, value) -> dict:
        return {self.name: value}


class HTTPMiddleware:
    @classmethod
    async def log(cls, event_method: str, event: str, context: dict, logger=None, span=None) -> None:
        if logger:
            await getattr(logger, event_method.lower())(event, **context)

        if span:
            span.add_event(event, attributes={k: str(v) for k, v in context.items()})

    @classmethod
    def init_context(cls, request: Request) -> dict:
        return {
            Field.method: request.method,
            Field.query_params: {k: v for k, v in request.query_params.items()},
            Field.timestamp: datetime.utcnow(),
            Field.levelname: "INFO",
            Field.level: logging.INFO,
            Field.url: request.url,
            Field.url_mask: request.url,
            Field.request_path: request.url.path,
            Field.headers: {k: v for k, v in request.headers.items()},
        }

    @classmethod
    async def parse_body(cls, request: Request) -> Union[str, bytes]:
        async def __receive() -> dict:
            """
            The static result of request._receive that is fired in await request.body().

            Required to be able to view the body from an incoming request, otherwise the application is blocked.
            """
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
                # FastAPI 422 Error: Unprocessable Entity
                ...

        return payload

    @classmethod
    async def parse_response(cls, response: StreamingResponse) -> str:
        content = b""
        async for chunk in response.body_iterator:
            content += chunk
        return content.decode("utf-8")

    @classmethod
    async def _proxy(cls, request: Request, call_next, logger=None, span=None) -> Response:  # noqa:C901
        context = cls.init_context(request)

        if request.method in {"PATCH", "POST", "PUT"}:
            context[Field.request_data] = await cls.parse_body(request)

        await cls.log(
            event_method=context[Field.levelname],
            event=f"HTTP Request {context[Field.url]}",
            context=context,
            logger=logger,
            span=span,
        )

        try:
            response = await call_next(request)
        except Exception as e:
            context[Field.levelname] = "ERROR"
            context[Field.level] = logging.ERROR
            context[Field.exception] = str(e)
            context[Field.stacktrace] = get_traceback(e)
            context["status_code"] = 500
            await cls.log(
                event_method=context[Field.levelname],
                event=f"HTTP Error {context[Field.url]}",
                context=context,
                logger=logger,
                span=span,
            )
            raise e
        finally:
            route = request.scope.get("route", None)
            if route:
                url_mask = f"{request.base_url}{route.path[1:]}"

                context[Field.url_mask] = url_mask

                if span:
                    span.update_name(url_mask)

        content = await cls.parse_response(response)

        context[Field.status_code] = response.status_code
        context[Field.response_data] = content
        context[Field.elapsed] = get_elapsed(context[Field.timestamp])

        await cls.log(
            event_method=context[Field.levelname],
            event=f"HTTP Response {context[Field.url]}",
            context=context,
            logger=logger,
            span=span,
        )

        return Response(
            content=content,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )

    @classmethod
    async def proxy(
        cls,
        request: Request,
        call_next,
        logger=None,
        tracer=None,
        *,
        exclude_paths: list[str] = None,
    ) -> Response:
        if exclude_paths:
            matches = [path for path in exclude_paths if re.match(path, str(request.url))]
            if matches:
                return await call_next(request)

        if not tracer:
            return await cls._proxy(request, call_next, logger)

        with tracer.start_as_current_span(str(request.url)) as span:
            return await cls._proxy(request, call_next, logger, span)
