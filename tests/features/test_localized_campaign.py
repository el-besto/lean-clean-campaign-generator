"""
Feature Test: Localized Campaign Generation

Tests the complete workflow:
1. Load campaign brief (YAML)
2. Load brand guidelines
3. Generate localized assets (2 products × 3 aspects × 2 locales = 12 assets)
4. Validate legal compliance
5. Save organized output

Uses ONLY fakes (no external dependencies, <1s execution).
"""
import pytest
from datetime import datetime

from app.entities.campaign_brief import CampaignBrief, Product
from app.entities.brand_summary import BrandSummary


@pytest.mark.acceptance
def test_localized_campaign_generation():
    """
    Given: A campaign brief for 2 products, 3 aspect ratios, 2 locales
    When: I run campaign generation
    Then: System generates 12 localized creative assets
    And: Assets are organized by product/locale/aspect
    And: All assets pass validation
    """
    # GIVEN: Campaign brief
    brief = CampaignBrief(
        brief_id="holiday-2025-01",
        brand_id="natural-suds-co",
        campaign_slogan="Gift Wellness",
        target_region="North America",
        target_audience="Gift shoppers 25-45",
        target_locales=["en-US", "es-US"],
        products=[
            Product(name="Lavender Soap", palette_words=["calming", "purple", "natural"]),
            Product(name="Citrus Shower Gel", palette_words=["energizing", "orange", "fresh"]),
        ],
        aspects=["1:1", "9:16", "16:9"],
        created_at=datetime.now(),
    )

    # GIVEN: Brand guidelines
    brand = BrandSummary(
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

    # GIVEN: Dependencies (fake adapters)
    from app.adapters.ai.fake import FakeAIAdapter
    from app.adapters.storage.fake import FakeStorageAdapter
    from app.infrastructure.repositories.brand.in_memory import InMemoryBrandRepository
    from app.use_cases.generate_campaign_uc import GenerateCampaignUC
    from app.use_cases.validate_campaign_uc import ValidateCampaignUC
    from app.interface_adapters.orchestrators.campaign_orchestrator import CampaignOrchestrator

    ai_adapter = FakeAIAdapter()
    storage_adapter = FakeStorageAdapter()
    brand_repo = InMemoryBrandRepository()

    # WHEN: Generate campaign
    generate_uc = GenerateCampaignUC(
        ai_adapter=ai_adapter,
        storage_adapter=storage_adapter,
    )
    validate_uc = ValidateCampaignUC()
    orchestrator = CampaignOrchestrator(generate_uc, validate_uc, brand_repo)
    result = orchestrator.generate_campaign(brief)
    assets = result["assets"]

    # THEN: 12 assets generated (2 products × 3 aspects × 2 locales)
    assert len(assets) == 12
    assert result["summary"]["total_assets"] == 12

    # THEN: Assets organized correctly
    lavender_assets = [a for a in assets if a.product_name == "Lavender Soap"]
    assert len(lavender_assets) == 6  # 3 aspects × 2 locales

    # THEN: Localized messages
    en_assets = [a for a in assets if a.locale == "en-US"]
    es_assets = [a for a in assets if a.locale == "es-US"]
    assert len(en_assets) == 6
    assert len(es_assets) == 6
    assert any("Regalo Bienestar" in a.message for a in es_assets)

    # THEN: All assets validated
    assert result["summary"]["validation_failed"] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
