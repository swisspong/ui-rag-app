from typing import List, Union, Optional, Dict, Any
from collections import defaultdict
import logging

from src.contexts.rag.domain.repositories.vector_repository import VectorRepository
from src.contexts.rag.infrastructure.database.milvus_connection import MilvusConnection
from src.contexts.rag.domain.entities.new_vector_chunk import NewVectorChunk
from src.contexts.rag.domain.value_objects.vector_chunk_id import VectorChunkID
from src.contexts.rag.domain.value_objects.chunk_id import ChunkID
from src.contexts.rag.domain.value_objects.collection_id import CollectionID
# type: ignoreutility
from pymilvus import MilvusClient, DataType, CollectionSchema, FieldSchema, utility
logger = logging.getLogger(__name__)


class MilvusVectorRepository(VectorRepository):

    def __init__(self, connection: MilvusConnection):

        self._connection = connection

    def _get_index_params(self):
        """Get IndexParams in a version-compatible way"""
        try:
            # Try to use client's prepare_index_params method (most common)
            if hasattr(self._connection._client, "prepare_index_params"):
                return self._connection._client.prepare_index_params()
        except Exception:
            pass

        try:
            # Try to import IndexParams from different possible locations
            from pymilvus.client.prepare import IndexParams

            return IndexParams()
        except ImportError:
            pass

        try:
            from pymilvus.client.types import IndexParams

            return IndexParams()
        except ImportError:
            pass

        try:
            from pymilvus import IndexParams

            return IndexParams()
        except ImportError:
            pass

        # If all else fails, return None to use fallback method
        return None

    def _create_vector_index_fallback(self, collection_name: str):
        """Fallback method to create vector index using direct API"""
        try:
            self._connection._client.create_index(
                collection_name=collection_name,
                field_name="vector",
                index_params={
                    "index_type": "HNSW",
                    "metric_type": "COSINE",
                    "params": {"M": 16, "efConstruction": 256},
                },
            )
            logger.debug(
                f"[{collection_name}] Created vector index using fallback method"
            )
        except Exception as e:
            logger.warning(
                f"[{collection_name}] Failed to create vector index using fallback method: {e}"
            )

    def _create_indexes_after_collection(self, collection_name: str):
        """Create indexes after collection is created"""
        try:
            # Try to get IndexParams in a version-compatible way
            IndexParamsClass = self._get_index_params()

            if IndexParamsClass is not None:
                # Use IndexParams approach if available
                try:
                    # Create vector index first (required for most operations)
                    vector_index = IndexParamsClass
                    vector_index.add_index(
                        field_name="vector",
                        index_type="HNSW",
                        metric_type="COSINE",
                        params={"M": 16, "efConstruction": 256},
                    )
                    self._connection._client.create_index(
                        collection_name=collection_name, index_params=vector_index
                    )
                    logger.debug(
                        f"[{collection_name}] Created vector index using IndexParams"
                    )
                except Exception as e:
                    logger.debug(
                        f"[{collection_name}] IndexParams method failed for vector index: {e}"
                    )
                    self._create_vector_index_fallback(collection_name)

                # if self.namespace.endswith("chunks"):
                #     # Create indexes for chunk fields
                #     try:
                #         doc_id_index = self._get_index_params()
                #         doc_id_index.add_index(
                #             field_name="full_doc_id", index_type="INVERTED"
                #         )
                #         self._client.create_index(
                #             collection_name=self.final_namespace,
                #             index_params=doc_id_index,
                #         )
                #     except Exception as e:
                #         logger.debug(
                #             f"[{self.workspace}] IndexParams method failed for full_doc_id: {e}"
                #         )
                #         self._create_scalar_index_fallback(
                #             "full_doc_id", "INVERTED")

                # No common indexes needed

            else:
                # Fallback to direct API calls if IndexParams is not available
                logger.info(
                    f"[{collection_name}] IndexParams not available, using fallback methods for {collection_name}"
                )

                # Create vector index using fallback
                self._create_vector_index_fallback(collection_name)

                # Create scalar indexes using fallback
                # if self.namespace.endswith("entities"):
                #     self._create_scalar_index_fallback(
                #         "entity_name", "INVERTED")
                # elif self.namespace.endswith("relationships"):
                #     self._create_scalar_index_fallback("src_id", "INVERTED")
                #     self._create_scalar_index_fallback("tgt_id", "INVERTED")
                # elif self.namespace.endswith("chunks"):
                #     self._create_scalar_index_fallback(
                #         "full_doc_id", "INVERTED")

            logger.info(
                f"[{collection_name}] Created indexes for collection:"
            )

        except Exception as e:
            logger.warning(
                f"[{collection_name}] Failed to create some indexes for: {e}")

    def _ensure_collection_loaded(self, collection_name: str):
        """Ensure the collection is loaded into memory for search operations"""
        try:
            # Check if collection exists first
            if not self._connection._client.has_collection(collection_name):
                logger.error(
                    f"[{collection_name}] Collection {collection_name} does not exist"
                )
                raise ValueError(
                    f"Collection {collection_name} does not exist")

            # Load the collection if it's not already loaded
            # In Milvus, collections need to be loaded before they can be searched
            self._connection._client.load_collection(collection_name)
            # logger.debug(f"[{self.workspace}] Collection {self.namespace} loaded successfully")

        except Exception as e:
            logger.error(
                f"[{collection_name}] Failed to load collection {collection_name}: {e}"
            )
            raise

    def _create_collection_if_not_exist(self, collection_name: str, dimension: int):
        collection_exists = self._connection._client.has_collection(
            collection_name)
        if not collection_exists:
            schema = self._create_schema_for_namespace(dimension)
            self._connection._client.create_collection(
                collection_name=collection_name, schema=schema
            )
            self._create_indexes_after_collection(collection_name)
            self._ensure_collection_loaded(collection_name)

    def _create_schema_for_namespace(self, dimension: int) -> CollectionSchema:
        """Create schema based on the current instance's namespace"""

        # Get vector dimension from embedding_func
        # dimension = self.embedding_func.embedding_dim

        # Base fields (common to all collections)
        base_fields = [
            FieldSchema(
                name="id", dtype=DataType.VARCHAR, max_length=64, is_primary=True
            ),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR,
                        dim=dimension),
            FieldSchema(name="created_at", dtype=DataType.INT64),
        ]

        specific_fields = [
            FieldSchema(
                name="full_doc_id",
                dtype=DataType.VARCHAR,
                max_length=64,
                nullable=True,
            ),
            FieldSchema(
                name="file_path",
                dtype=DataType.VARCHAR,
                max_length=32768,
                nullable=True,
            ),
        ]
        description = ""

        # Merge all fields
        all_fields = base_fields + specific_fields

        return CollectionSchema(
            fields=all_fields,
            description=description,
            enable_dynamic_field=True,  # Support dynamic fields
        )

    async def upsert(self, collection_name: str, data: List[NewVectorChunk]) -> None:

        # if not self._connection.is_connected():
        #     await self._connection.connect()

        # collection = self._connection.get_collection(
        #     collection_name=collection_name
        # )

        self._connection._client.upsert(
            collection_name=collection_name,
            data=[
                d.to_dict()
                for d in data
            ],
            partial_update=True
        )

    def _format_collection_name(self, collection_name: str) -> str:
        """Format collection name for Milvus by replacing hyphens with underscores and adding underscore prefix."""
        return "_" + collection_name.replace("-", "_")

    async def get_by_collection_id_and_chunk_id(
        self,
        collection_id: str,
        chunk_id: Optional[str] = None,
    ) -> List[NewVectorChunk]:
        """
        Query vectors by dynamic fields collection_id and optionally chunk_id.
        
        Args:
            collection_id: The collection_id to filter by (used to format collection name)
            chunk_id: Optional filter for chunk_id dynamic field
            
        Returns:
            List of NewVectorChunk entities matching the filter criteria
        """
        formatted_collection_name = self._format_collection_name(collection_id)
        
        # Ensure collection exists and is loaded
        if not self._connection._client.has_collection(formatted_collection_name):
            logger.error(
                f"[{formatted_collection_name}] Collection does not exist"
            )
            raise ValueError(f"Collection {collection_id} does not exist")
        
        self._ensure_collection_loaded(formatted_collection_name)
        
        # Build filter expression for dynamic fields
        if chunk_id:
            filter_expr = f'collection_id == "{collection_id}" && chunk_id == "{chunk_id}"'
        else:
            filter_expr = f'collection_id == "{collection_id}"'
        
        # Perform the query
        try:
            results = self._connection._client.query(
                collection_name=formatted_collection_name,
                filter=filter_expr,
                output_fields=["id", "vector", "content", "meta", "created_at", "collection_id", "chunk_id", "full_doc_id", "file_path"]
            )
            
            logger.debug(
                f"[{formatted_collection_name}] Query completed with {len(results)} results"
            )
            
            # Map results to NewVectorChunk entities
            vector_chunks = []
            for result in results:
                vector_chunk = NewVectorChunk(
                    id=VectorChunkID.from_value(result["id"]),
                    chunk_id=ChunkID.from_value(result["chunk_id"]) if result.get("chunk_id") else None,
                    collection_id=CollectionID.from_value(result["collection_id"]),
                    vector=result["vector"],
                    content=result["content"],
                    meta=result.get("meta", {}),
                    created_at=result["created_at"]
                )
                vector_chunks.append(vector_chunk)
            
            return vector_chunks
            
        except Exception as e:
            logger.error(
                f"[{formatted_collection_name}] Query failed: {e}"
            )
            raise

    async def saves(self, data: List[NewVectorChunk], dimension: int) -> None:
        if not data:
            return

        # Group data by collection_id.value (collection name)
        grouped_data = defaultdict(list)
        for item in data:
            collection_name = item.collection_id.value
            grouped_data[collection_name].append(item)

        # Upsert each group to its respective collection
        for collection_name, chunks in grouped_data.items():
            formatted_collection_name = self._format_collection_name(
                collection_name)
            self._create_collection_if_not_exist(formatted_collection_name, dimension)
            await self.upsert(collection_name=formatted_collection_name, data=chunks)
