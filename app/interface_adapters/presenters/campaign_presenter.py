"""
Campaign Presenter

Formats orchestrator results for display:
- CLI text output
- UI-friendly JSON
- Summary reports
"""
from typing import Dict, Any, List
from app.entities.creative_asset import CreativeAsset
from app.entities.validation_result import ValidationResult


class CampaignPresenter:
    """Formats campaign generation results for different outputs."""

    @staticmethod
    def format_summary(result: Dict[str, Any]) -> str:
        """
        Format result as text summary for CLI.

        Args:
            result: Orchestrator result dict

        Returns:
            Formatted text summary
        """
        summary = result["summary"]
        assets = result["assets"]

        output = [
            "\n" + "=" * 60,
            "CAMPAIGN GENERATION SUMMARY",
            "=" * 60,
            "",
            f"Brief ID: {summary['brief_id']}",
            f"Brand ID: {summary['brand_id']}",
            "",
            f"Total Assets Generated: {summary['total_assets']}",
            f"  ✓ Validation Passed: {summary['validation_passed']}",
            f"  ✗ Validation Failed: {summary['validation_failed']}",
            "",
            "Assets by Product:",
        ]

        # Group by product
        products = {}
        for asset in assets:
            if asset.product_name not in products:
                products[asset.product_name] = []
            products[asset.product_name].append(asset)

        for product, product_assets in products.items():
            output.append(f"  • {product}: {len(product_assets)} assets")
            locales = {}
            for asset in product_assets:
                if asset.locale not in locales:
                    locales[asset.locale] = 0
                locales[asset.locale] += 1
            for locale, count in locales.items():
                output.append(f"    - {locale}: {count}")

        output.append("")
        output.append("=" * 60)
        output.append("")

        return "\n".join(output)

    @staticmethod
    def format_assets_list(assets: List[CreativeAsset]) -> str:
        """Format assets as detailed list."""
        output = ["\nGenerated Assets:"]
        for i, asset in enumerate(assets, 1):
            output.append(
                f"  {i}. [{asset.product_name}] {asset.aspect_ratio} / {asset.locale}"
            )
            output.append(f"     Message: \"{asset.message}\"")
            output.append(f"     Path: {asset.image_url}")
        return "\n".join(output)

    @staticmethod
    def format_validation_report(results: List[ValidationResult]) -> str:
        """Format validation results."""
        output = ["\nValidation Report:"]

        failed_results = [r for r in results if not r.is_valid]
        if not failed_results:
            output.append("  ✓ All assets passed validation")
            return "\n".join(output)

        output.append(f"  ✗ {len(failed_results)} assets failed validation:")
        for result in failed_results:
            output.append(f"\n  Asset: {result.asset_id}")
            for issue in result.issues:
                output.append(f"    [{issue.severity.upper()}] {issue.message}")
                if issue.fix_suggestion:
                    output.append(f"    → {issue.fix_suggestion}")

        return "\n".join(output)
