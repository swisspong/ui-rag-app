from fastapi import Depends, status, Query
from typing import Optional
from dependency_injector.wiring import inject, Provide
import math

from src.contexts.collections.interfaces.http.schema.get_files_in_collection import (
    CollectionFileResponse,
    FilesListMeta,
    GetFilesInCollectionResponse
)
from src.contexts.collections.application.queries.get_files_in_collection.get_files_in_collection_query import GetFilesInCollectionQuery
from src.contexts.collections.application.queries.get_files_in_collection.get_files_in_collection_input import GetFilesInCollectionInput
from src.contexts.collections.application.queries.models.collection_file_read_model import CollectionFileReadModel
from src.contexts.collections.domain.value_objects.collection_id import CollectionID
from src.boot.container import ApplicationContainer
from . import router


def _map_read_model_to_response(read_model: CollectionFileReadModel) -> CollectionFileResponse:
    """Maps a CollectionFileReadModel to a CollectionFileResponse."""
    return CollectionFileResponse(
        id=read_model.id,
        name=read_model.filename,
        size=read_model.size,
        type=read_model.type,
        created_at=read_model.created_at
    )


@router.get(
    "/{collection_id}/files",
    response_model=GetFilesInCollectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Get files in a collection",
    description="Retrieves a paginated list of files associated with a specific collection"
)
@inject
async def get_files_in_collection(
    collection_id: str,
    search: Optional[str] = Query(
        None, description="Search term to filter files by filename"),
    order_by: str = Query(
        "created_at", description="Field to order by (created_at, filename)"),
    limit: int = Query(
        20, ge=1, le=100, description="Number of items per page"),
    page: int = Query(1, ge=1, description="Page number"),
    select: bool = Query(False, description="Return only id and name fields"),
    get_files_in_collection_query: GetFilesInCollectionQuery = Depends(
        Provide[ApplicationContainer.collection_package.get_files_in_collection_query]),
) -> GetFilesInCollectionResponse:

    # Calculate offset from page and limit
    offset = (page - 1) * limit

    input_data = GetFilesInCollectionInput(
        collection_id=CollectionID.from_value(collection_id),
        search=search,
        order_by=order_by,
        limit=limit,
        offset=offset,
        select=select
    )

    result = await get_files_in_collection_query.execute(input_data)

    # Map the read models to response models
    file_responses = [
        _map_read_model_to_response(file)
        for file in result.files
    ]

    # Calculate pagination metadata
    if select:
        metadata = None
    else:
        total_pages = math.ceil(result.total_count /
                                limit) if result.total_count > 0 else 0
        has_next_page = page < total_pages
        has_previous_page = page > 1

        metadata = FilesListMeta(
            total=result.total_count,
            limit=limit,
            page=page,
            total_pages=total_pages,
            search=search,
            has_next_page=has_next_page,
            has_previous_page=has_previous_page
        )

    # Create the response with data list and metadata
    return GetFilesInCollectionResponse(
        data=file_responses,
        metadata=metadata
    )
