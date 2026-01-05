from dataclasses import dataclass
from typing import Optional


@dataclass
class GetCollectionListInput:
    """
    Input model for the get_collection_list query.
    
    Used to retrieve a paginated list of collections with optional filtering.
    """
    search: Optional[str] = None
    order_by: str = "created_at"
    limit: int = 20
    offset: int = 0