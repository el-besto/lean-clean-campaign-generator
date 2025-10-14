"""Brand Summary Entity

Encapsulates brand identity, guidelines, and consistency rules.
Generated via Claude Vision API from brand assets.
"""
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class BrandSummary:
    """
    Brand identity and guidelines for campaign generation.

    Generated via Claude Vision API from brand assets.
    Stored in YAML config (Decision 5) with adapter for Weaviate evolution.
    """
    brand_id: str
    name: str
    description: str
    colors: List[str]  # Hex codes: ["#FF5733", "#33FF57"]
    typography: Optional[str]
    voice_tone: str  # e.g., "professional", "playful", "authoritative"
    target_audiences: List[str]
    target_regions: List[str]
    products: List[str]
    campaign_slogans: List[str]  # Historical slogans for consistency
    logo_url: Optional[str]
    created_at: datetime
    updated_at: datetime

    def validate(self) -> bool:
        """Validate brand summary has minimum required fields."""
        return bool(
            self.brand_id and
            self.name and
            self.description and
            self.colors and
            self.voice_tone
        )
