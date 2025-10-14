"""
Seed Brand Data to Weaviate

Utility script to populate Weaviate with example brand data.
Run after starting Weaviate: make up && python tools/seed_brand.py
"""
from datetime import datetime
from app.entities.brand_summary import BrandSummary
from app.infrastructure.repositories.brand.weaviate import WeaviateBrandRepository


def seed_example_brand():
    """Seed Natural Suds Co. brand data to Weaviate."""
    print("Connecting to Weaviate...")
    repo = WeaviateBrandRepository()

    brand = BrandSummary(
        brand_id="natural-suds-co",
        name="Natural Suds Co.",
        description="Organic personal care products focusing on natural ingredients and sustainable practices",
        colors=["#8B7355", "#E6D5B8", "#4A6741"],
        typography="Montserrat",
        voice_tone="warm, natural, trustworthy",
        target_audiences=["Health-conscious millennials", "Eco-friendly shoppers"],
        target_regions=["North America", "Europe"],
        products=["Lavender Soap", "Citrus Shower Gel", "Rose Hand Cream"],
        campaign_slogans=["Pure Nature", "Wellness Naturally", "Gift Wellness"],
        logo_url=None,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    print(f"Inserting brand: {brand.name} ({brand.brand_id})")
    repo.upsert(brand)
    print(f"✅ Seeded brand: {brand.name} ({brand.brand_id})")

    # Verify
    print("\nVerifying...")
    retrieved = repo.get_by_id(brand.brand_id)
    if retrieved:
        print(f"✅ Verified: Found brand '{retrieved.name}'")
    else:
        print("❌ Error: Could not retrieve brand after insertion")


if __name__ == "__main__":
    try:
        seed_example_brand()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure Weaviate is running: make up")
        exit(1)
