import logging
from datetime import datetime
from enum import Enum
from json import JSONDecodeError
from typing import Optional
from urllib.parse import urlparse

import httpx
from httpx import HTTPError
from httpx import HTTPStatusError

from app.libs.utils import get_elapsed
from app.libs.utils import get_traceback


class ClientError(Exception):
    status_code: int
    reason: Optional[str] = None
    description: Optional[str] = None

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    def to_dict(self) -> dict:
        return dict(
            status_code=self.status_code,
            detail=dict(
                type=self.class_name,
                reason=self.reason,
                description=self.description,
            ),
        )


class CanNotGetResponseError(ClientError):
    status_code = 503

    def __init__(self, error: HTTPError) -> None:
        self.reason = error.__class__.__name__

        if str(error):
            self.reason = f"{self.reason} {str(error)}"


class ServiceError(ClientError):
    def __init__(self, error: HTTPStatusError) -> None:
        self.status_code = error.response.status_code

        try:
            self.reason = error.response.json()
        except JSONDecodeError:
            self.reason = str(error.response.text)


class Field(str, Enum):
    method = "method"
    timestamp = "timestamp"
    levelname = "levelname"
    level = "level"
    url = "url"
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


class HTTPClient:
    @classmethod
    async def log(cls, event_method: str, event: str, context: dict, logger=None) -> None:
        if logger:
            await getattr(logger, event_method.lower())(event, **context)

    @classmethod
    async def request(  # noqa:C901
        cls,
        method: str,
        url: str,
        headers: Optional[dict] = None,
        body: Optional[dict] = None,
        logger=None,
        **kwargs,
    ) -> Optional[dict]:
        request_params = dict(url=url, method=method, json=body, headers=headers, **kwargs)

        context = {
            Field.method: request_params["method"],
            Field.timestamp: datetime.utcnow(),
            Field.levelname: "INFO",
            Field.level: logging.INFO,
            Field.headers: request_params["headers"],
            Field.request_data: request_params["json"],
            Field.request_path: urlparse(request_params["url"]).path,
            Field.url: request_params["url"],
            **kwargs,
        }

        await cls.log(
            event_method=context[Field.levelname],
            event=f"Send request to {url}",
            context=context,
            logger=logger,
        )

        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(**request_params)
                response.raise_for_status()
                context[Field.status_code] = response.status_code
                context[Field.elapsed] = get_elapsed(context[Field.timestamp])
            except (HTTPStatusError, HTTPError) as e:
                if isinstance(e, HTTPStatusError):
                    error = ServiceError(e)
                else:
                    error = CanNotGetResponseError(e)

                context[Field.stacktrace] = get_traceback(e)
                context[Field.exception] = error.reason
                context[Field.levelname] = "ERROR"
                context[Field.level] = logging.ERROR
                context[Field.elapsed] = get_elapsed(context[Field.timestamp])

                await cls.log(
                    event_method=context[Field.levelname],
                    event=f"Received error from {url}",
                    context=context,
                    logger=logger,
                )

                raise error

        data = None

        if response.text:
            data = response.json()

        context[Field.response_data] = data
        context[Field.elapsed] = get_elapsed(context[Field.timestamp])

        await cls.log(
            event_method=context[Field.levelname],
            event=f"Received response from {url}",
            context=context,
            logger=logger,
        )

        return data
