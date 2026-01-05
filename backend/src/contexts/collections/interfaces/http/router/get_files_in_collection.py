from fastapi import Depends, status
from dependency_injector.wiring import inject, Provide

from src.contexts.collections.interfaces.http.schema.get_files_in_collection import (
    CollectionFileResponse,
    DataWrapper,
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
        collection_file_id=read_model.collection_file_id,
        filename=read_model.filename,
        size=read_model.size,
        asset_id=read_model.asset_id,
        created_at=read_model.created_at,
        current_stage=read_model.current_stage,
        status="in progress" if read_model.status == "running" else read_model.status
    )


@router.get(
    "/{collection_id}/files",
    response_model=GetFilesInCollectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Get files in a collection",
    description="Retrieves all files associated with a specific collection"
)
@inject
async def get_files_in_collection(
    collection_id: str,
    get_files_in_collection_query: GetFilesInCollectionQuery = Depends(
        Provide[ApplicationContainer.collection_package.get_files_in_collection_query]),
) -> GetFilesInCollectionResponse:

    input_data = GetFilesInCollectionInput(
        collection_id=CollectionID.from_value(collection_id)
    )

    result = await get_files_in_collection_query.execute(input_data)
    # Map the read models to response models
    file_responses = [
        _map_read_model_to_response(file) 
        for file in result
    ]

    # Create the response
    return GetFilesInCollectionResponse(
        data=DataWrapper(files=file_responses)
    )
