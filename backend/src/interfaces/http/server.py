from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.shared.infrastructure.configs.settings import Settings
from src.shared.errors.error import Error
from src.boot.container import ApplicationContainer
from src.interfaces.http.routes import register_router
from src.interfaces.http.execption_handler import register_exception_handlers
# from src.contexts.rag.interfaces.http.router.chunking


@asynccontextmanager
async def lifespan(app: FastAPI):

    container = ApplicationContainer()
    container.config.from_pydantic(Settings())

    container.wire(modules=[
        "src.contexts.collections.interfaces.http.router.create_collection",
        "src.contexts.collections.interfaces.http.router.get_collection_list",
        "src.contexts.collections.interfaces.http.router.get_collection",
        "src.contexts.collections.interfaces.http.router.get_files_in_collection",
        "src.contexts.collections.interfaces.http.router.upload_files",
        "src.contexts.rag.interfaces.http.router.process_ocr",
        "src.contexts.rag.interfaces.http.router.chunking",
        "src.contexts.rag.interfaces.http.router.ingest",
        "src.contexts.rag.interfaces.http.router.get_documents_in_collection",
        "src.contexts.rag.interfaces.http.router.get_chunks_by_collection_file_id",
        "src.contexts.rag.interfaces.http.router.get_document_by_collection_and_file_id",
        "src.contexts.rag.interfaces.http.router.get_chunk_by_id_and_collection_id",
        "src.contexts.rag.interfaces.http.router.update_chunk",
        "src.contexts.rag.interfaces.http.router.delete_multiple_chunks",
        "src.contexts.rag.interfaces.http.router.get_chunks_by_collection_id",
        "src.contexts.rag.interfaces.http.router.ingest_multiple_chunks_by_collection",
        "src.contexts.rag.interfaces.http.router.get_document_chunks_in_collection",
    ])

    database = container.database()
    await database.connect()

    yield

    await database.disconnect()
    container.unwire()

# Create FastAPI app
app = FastAPI(
    title="RAG API",
    description="A FastAPI application with DDD architecture",
    version="1.0.0",
    lifespan=lifespan
)

register_exception_handlers(app)
# ValueError exception handler


# @app.exception_handler(ValueError)
# async def value_error_exception_handler(request: Request, exc: ValueError):
#     return JSONResponse(
#         status_code=status.HTTP_400_BAD_REQUEST,
#         content={
#             "error": "Validation Error",
#             "message": str(exc),
#             # Add this line to include the message in detail
#             "detail": str(exc),
#             "type": "value_error"
#         }
#     )


# @app.exception_handler(Error)
# async def base_error_exception_handler(request: Request, exc: Error):
#     if isinstance(exc, ModelInvalidError):
#         return JSONResponse(
#             status_code=exc.status_code,
#             content={
#                 "error": exc.code,
#                 "message": str(exc),
#                 "field": exc.field,
#                 # Add this line to include the message in detail
#                 "detail": str(exc),
#                 "type": exc.__class__.__name__
#             }
#         )
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={
#             "error": exc.code,
#             "message": str(exc),
#             # Add this line to include the message in detail
#             "detail": str(exc),
#             "type": exc.__class__.__name__
#         }
#     )

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
register_router(app)

# Health check endpoint


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

# Root endpoint


@app.get("/")
async def root():
    return {"message": "Welcome to RAG API"}
