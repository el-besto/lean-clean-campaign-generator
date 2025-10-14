"""
Generate Campaign Use Case

Business logic for campaign generation:
1. Search Weaviate for existing similar assets (reuse if found)
2. Localize campaign slogan
3. For each product × aspect × locale:
   a. Check if similar asset exists in Weaviate
   b. If found: reuse existing asset
   c. If not: generate hero image, add text overlay, save
4. Return list of assets
"""
from typing import List, Optional
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
        asset_repository=None,
    ):
        self.ai_adapter = ai_adapter
        self.storage_adapter = storage_adapter
        self.asset_repository = asset_repository  # Optional: Weaviate asset search

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
        """
        Generate single creative asset.

        Searches Weaviate for existing similar assets first.
        If found, reuses existing asset. If not, generates new one.
        """
        # Step 1: Check Weaviate for existing similar assets
        if self.asset_repository:
            existing = self.asset_repository.find_existing(
                product_name=product.name,
                aspect_ratio=aspect,
                locale=locale,
                limit=1,
            )
            if existing:
                # Reuse existing asset (update metadata)
                reused_asset = existing[0]
                reused_asset.brief_id = brief.brief_id
                reused_asset.message = slogan
                reused_asset.reused = True
                return reused_asset

        # Step 2: No existing asset found - generate new one
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
        asset = CreativeAsset(
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

        # Step 3: Index new asset in Weaviate for future reuse
        if self.asset_repository:
            self.asset_repository.upsert(
                asset,
                image_bytes=final_image,
                tags=["generated"],
            )

        return asset

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
