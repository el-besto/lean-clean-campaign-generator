"""
AI Adapter Protocol (Interface)

Defines contract for AI services:
- Image generation (OpenAI DALL-E 3)
- Text overlay (OpenAI API)
- Brand understanding (Claude Vision)
- Localization (Claude Multilingual)
"""
from typing import Protocol, Dict, List


class IAIAdapter(Protocol):
    """Interface for AI adapters (image gen, localization, brand analysis)."""

    def generate_image(self, prompt: str, aspect_ratio: str, seed_image: bytes = None) -> bytes:
        """
        Generate hero image from text prompt, optionally based on a seed image.

        Args:
            prompt: Image generation prompt (product + brand guidelines)
            aspect_ratio: "1:1", "9:16", or "16:9"
            seed_image: Optional seed image bytes to base generation on

        Returns:
            Image bytes (PNG format)
        """
        ...

    def overlay_text(self, image: bytes, text: str, aspect_ratio: str) -> bytes:
        """
        Add campaign message text overlay to image.

        Args:
            image: Base image bytes
            text: Localized campaign slogan
            aspect_ratio: Image dimensions

        Returns:
            Image with text overlay (PNG format)
        """
        ...

    def understand_brand(self, brand_assets: List[str]) -> Dict[str, any]:
        """
        Analyze brand assets to extract brand guidelines.

        Args:
            brand_assets: List of image URLs or paths

        Returns:
            Dict with brand summary (colors, voice, typography, etc.)
        """
        ...

    def localize(self, text: str, source_locale: str, target_locale: str) -> str:
        """
        Translate text while preserving brand voice.

        Args:
            text: Source text (campaign slogan)
            source_locale: Source language (e.g., "en-US")
            target_locale: Target language (e.g., "es-US")

        Returns:
            Localized text
        """
        ...
