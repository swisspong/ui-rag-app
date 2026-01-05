from fastapi import APIRouter

router = APIRouter(prefix="/collections", tags=["Collections"])

from . import (
    create_collection,
    get_collection_list,
    get_files_in_collection,
    upload_files
)