"""
Validate Campaign Use Case

Business logic for campaign validation:
- Legal content checks (prohibited words)
- Brand compliance checks (stubbed for PoC)
"""
from typing import List

from app.entities.creative_asset import CreativeAsset
from app.entities.validation_result import ValidationResult, ValidationStatus, ValidationIssue


class ValidateCampaignUC:
    """Use case: Validate campaign assets."""

    PROHIBITED_WORDS = [
        "guarantee",
        "miracle",
        "cure",
        "free",  # Unless truly free
    ]

    def execute(self, assets: List[CreativeAsset]) -> List[ValidationResult]:
        """
        Validate list of assets.

        Args:
            assets: List of CreativeAsset entities

        Returns:
            List of ValidationResult entities
        """
        results = []
        for asset in assets:
            result = self._validate_asset(asset)
            results.append(result)
        return results

    def _validate_asset(self, asset: CreativeAsset) -> ValidationResult:
        """Validate single asset."""
        issues = []
        checks_run = ["prohibited_words"]

        # Check 1: Prohibited words
        for word in self.PROHIBITED_WORDS:
            if word.lower() in asset.message.lower():
                issues.append(ValidationIssue(
                    check_name="prohibited_words",
                    severity="error",
                    message=f"Prohibited word detected: '{word}'",
                    fix_suggestion=f"Remove or rephrase to avoid '{word}'",
                ))

        # Check 2: Brand compliance (stubbed)
        checks_run.append("brand_compliance")
        # TODO: Implement logo presence, color usage checks

        # Determine status
        failed_count = len([i for i in issues if i.severity == "error"])
        passed_count = len(checks_run) - failed_count
        status = ValidationStatus.PASSED if failed_count == 0 else ValidationStatus.FAILED

        return ValidationResult(
            asset_id=asset.asset_id,
            status=status,
            checks_run=checks_run,
            issues=issues,
            passed_count=passed_count,
            failed_count=failed_count,
        )
