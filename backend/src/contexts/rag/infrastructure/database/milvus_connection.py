import logging
from typing import Optional, Dict, Any, List
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility, MilvusClient
from pymilvus.exceptions import MilvusException


logger = logging.getLogger(__name__)


class MilvusConnection:
    """
    Manages connection to Milvus vector database.
    Provides connection pooling and collection management functionality.
    """
    _client: MilvusClient
    def __init__(self, host: str = "localhost", port: int = 19530, user: str = "", password: str = "", db_name: str = ""):
        """
        Initialize Milvus connection parameters.

        Args:
            host: Milvus server host
            port: Milvus server port
            user: Username for authentication (optional)
            password: Password for authentication (optional)
            db_name: Database name (optional)
        """
        # self._host = host
        # self._port = port
        # self._user = user
        # self._password = password
        # self._db_name = db_name
        # self._alias = "default"
        # self._connected = False
        self._client = MilvusClient(
            uri=f"http://{host}:{port}",
            user=user,
            password=password,
            db_name=db_name
        )

    async def connect(self) -> None:
        """
        Establish connection to Milvus server.
        """
        try:
            if self._user and self._password:
                connections.connect(
                    alias=self._alias,
                    host=self._host,
                    port=self._port,
                    user=self._user,
                    password=self._password,
                    db_name=self._db_name
                )
            else:
                connections.connect(
                    alias=self._alias,
                    host=self._host,
                    port=self._port,
                    db_name=self._db_name
                )
            self._connected = True
            logger.info(f"Connected to Milvus at {self._host}:{self._port}")
        except MilvusException as e:
            logger.error(f"Failed to connect to Milvus: {e}")
            raise

    async def disconnect(self) -> None:
        """
        Disconnect from Milvus server.
        """
        try:
            if self._connected:
                connections.disconnect(self._alias)
                self._connected = False
                logger.info("Disconnected from Milvus")
        except MilvusException as e:
            logger.error(f"Error disconnecting from Milvus: {e}")
            raise

    def is_connected(self) -> bool:
        """
        Check if connected to Milvus.

        Returns:
            True if connected, False otherwise
        """
        return self._connected

    def get_collection(self, collection_name: str) -> Collection:
        """
        Get an existing collection.

        Args:
            collection_name: Name of the collection

        Returns:
            Collection object
        """
        try:
            if not utility.has_collection(collection_name, using=self._alias):
                raise ValueError(
                    f"Collection {collection_name} does not exist")

            return Collection(collection_name, using=self._alias)
        except MilvusException as e:
            logger.error(f"Error getting collection {collection_name}: {e}")
            raise

    def has_collection(self, collection_name: str):
        """
        Get an existing collection.

        Args:
            collection_name: Name of the collection

        Returns:
            Collection object
        """
        try:
            return utility.has_collection(collection_name, using=self._alias)
            #     raise ValueError(
            #         f"Collection {collection_name} does not exist")

            # return Collection(collection_name, using=self._alias)
        except MilvusException as e:
            logger.error(f"Error getting collection {collection_name}: {e}")
            raise

    def create_collection(self, collection_name: str, schema: CollectionSchema):
        utility.create_collection


# class MilvusVectorRepository:
#     """
#     Concrete implementation of VectorRepository for Milvus vector database.
#     This repository operates in the infrastructure layer, fulfilling the domain
#     contract without introducing infrastructural concerns into the domain.
#     """

#     def __init__(self, connection: MilvusConnection):
#         """
#         Initialize with a MilvusConnection which provides the connection handling.

#         Args:
#             connection: MilvusConnection instance
#             collection_name: Name of the Milvus collection
#             vector_dim: Dimension of the vector embeddings
#         """
#         self._connection = connection

#     async def get_by_full_doc_ids(self, collection_name: str, full_doc_ids: list[str]):

#         # Check if Milvus connection is established, if not, connect
#         if not self._connection.is_connected():
#             await self._connection.connect()

#         test = self._connection.get_collection(
#             collection_name=collection_name
#         )

#         # Format the full_doc_ids list for Milvus expression
#         # String values need to be quoted in the expression
#         formatted_ids = [f"'{doc_id}'" for doc_id in full_doc_ids]
#         expr = f"full_doc_id in [{', '.join(formatted_ids)}]"
#         result = test.query(expr=expr, output_fields=["id", "full_doc_id"])
#         return result

#     async def upsert(self, collection_name: str, data: list[str]):

#         if not self._connection.is_connected():
#             await self._connection.connect()

#         test = self._connection.get_collection(
#             collection_name=collection_name
#         )

#         test.upsert(data=data, partial_update=True)


# async def main():
#     milvus_connection = MilvusConnection(
#         "localhost",
#         "19530",
#         "",
#         "",
#         "default"
#     )

#     milvus_repository = MilvusVectorRepository(milvus_connection)

#     data = [
#         {
#             "id": "chunk-4a22ff0ec9bff531f5cb6da0d8de221d",
#             "test": None
#         }
#     ]

#     await milvus_repository.get_by_full_doc_ids("_269f4415_d7ce_4098_b93b_2a0547403421_chunks", ["48e9a9de-6823-419c-89a7-a2a5c193e6d9"])
#     await milvus_repository.upsert("_269f4415_d7ce_4098_b93b_2a0547403421_chunks", data)

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())
