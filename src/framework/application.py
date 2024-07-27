from contextlib import asynccontextmanager

from fastapi import Depends
from fastapi import FastAPI
from fastapi import Request
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from src.endpoints.http import router
from src.tools.exceptions import Error
from src.tools.fastapi.middleware.http import EXCLUDE_PATHS
from src.tools.fastapi.middleware.http import HTTPMiddleware

from .i18n import I18Error
from .i18n import Locale
from .logger import logger
from .settings import settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield
    # await Cache.delete_namespace()


app = FastAPI(
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
)


@app.get(f"{settings.SERVER_API_PATH}/docs", include_in_schema=False)
async def swagger():
    return get_swagger_ui_html(
        openapi_url=f"{settings.SERVER_API_PATH}/openapi.json",
        title=app.title,
    )


@app.get(f"{settings.SERVER_API_PATH}/redoc", include_in_schema=False)
async def redoc():
    return get_redoc_html(openapi_url=f"{settings.SERVER_API_PATH}/openapi.json", title=app.title)


@app.get(f"{settings.SERVER_API_PATH}/openapi.json", include_in_schema=False)
async def openapi():
    return get_openapi(title=app.title, version=app.version, routes=app.routes)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    HTTPMiddleware,
    exclude_paths=EXCLUDE_PATHS,
    logger=logger,
)

app.include_router(router)

app.mount(f"{settings.SERVER_API_PATH}/static", StaticFiles(directory="src/static"), name="static")


@app.exception_handler(I18Error)
async def i18error_handler(request: Request, error: I18Error) -> JSONResponse:
    locale = Locale(request.headers.get("locale"))

    await logger.error(
        error.description,
        status_code=error.status_code,
        content=error.to_dict(locale),
    )
    return JSONResponse(status_code=error.status_code, content=error.to_dict(locale))


@app.exception_handler(Error)
async def error_handler(_: Request, error: Error) -> JSONResponse:
    await logger.error(
        error.description,
        status_code=error.status_code,
        content=error.to_dict(),
    )

    return JSONResponse(status_code=error.status_code, content=error.to_dict())
