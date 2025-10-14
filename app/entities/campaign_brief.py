"""Campaign Brief Entity

Input contract for campaign generation (Decision 4: YAML format).
"""
from dataclasses import dataclass
from typing import List
from datetime import datetime


@dataclass
class Product:
    """Product to be featured in campaign."""
    name: str
    palette_words: List[str]  # Visual style keywords: ["vibrant", "modern"]

    def __post_init__(self):
        if not self.name:
            raise ValueError("Product name is required")


@dataclass
class CampaignBrief:
    """
    Campaign brief input (Decision 4: YAML format).

    Defines what campaign to generate, for whom, and in which locales.
    Decision 6: Locale handling at campaign level (not product level).
    """
    brief_id: str
    brand_id: str
    campaign_slogan: str
    target_region: str  # e.g., "North America", "EMEA"
    target_audience: str  # e.g., "Gen Z professionals", "Parents 35-50"
    target_locales: List[str]  # Decision 7: ["en-US", "es-US"]
    products: List[Product]  # Decision: Minimum 2 products (PDF requirement)
    aspects: List[str]  # Decision: Minimum 3 ratios: ["1:1", "9:16", "16:9"]
    created_at: datetime

    def validate(self) -> bool:
        """Validate campaign brief meets PDF requirements."""
        return bool(
            self.brief_id and
            self.brand_id and
            self.campaign_slogan and
            len(self.products) >= 2 and  # PDF: at least 2 products
            len(self.aspects) >= 3 and   # PDF: at least 3 aspect ratios
            len(self.target_locales) >= 1  # At least English (Decision 7)
        )

    @property
    def total_assets_required(self) -> int:
        """Calculate total number of creative assets to generate."""
        return len(self.products) * len(self.aspects) * len(self.target_locales)
