"""
In-Memory Brand Repository for Testing
"""
from typing import Dict, List, Optional
from datetime import datetime
from app.entities.brand_summary import BrandSummary


class InMemoryBrandRepository:
    """In-memory brand repository implementing IBrandRepository protocol."""

    def __init__(self):
        # Seed with example brand
        self.brands: Dict[str, BrandSummary] = {
            "natural-suds-co": BrandSummary(
                brand_id="natural-suds-co",
                name="Natural Suds Co.",
                description="Organic personal care products",
                colors=["#8B7355", "#E6D5B8", "#4A6741"],
                typography="Montserrat",
                voice_tone="warm, natural, trustworthy",
                target_audiences=["Health-conscious millennials", "Eco-friendly shoppers"],
                target_regions=["North America", "Europe"],
                products=["Lavender Soap", "Citrus Shower Gel", "Rose Hand Cream"],
                campaign_slogans=["Pure Nature", "Wellness Naturally"],
                logo_url=None,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
        }

    def get_by_id(self, brand_id: str) -> Optional[BrandSummary]:
        """Load brand from dict."""
        return self.brands.get(brand_id)

    def search_similar(self, brand: BrandSummary, limit: int = 5) -> List[BrandSummary]:
        """Stub for vector search (Task 3)."""
        return []  # Not implemented in fake
