from fastapi import FastAPI

from src.contexts.collections.interfaces.http.router import router as CollectionRouter
from src.contexts.rag.interfaces.http.router import router as RAGRouter


def register_router(app: FastAPI):
    app.include_router(CollectionRouter)
    app.include_router(RAGRouter)
