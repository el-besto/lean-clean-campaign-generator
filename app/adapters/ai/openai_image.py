"""
OpenAI Image Generation Adapter

Implements IAIAdapter protocol for real image generation via OpenAI API.
Uses gpt-image-1 model (GPT Image Generation).
"""
import base64
from typing import Dict, List
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from app.infrastructure.config import settings


class OpenAIImageAdapter:
    """Real AI adapter using OpenAI API for image generation."""

    def __init__(self, api_key: str = None):
        self.client = OpenAI(api_key=api_key or settings.OPENAI_API_KEY)
        self._aspect_to_size_map = {
            "1:1": "1024x1024",
            "16:9": "1536x1024",
            "9:16": "1024x1536",
        }

    def generate_image(self, prompt: str, aspect_ratio: str) -> bytes:
        """
        Generate hero image from text prompt via OpenAI.

        Args:
            prompt: Image generation prompt (product + brand guidelines)
            aspect_ratio: "1:1", "9:16", or "16:9"

        Returns:
            Image bytes (PNG format)
        """
        size = self._aspect_to_size_map.get(aspect_ratio, "1024x1024")

        response = self.client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size=size,
            n=1,
        )

        # Decode base64 image (b64_json is returned by default)
        image_b64 = response.data[0].b64_json
        return base64.b64decode(image_b64)

    def overlay_text(self, image: bytes, text: str, aspect_ratio: str) -> bytes:
        """
        Add campaign message text overlay to image using Pillow.

        Args:
            image: Base image bytes
            text: Localized campaign slogan
            aspect_ratio: Image dimensions

        Returns:
            Image with text overlay (PNG format)
        """
        # Load image
        img = Image.open(BytesIO(image))
        draw = ImageDraw.Draw(img)

        # Simple text overlay (bottom center)
        # TODO: Use brand fonts, better positioning, background box
        width, height = img.size

        # Try to load a nice font, fall back to default
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
        except:
            font = ImageFont.load_default()

        # Calculate text position (bottom center)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (width - text_width) // 2
        y = height - text_height - 40

        # Draw text with outline for readability
        outline_color = "black"
        text_color = "white"

        # Outline
        for offset_x in [-2, 0, 2]:
            for offset_y in [-2, 0, 2]:
                draw.text((x + offset_x, y + offset_y), text, font=font, fill=outline_color)

        # Main text
        draw.text((x, y), text, font=font, fill=text_color)

        # Convert back to bytes
        output = BytesIO()
        img.save(output, format="PNG")
        return output.getvalue()

    def understand_brand(self, brand_assets: List[str]) -> Dict[str, any]:
        """
        Analyze brand assets to extract brand guidelines.

        NOT IMPLEMENTED: Placeholder for Phase 4 (Claude Vision integration)
        """
        return {
            "colors": [],
            "voice_tone": "professional",
            "typography": "sans-serif",
        }

    def localize(self, text: str, source_locale: str, target_locale: str) -> str:
        """
        Translate text while preserving brand voice.

        NOT IMPLEMENTED: Placeholder for Phase 4 (Claude Multilingual integration)
        Falls back to simple mapping for now.
        """
        # Simple mapping (same as FakeAIAdapter)
        localization_map = {
            "en-US": {
                "Gift Wellness": "Gift Wellness",
                "Pure Nature": "Pure Nature",
            },
            "es-US": {
                "Gift Wellness": "Regalo Bienestar",
                "Pure Nature": "Naturaleza Pura",
            },
        }

        if target_locale in localization_map:
            return localization_map[target_locale].get(text, text)
        return text
