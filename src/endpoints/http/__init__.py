from fastapi import APIRouter
from fastapi import Depends

from src.framework import settings
from src.framework.i18n import get_locale

from .v1 import router as v1_router

router = APIRouter(prefix=settings.SERVER_API_PATH, dependencies=[Depends(get_locale)])

router.include_router(v1_router)
