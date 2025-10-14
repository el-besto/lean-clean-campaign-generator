"""
Campaign Orchestrator

Coordinates the complete campaign generation workflow:
1. Load brand from repository
2. Generate campaign assets (use case)
3. Validate assets (use case)
4. Return summary results
"""
from typing import Dict, Any

from app.entities.campaign_brief import CampaignBrief
from app.use_cases.generate_campaign_uc import GenerateCampaignUC
from app.use_cases.validate_campaign_uc import ValidateCampaignUC


class CampaignOrchestrator:
    """
    Orchestrates campaign generation workflow.

    Coordinates use cases and infrastructure components.
    """

    def __init__(
        self,
        generate_uc: GenerateCampaignUC,
        validate_uc: ValidateCampaignUC,
        brand_repository,
    ):
        self.generate_uc = generate_uc
        self.validate_uc = validate_uc
        self.brand_repository = brand_repository

    def generate_campaign(self, brief: CampaignBrief) -> Dict[str, Any]:
        """
        Execute complete campaign generation workflow.

        Args:
            brief: Campaign brief (products, locales, aspects)

        Returns:
            Dict with assets, validation results, and summary
        """
        # Step 1: Load brand
        brand = self.brand_repository.get_by_id(brief.brand_id)
        if not brand:
            raise ValueError(f"Brand not found: {brief.brand_id}")

        # Step 2: Generate assets
        assets = self.generate_uc.execute(brief, brand)

        # Step 3: Validate assets
        validation_results = self.validate_uc.execute(assets)

        # Step 4: Build summary
        validation_failed = sum(1 for r in validation_results if not r.is_valid)
        validation_passed = len(validation_results) - validation_failed

        return {
            "success": True,
            "assets": assets,
            "validation_results": validation_results,
            "summary": {
                "total_assets": len(assets),
                "validation_passed": validation_passed,
                "validation_failed": validation_failed,
                "brief_id": brief.brief_id,
                "brand_id": brief.brand_id,
            },
        }
