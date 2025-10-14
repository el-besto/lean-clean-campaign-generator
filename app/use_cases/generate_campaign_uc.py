"""
Generate Campaign Use Case

Business logic for campaign generation:
1. Localize campaign slogan
2. For each product × aspect × locale:
   a. Generate hero image
   b. Add text overlay
   c. Create CreativeAsset entity
3. Return list of assets
"""
from typing import List
from datetime import datetime
import hashlib

from app.entities.campaign_brief import CampaignBrief
from app.entities.brand_summary import BrandSummary
from app.entities.creative_asset import CreativeAsset


class GenerateCampaignUC:
    """Use case: Generate campaign creative assets."""

    def __init__(
        self,
        ai_adapter,
        storage_adapter,
    ):
        self.ai_adapter = ai_adapter
        self.storage_adapter = storage_adapter

    def execute(
        self,
        brief: CampaignBrief,
        brand: BrandSummary,
    ) -> List[CreativeAsset]:
        """
        Generate campaign assets.

        Args:
            brief: Campaign brief (products, aspects, locales)
            brand: Brand guidelines (colors, voice, tone)

        Returns:
            List of CreativeAsset entities
        """
        assets = []

        # Step 1: Localize campaign slogan for each locale
        localized_slogans = self._localize_slogans(brief, brand)

        # Step 2: Generate assets for each combination
        for product in brief.products:
            for aspect in brief.aspects:
                for locale in brief.target_locales:
                    asset = self._generate_asset(
                        brief=brief,
                        brand=brand,
                        product=product,
                        aspect=aspect,
                        locale=locale,
                        slogan=localized_slogans[locale],
                    )
                    assets.append(asset)

        return assets

    def _localize_slogans(self, brief: CampaignBrief, brand: BrandSummary) -> dict:
        """Localize campaign slogan for each target locale."""
        slogans = {}
        for locale in brief.target_locales:
            slogans[locale] = self.ai_adapter.localize(
                text=brief.campaign_slogan,
                source_locale="en-US",
                target_locale=locale,
            )
        return slogans

    def _generate_asset(
        self,
        brief: CampaignBrief,
        brand: BrandSummary,
        product,
        aspect: str,
        locale: str,
        slogan: str,
    ) -> CreativeAsset:
        """Generate single creative asset."""
        # Generate image prompt
        prompt = self._create_prompt(brand, product, aspect)

        # Generate hero image
        image_bytes = self.ai_adapter.generate_image(prompt, aspect)

        # Add text overlay
        final_image = self.ai_adapter.overlay_text(image_bytes, slogan, aspect)

        # Save to storage
        asset_id = self._generate_asset_id(brief, product, aspect, locale)
        storage_path = f"{product.name.lower().replace(' ', '-')}/{locale}/{aspect.replace(':', 'x')}/{asset_id}.png"
        saved_path = self.storage_adapter.save(storage_path, final_image)

        # Create entity
        return CreativeAsset(
            asset_id=asset_id,
            brief_id=brief.brief_id,
            brand_id=brand.brand_id,
            product_name=product.name,
            audience=brief.target_audience,
            locale=locale,
            aspect_ratio=aspect,
            message=slogan,
            image_url=saved_path,
            reused=False,
            generated_at=datetime.now(),
            meta={
                "validation_status": "passed",  # Stub
                "prompt": prompt,
            },
        )

    def _create_prompt(self, brand: BrandSummary, product, aspect: str) -> str:
        """Create image generation prompt."""
        palette = ", ".join(product.palette_words)
        colors = ", ".join(brand.colors)
        return (
            f"Professional product photography of {product.name}. "
            f"Style: {palette}. Brand colors: {colors}. "
            f"Mood: {brand.voice_tone}. Aspect ratio: {aspect}. "
            f"High quality, commercial, clean background."
        )

    def _generate_asset_id(self, brief, product, aspect: str, locale: str) -> str:
        """Generate deterministic asset ID."""
        data = f"{brief.brief_id}-{product.name}-{aspect}-{locale}"
        return hashlib.md5(data.encode()).hexdigest()[:12]
