from typing import List

from fastapi import UploadFile, File, Form, Depends, status
from dependency_injector.wiring import inject, Provide

from src.contexts.collections.interfaces.http.schema.create_collection import (
    CreateCollectionRequest,
    CreateCollectionResponse
)
from src.contexts.collections.application.commands.upload_files_for_collection.upload_files_handler import UploadFilesHandler
from src.contexts.collections.application.commands.upload_files_for_collection.upload_files_input import UploadFilesInput, FileItem
from src.boot.container import ApplicationContainer
from . import router


@router.post(
    "/{collection_id}/files",
    status_code=status.HTTP_200_OK,
    summary="",
    description=""
)
@inject
async def upload_files(
    collection_id: str,
    files: List[UploadFile] = File(...),
    upload_files_command: UploadFilesHandler = Depends(
        Provide[ApplicationContainer.collection_package.upload_files_command]),
):
    results = []
    input = UploadFilesInput(
        collection_id=collection_id,
        files=[
            FileItem(
                filename=f.filename,
                content_type=f.content_type,
                stream=f.file,
                size=f.size
            )
            for f in files
        ]
    )

    await upload_files_command.execute(input)
    # incoming_files = [
    #     IncomingFile(
    #         filename=f.filename,
    #         content_type=f.content_type or "application/octet-stream",
    #         stream=f.file,   # <— สำคัญ
    #         size=f.size
    #     )
    #     for f in files
    # ]

    for file in files:
        # 1. validate file (size / type)
        # 2. create File entity
        # 3. save file to storage
        # 4. create Document
        # 5. enqueue RAG OCR job

        results.append({
            "filename": file.filename,
            "status": "UPLOADED"
        })

    return {
        "collection_id": collection_id,
        "files": results
    }
