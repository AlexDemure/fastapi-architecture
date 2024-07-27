from fastapi import APIRouter
from fastapi import Path
from fastapi import status

from src.domain import services

from .schemas import GetDummyDocumentResponse
from .schemas import GetDummyResponse
from .schemas import PostDummyDocumentResponse
from .schemas import PostDummyResponse

router = APIRouter()


@router.post(
    "/dummy",
    status_code=status.HTTP_201_CREATED,
    response_model=PostDummyResponse,
)
async def dummy_create() -> PostDummyResponse:
    dummy = await services.Dummy.create()
    return PostDummyResponse.serialize(dummy)


@router.get(
    "/dummy/{id}",
    status_code=status.HTTP_200_OK,
    response_model=GetDummyResponse,
)
async def dummy_get(dummy_id: int = Path(..., alias="id")) -> GetDummyResponse:
    dummy = await services.Dummy.get(dummy_id)
    return GetDummyResponse.serialize(dummy)


@router.post(
    "/dummy-document",
    status_code=status.HTTP_201_CREATED,
    response_model=PostDummyDocumentResponse,
)
async def dummy_document_create() -> PostDummyDocumentResponse:
    dummy = await services.DummyDocument.create()
    return PostDummyDocumentResponse.serialize(dummy)


@router.get(
    "/dummy-document/{id}",
    status_code=status.HTTP_200_OK,
    response_model=GetDummyDocumentResponse,
)
async def dummy_document_get(dummy_id: str = Path(..., alias="id")) -> GetDummyDocumentResponse:
    dummy = await services.DummyDocument.get(dummy_id)
    return GetDummyDocumentResponse.serialize(dummy)
