"""
Brand Repository Protocol

Defines contract for brand persistence:
- YAML file loader (simple)
- Weaviate vector store (advanced)
"""
from typing import Protocol, Optional, List
from app.entities.brand_summary import BrandSummary


class IBrandRepository(Protocol):
    """Interface for brand repositories."""

    def get_by_id(self, brand_id: str) -> Optional[BrandSummary]:
        """Load brand by ID."""
        ...

    def search_similar(self, brand: BrandSummary, limit: int = 5) -> List[BrandSummary]:
        """Find similar brands (for Task 3)."""
        ...
