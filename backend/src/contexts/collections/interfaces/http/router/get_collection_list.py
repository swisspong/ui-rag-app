from fastapi import Depends, status
from dependency_injector.wiring import inject, Provide
import math
from src.contexts.collections.interfaces.http.schema.get_collection_list import (
    GetCollectionListRequest,
    GetCollectionListResponse,
    CollectionResponse,
    CollectionListData,
    CollectionListMeta,
)
from src.contexts.collections.application.queries.get_collection_list.get_collection_list_query import GetCollectionListQuery
from src.contexts.collections.application.queries.get_collection_list.get_collection_list_input import GetCollectionListInput
from src.contexts.collections.application.queries.models.collection_read_model import (
    CollectionReadModel,
    LLMConfigReadModel,
    EmbeddingConfigReadModel,
    ChunkingConfigReadModel
)
from src.boot.container import ApplicationContainer
from . import router


def _map_read_model_to_response(read_model: CollectionReadModel) -> CollectionResponse:
    """Maps a CollectionReadModel to a CollectionResponse."""
    return CollectionResponse(
        id=read_model.id,
        name=read_model.name,
        description=read_model.description,
        file_count=read_model.file_count,
        created_at=read_model.created_at,
        updated_at=read_model.updated_at
    )


@router.get(
    "",
    response_model=GetCollectionListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a list of collections",
    description="Retrieves a paginated list of collections with optional search functionality"
)
@inject
async def get_collection_list(
    request: GetCollectionListRequest = Depends(),
    get_collection_list_query: GetCollectionListQuery = Depends(
        Provide[ApplicationContainer.collection_package.get_collection_list_query]),
) -> GetCollectionListResponse:

    input_data = GetCollectionListInput(
        search=request.search,
        order_by=request.order_by,
        limit=request.limit,
        offset=(request.page - 1) * request.limit
    )

    result = await get_collection_list_query.execute(input_data)

    # Map the read models to response models
    collection_responses = [
        _map_read_model_to_response(collection)
        for collection in result.collections
    ]
    total_pages = math.ceil(result.total_count / request.limit)
    # Create the response
    return GetCollectionListResponse(
        data=CollectionListData(
            collections=collection_responses
        ),
        meta=CollectionListMeta(
            total=result.total_count,
            limit=request.limit,
            page=request.page,
            search=request.search,
            total_pages=total_pages,
            has_next_page=request.page < total_pages,
            has_previous_page=request.page > 1
        )
    )
