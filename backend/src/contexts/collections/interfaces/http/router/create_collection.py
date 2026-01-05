from fastapi import Depends, status
from dependency_injector.wiring import inject, Provide

from src.contexts.collections.interfaces.http.schema.create_collection import (
    CreateCollectionRequest,
    CreateCollectionResponse
)
from src.contexts.collections.application.commands.create_collection.create_collection_handler import CreateCollectionHandler
from src.contexts.collections.application.commands.create_collection.create_collection_input import (
    CreateCollectionInput,
)
from src.boot.container import ApplicationContainer
from . import router


@router.post(
    "",
    response_model=CreateCollectionResponse,
    status_code=status.HTTP_200_OK,
    summary="",
    description=""
)
@inject
async def create_collection(
    request: CreateCollectionRequest,
    create_collection_command: CreateCollectionHandler = Depends(
        Provide[ApplicationContainer.collection_package.create_collection_command]),
) -> CreateCollectionResponse:

    input = CreateCollectionInput(
        name=request.name,
        description=request.description,
    )

    await create_collection_command.execute(input)

    return CreateCollectionResponse()
