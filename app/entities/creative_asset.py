"""Creative Asset Entity

Generated campaign creative (image + message).
"""
from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class CreativeAsset:
    """
    Generated creative asset for social ad campaign.

    Combines:
    - Hero image (generated via OpenAI DALL-E 3 or reused via Decision 8)
    - Localized campaign message (via Claude multilingual API)
    - Text overlay (via OpenAI API)
    """
    asset_id: str
    brief_id: str
    brand_id: str
    product_name: str
    audience: str
    locale: str  # e.g., "en-US", "es-US"
    aspect_ratio: str  # "1:1", "9:16", "16:9"
    message: str  # Localized campaign slogan
    image_url: str  # Path or URL to generated image
    reused: bool  # Decision 8: Was asset reused from existing?
    generated_at: datetime
    meta: Dict[str, Any]  # Additional metadata (GenAI params, validation results, etc.)

    def file_path(self, base_dir: str = "out/assets") -> str:
        """
        Generate organized file path (PDF requirement).

        Example: out/assets/product-soap/en-US/1x1/asset-123.png
        """
        return f"{base_dir}/{self.product_name}/{self.locale}/{self.aspect_ratio}/{self.asset_id}.png"

    @property
    def display_name(self) -> str:
        """Human-readable asset identifier."""
        return f"{self.product_name}_{self.aspect_ratio}_{self.locale}"
