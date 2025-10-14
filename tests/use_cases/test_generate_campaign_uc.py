"""
Use Case Tests: GenerateCampaignUC

Simple tests to ensure use case works with adapters.
Following lean-clean methodology: use fakes, focus on behavior.
"""
import pytest
from datetime import datetime

from app.entities.campaign_brief import CampaignBrief, Product
from app.entities.brand_summary import BrandSummary
from app.use_cases.generate_campaign_uc import GenerateCampaignUC
from app.adapters.ai.fake import FakeAIAdapter
from app.adapters.storage.fake import FakeStorageAdapter


def test_generate_campaign_creates_assets():
    """
    Given: A campaign brief and brand
    When: Generate campaign is executed
    Then: Assets are created for all product×aspect×locale combinations
    """
    # GIVEN
    brief = CampaignBrief(
        brief_id="test-001",
        brand_id="test-brand",
        campaign_slogan="Test Slogan",
        target_region="US",
        target_audience="Test audience",
        target_locales=["en-US", "es-US"],
        products=[Product(name="Test Product", palette_words=["modern"])],
        aspects=["1:1", "9:16"],
        created_at=datetime.now(),
    )

    brand = BrandSummary(
        brand_id="test-brand",
        name="Test Brand",
        description="Test description",
        colors=["#FF0000"],
        typography="Arial",
        voice_tone="friendly",
        target_audiences=["Everyone"],
        target_regions=["US"],
        products=["Test Product"],
        campaign_slogans=["Test Slogan"],
        logo_url=None,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    use_case = GenerateCampaignUC(
        ai_adapter=FakeAIAdapter(),
        storage_adapter=FakeStorageAdapter(),
    )

    # WHEN
    assets = use_case.execute(brief, brand)

    # THEN: 1 product × 2 aspects × 2 locales = 4 assets
    assert len(assets) == 4
    assert all(a.product_name == "Test Product" for a in assets)
    assert all(a.image_url for a in assets)  # All have images


def test_generate_campaign_localizes_messages():
    """
    Given: A brief with multiple locales
    When: Generate campaign is executed
    Then: Messages are localized per locale
    """
    # GIVEN
    brief = CampaignBrief(
        brief_id="test-002",
        brand_id="test-brand",
        campaign_slogan="Gift Wellness",
        target_region="US",
        target_audience="Test",
        target_locales=["en-US", "es-US"],
        products=[Product(name="Soap", palette_words=[])],
        aspects=["1:1"],
        created_at=datetime.now(),
    )

    brand = BrandSummary(
        brand_id="test-brand",
        name="Test Brand",
        description="Test",
        colors=["#000000"],
        typography="Arial",
        voice_tone="warm",
        target_audiences=["All"],
        target_regions=["US"],
        products=["Soap"],
        campaign_slogans=["Gift Wellness"],
        logo_url=None,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    use_case = GenerateCampaignUC(
        ai_adapter=FakeAIAdapter(),
        storage_adapter=FakeStorageAdapter(),
    )

    # WHEN
    assets = use_case.execute(brief, brand)

    # THEN: Spanish is localized
    en_asset = next(a for a in assets if a.locale == "en-US")
    es_asset = next(a for a in assets if a.locale == "es-US")

    assert en_asset.message == "Gift Wellness"
    assert es_asset.message == "Regalo Bienestar"  # Localized


def test_generate_campaign_with_asset_reuse():
    """
    Given: An asset repository with existing assets
    When: Generate campaign is executed
    Then: Existing assets are reused when found
    """
    # GIVEN
    from app.entities.creative_asset import CreativeAsset

    # Mock asset repository that returns existing assets
    class FakeAssetRepo:
        def find_existing(self, product_name, aspect_ratio, locale, limit=1):
            # Return existing asset for first combination
            if product_name == "Soap" and aspect_ratio == "1:1" and locale == "en-US":
                return [
                    CreativeAsset(
                        asset_id="existing-001",
                        brand_id="test-brand",
                        brief_id="old-brief",
                        product_name="Soap",
                        audience="Previous audience",
                        locale="en-US",
                        aspect_ratio="1:1",
                        message="Old message",
                        image_url="http://existing.com/image.png",
                        reused=True,
                        generated_at=datetime.now(),
                        meta={},
                    )
                ]
            return []

        def upsert(self, asset, image_bytes=None, tags=None):
            pass  # No-op for test

    brief = CampaignBrief(
        brief_id="test-003",
        brand_id="test-brand",
        campaign_slogan="Test",
        target_region="US",
        target_audience="Test",
        target_locales=["en-US"],
        products=[Product(name="Soap", palette_words=[])],
        aspects=["1:1"],
        created_at=datetime.now(),
    )

    brand = BrandSummary(
        brand_id="test-brand",
        name="Test",
        description="Test",
        colors=["#000000"],
        typography="Arial",
        voice_tone="warm",
        target_audiences=["All"],
        target_regions=["US"],
        products=["Soap"],
        campaign_slogans=["Test"],
        logo_url=None,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    use_case = GenerateCampaignUC(
        ai_adapter=FakeAIAdapter(),
        storage_adapter=FakeStorageAdapter(),
        asset_repository=FakeAssetRepo(),
    )

    # WHEN
    assets = use_case.execute(brief, brand)

    # THEN: Asset is reused
    assert len(assets) == 1
    assert assets[0].reused is True
    assert assets[0].asset_id == "existing-001"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
