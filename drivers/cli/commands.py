"""
CLI Driver for Campaign Generator

Typer-based command-line interface for generating campaigns.
"""
import typer
from typing import List
from pathlib import Path
from datetime import datetime

from app.entities.campaign_brief import CampaignBrief, Product
from app.use_cases.generate_campaign_uc import GenerateCampaignUC
from app.use_cases.validate_campaign_uc import ValidateCampaignUC
from app.interface_adapters.orchestrators.campaign_orchestrator import CampaignOrchestrator
from app.interface_adapters.presenters.campaign_presenter import CampaignPresenter
from app.infrastructure.factories import (
    create_ai_adapter,
    create_storage_adapter,
    create_brand_repository,
)

app = typer.Typer(
    name="campaign-generator",
    help="AI-driven creative automation for social ad campaigns",
)


def build_orchestrator(use_real: bool = False) -> CampaignOrchestrator:
    """
    Build orchestrator with specified adapter implementations.

    Args:
        use_real: If True, use real adapters (OpenAI, MinIO, Weaviate);
                  else use fake adapters (for testing)

    Returns:
        CampaignOrchestrator with injected dependencies
    """
    ai_adapter = create_ai_adapter(use_real=use_real)
    storage_adapter = create_storage_adapter(use_real=use_real)
    brand_repo = create_brand_repository(use_real=use_real)

    generate_uc = GenerateCampaignUC(ai_adapter, storage_adapter)
    validate_uc = ValidateCampaignUC()

    return CampaignOrchestrator(generate_uc, validate_uc, brand_repo)


@app.command()
def generate(
    brand_id: str = typer.Option("natural-suds-co", "--brand", "-b", help="Brand ID"),
    campaign_slogan: str = typer.Option("Gift Wellness", "--slogan", "-s", help="Campaign slogan"),
    products: List[str] = typer.Option(
        ["Lavender Soap", "Citrus Shower Gel"],
        "--product",
        "-p",
        help="Product names (repeat for multiple)",
    ),
    locales: List[str] = typer.Option(
        ["en-US", "es-US"],
        "--locale",
        "-l",
        help="Target locales (repeat for multiple)",
    ),
    aspects: List[str] = typer.Option(
        ["1:1", "9:16", "16:9"],
        "--aspect",
        "-a",
        help="Aspect ratios (repeat for multiple)",
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output"),
    real: bool = typer.Option(
        False,
        "--real",
        help="Use real adapters (OpenAI, MinIO, Weaviate). Requires: docker services running + OPENAI_API_KEY set",
    ),
):
    """
    Generate localized campaign creative assets.

    Example:
        campaign-generator generate \\
            --brand natural-suds-co \\
            --slogan "Gift Wellness" \\
            --product "Lavender Soap" \\
            --product "Citrus Gel" \\
            --locale en-US --locale es-US \\
            --aspect 1:1 --aspect 9:16

        # With real adapters:
        campaign-generator generate --real \\
            --brand natural-suds-co \\
            --slogan "Gift Wellness"
    """
    adapter_mode = "real (OpenAI + MinIO + Weaviate)" if real else "fake (testing mode)"
    typer.echo("🚀 Campaign Generator - Pragmatic Clean Architecture Demo")
    typer.echo(f"   Adapter mode: {adapter_mode}\n")

    # Build campaign brief
    brief = CampaignBrief(
        brief_id=f"cli-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        brand_id=brand_id,
        campaign_slogan=campaign_slogan,
        target_region="North America",
        target_audience="General",
        target_locales=list(locales),
        products=[Product(name=p, palette_words=["clean", "natural"]) for p in products],
        aspects=list(aspects),
        created_at=datetime.now(),
    )

    typer.echo(f"📋 Campaign Brief: {brief.brief_id}")
    typer.echo(f"   Brand: {brand_id}")
    typer.echo(f"   Slogan: {campaign_slogan}")
    typer.echo(f"   Products: {len(products)}")
    typer.echo(f"   Locales: {len(locales)}")
    typer.echo(f"   Aspects: {len(aspects)}")
    typer.echo(f"   Expected Assets: {brief.total_assets_required}\n")

    # Generate campaign
    typer.echo("⚙️  Generating campaign...")
    orchestrator = build_orchestrator(use_real=real)

    try:
        result = orchestrator.generate_campaign(brief)

        # Format and display results
        presenter = CampaignPresenter()
        summary = presenter.format_summary(result)
        typer.echo(summary)

        if verbose:
            assets_list = presenter.format_assets_list(result["assets"])
            typer.echo(assets_list)

            validation_report = presenter.format_validation_report(result["validation_results"])
            typer.echo(validation_report)

        typer.echo("\n✅ Campaign generation complete!")
        if real:
            typer.echo(f"💾 Assets stored in MinIO (S3-compatible storage)")
        else:
            typer.echo(f"💾 Assets stored in memory (using FakeStorageAdapter)")

    except Exception as e:
        typer.echo(f"\n❌ Error: {e}", err=True)
        raise typer.Exit(code=1)


@app.command()
def demo():
    """Run a quick demo with example campaign."""
    typer.echo("🎬 Running demo campaign...\n")

    # Build example brief
    brief = CampaignBrief(
        brief_id="demo-001",
        brand_id="natural-suds-co",
        campaign_slogan="Pure Wellness",
        target_region="North America",
        target_audience="Health-conscious shoppers",
        target_locales=["en-US", "es-US"],
        products=[
            Product(name="Lavender Soap", palette_words=["calming", "purple"]),
            Product(name="Citrus Gel", palette_words=["energizing", "orange"]),
        ],
        aspects=["1:1", "9:16"],
        created_at=datetime.now(),
    )

    typer.echo(f"📊 Demo Configuration:")
    typer.echo(f"   Products: 2 (Lavender Soap, Citrus Gel)")
    typer.echo(f"   Locales: 2 (en-US, es-US)")
    typer.echo(f"   Aspects: 2 (1:1, 9:16)")
    typer.echo(f"   Total Assets: {brief.total_assets_required}\n")

    orchestrator = build_orchestrator()
    result = orchestrator.generate_campaign(brief)

    presenter = CampaignPresenter()
    summary = presenter.format_summary(result)
    typer.echo(summary)

    typer.echo("\n💡 Tip: Run with --verbose for detailed asset listing")
    typer.echo("💡 Tip: Try 'campaign-generator generate --help' for custom campaigns")


if __name__ == "__main__":
    app()
