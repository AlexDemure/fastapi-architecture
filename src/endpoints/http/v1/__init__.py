from fastapi import APIRouter

from .dummy import dummy_router

router = APIRouter(prefix="/v1")

router.include_router(dummy_router, tags=["Dummy"])
