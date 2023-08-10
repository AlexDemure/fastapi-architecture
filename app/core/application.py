import uvicorn
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.responses import Response
from starlette.middleware.cors import CORSMiddleware

from app.core.logger import logger
from app.core.sentry import add_sentry
from app.core.settings import config
from app.core.tracing import add_jaeger
from app.core.tracing import tracer
from app.core.urls import urls
from app.exceptions.business import BusinessError
from app.libs.http_client import ClientError
from app.libs.http_middleware import EXCLUDE_PATHS
from app.libs.http_middleware import HTTPMiddleware


def init_app():
    print("\n".join("%s: %s" % item for item in vars(config).items()))

    if config.TRACING:
        add_jaeger(service_name=config.PROJECT_NAME, endpoint=config.TRACING_ENDPOINT)

    if config.SENTRY:
        add_sentry(dsn=config.SENTRY_DSN, environment=config.SENTRY_ENVIRONMENT)

    application = FastAPI(
        title=config.PROJECT_NAME,
        debug=config.API_DEBUG,
        docs_url="/docs",
        openapi_url="/openapi.json",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(urls)

    return application


application = init_app()


@application.middleware("http")
async def _http_middleware(request, call_next) -> Response:
    return await HTTPMiddleware.proxy(request, call_next, logger, tracer, exclude_paths=EXCLUDE_PATHS)


@application.exception_handler(BusinessError)
async def business_error_handler(_: Request, error: BusinessError) -> JSONResponse:
    await logger.error(error.description, status_code=error.status_code, content=error.to_dict())
    return JSONResponse(status_code=error.status_code, content=error.to_dict())


@application.exception_handler(ClientError)
async def client_error_handler(_: Request, error: ClientError) -> JSONResponse:
    await logger.error(error.description, status_code=error.status_code, content=error.to_dict())
    return JSONResponse(status_code=error.status_code, content=error.to_dict())


if __name__ == "__main__":
    uvicorn.run("app.core.application:application", host="127.0.0.1", port=4000)
