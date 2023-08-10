from fastapi import APIRouter

from app.api.v1.accounts import router as accounts_router
from app.core.settings import config

urls = APIRouter(prefix=config.API_PREFIX)

urls.include_router(accounts_router, tags=["Accounts"])
