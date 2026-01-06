from fastapi import Depends, status, HTTPException
from dependency_injector.wiring import inject, Provide

from src.contexts.collections.interfaces.http.schema.get_collection import (
    CollectionData,
    GetCollectionResponse
)
from src.contexts.collections.application.queries.get_collection.get_collection_query import GetCollectionQuery
from src.contexts.collections.application.queries.get_collection.get_collection_input import GetCollectionInput
from src.contexts.collections.application.queries.models.collection_read_model import CollectionReadModel
from src.contexts.collections.domain.value_objects.collection_id import CollectionID
from src.boot.container import ApplicationContainer
from . import router


def _map_read_model_to_response(read_model: CollectionReadModel) -> CollectionData:
    """Maps a CollectionReadModel to a CollectionData."""
    return CollectionData(
        id=read_model.id,
        name=read_model.name,
        description=read_model.description,
        file_count=read_model.file_count,
        created_at=read_model.created_at
    )


@router.get(
    "/{collection_id}",
    response_model=GetCollectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a collection by ID",
    description="Retrieves a specific collection by its unique identifier"
)
@inject
async def get_collection(
    collection_id: str,
    get_collection_query: GetCollectionQuery = Depends(
        Provide[ApplicationContainer.collection_package.get_collection_query]),
) -> GetCollectionResponse:

    input_data = GetCollectionInput(
        collection_id=CollectionID.from_value(collection_id)
    )

    result = await get_collection_query.execute(input_data)

    if result.collection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Collection with id '{collection_id}' not found"
        )

    # Map the read model to response model
    collection_data = _map_read_model_to_response(result.collection)

    # Create the response
    return GetCollectionResponse(
        data=collection_data,
        message="Collection retrieved successfully"
    )
