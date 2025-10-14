"""
Fake AI Adapter for Testing

Returns deterministic placeholder data without external API calls.
Enables fast testing and demo without API keys.
"""
from typing import Dict, List


class FakeAIAdapter:
    """
    Fake AI adapter implementing IAIAdapter protocol.

    Returns deterministic results for:
    - Image generation (placeholder PNGs)
    - Text overlay (simulated)
    - Brand understanding (hardcoded guidelines)
    - Localization (simple mapping)
    """

    def __init__(self):
        self.call_count = 0
        self.localization_map = {
            "en-US": {
                "Gift Wellness": "Gift Wellness",
                "Pure Nature": "Pure Nature",
            },
            "es-US": {
                "Gift Wellness": "Regalo Bienestar",
                "Pure Nature": "Naturaleza Pura",
            },
        }

    def generate_image(self, prompt: str, aspect_ratio: str) -> bytes:
        """Generate placeholder image (1x1 PNG)."""
        self.call_count += 1
        # Return minimal valid PNG (1x1 transparent pixel)
        # In real implementation, would call OpenAI DALL-E 3
        return self._create_placeholder_png(aspect_ratio)

    def overlay_text(self, image: bytes, text: str, aspect_ratio: str) -> bytes:
        """Simulate text overlay (returns image unchanged)."""
        self.call_count += 1
        # In real implementation, would use PIL or OpenAI API
        return image  # Fake: just return image as-is

    def understand_brand(self, brand_assets: List[str]) -> Dict[str, any]:
        """Return hardcoded brand guidelines."""
        self.call_count += 1
        # In real implementation, would call Claude Vision API
        return {
            "colors": ["#8B7355", "#E6D5B8", "#4A6741"],
            "voice_tone": "warm, natural, trustworthy",
            "typography": "Montserrat",
        }

    def localize(self, text: str, source_locale: str, target_locale: str) -> str:
        """Localize text using simple mapping."""
        self.call_count += 1
        # In real implementation, would call Claude Multilingual API
        if target_locale in self.localization_map:
            return self.localization_map[target_locale].get(text, text)
        return text

    def _create_placeholder_png(self, aspect_ratio: str) -> bytes:
        """Create minimal valid PNG (1x1 transparent pixel)."""
        # PNG header + minimal IDAT chunk (1x1 transparent pixel)
        return bytes.fromhex(
            "89504e470d0a1a0a"  # PNG signature
            "0000000d49484452"  # IHDR chunk
            "0000000100000001"  # 1x1 dimensions
            "0806000000"  # Bit depth 8, color type 6 (RGBA)
            "1f15c489"  # CRC
            "0000000a49444154"  # IDAT chunk
            "78da62000000020001"  # Compressed image data
            "e221bc33"  # CRC
            "0000000049454e44"  # IEND chunk
            "ae426082"  # CRC
        )
