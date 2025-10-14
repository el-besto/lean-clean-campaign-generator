"""
Shared Streamlit UI utilities

Helper functions for file upload and brief parsing.
"""
import io
import json
import yaml
import hashlib
from typing import Tuple, Dict, List
from datetime import datetime
from io import BytesIO
from colorthief import ColorThief

from app.entities.campaign_brief import CampaignBrief, Product
from app.entities.creative_asset import CreativeAsset
from app.infrastructure.repositories.asset.weaviate import WeaviateAssetRepository
from app.adapters.storage.minio import MinIOStorageAdapter


def parse_brief_file(upload) -> Tuple[CampaignBrief, dict]:
    """
    Parse uploaded brief file (YAML or JSON) into CampaignBrief entity.

    Args:
        upload: Streamlit UploadedFile object

    Returns:
        Tuple of (CampaignBrief entity, raw dict data)
    """
    raw = upload.getvalue()

    # Parse based on file extension
    if upload.name.endswith((".yml", ".yaml")):
        data = yaml.safe_load(io.BytesIO(raw))
    else:
        data = json.loads(raw.decode("utf-8"))

    # Extract products
    products = []
    for p in data.get("products", []):
        products.append(Product(
            name=p["name"],
            palette_words=p.get("palette_words", p.get("paletteWords", []))
        ))

    # Build brief
    brief = CampaignBrief(
        brief_id=data.get("brief_id", f"upload-{datetime.now().strftime('%Y%m%d-%H%M%S')}"),
        brand_id=data.get("brand_id", "natural-suds-co"),
        campaign_slogan=data.get("campaign_slogan", data.get("campaign_message", "Gift Wellness")),
        target_region=data.get("target_region", "North America"),
        target_audience=data.get("target_audience", "Gift shoppers 25-45"),
        target_locales=data.get("target_locales", data.get("locales", ["en-US"])),
        products=products,
        aspects=data.get("aspects", ["1:1", "9:16", "16:9"]),
        created_at=datetime.now(),
    )

    return brief, data


def upload_seed_assets(
    brand_id: str,
    product_name: str,
    uploaded_files: List,
    use_real: bool = True,
) -> Dict:
    """
    Upload seed images to MinIO and index in Weaviate.

    Args:
        brand_id: Brand identifier
        product_name: Product name for these assets
        uploaded_files: List of Streamlit UploadedFile objects
        use_real: Use real adapters (MinIO + Weaviate)

    Returns:
        Dict with seed_count and seeded assets list
    """
    if not use_real:
        return {"seed_count": 0, "seeded": [], "error": "Real adapters required for upload"}

    storage = MinIOStorageAdapter()
    asset_repo = WeaviateAssetRepository()

    seeded = []
    for upload in uploaded_files:
        raw = upload.getvalue()

        # Extract color palette
        try:
            ct = ColorThief(BytesIO(raw))
            palette_rgb = ct.get_palette(color_count=5)
            palette_hex = [f"#{r:02x}{g:02x}{b:02x}" for (r, g, b) in palette_rgb]
        except Exception:
            palette_hex = []

        # Generate asset ID
        asset_id = f"seed-{hashlib.sha1(raw).hexdigest()[:8]}"

        # Save to MinIO
        key = f"{brand_id}/{product_name}/seeds/{upload.name}"
        image_url = storage.save(key, raw)

        # Create asset entity
        asset = CreativeAsset(
            asset_id=asset_id,
            brand_id=brand_id,
            brief_id="seed",
            product_name=product_name,
            locale="en-US",
            aspect_ratio="unknown",  # Can detect from image dimensions if needed
            message="Seed asset",
            image_url=image_url,
            validation_status="approved",
        )

        # Index in Weaviate with image bytes for vectorization
        asset_repo.upsert(
            asset,
            image_bytes=raw,
            tags=["seed", "uploaded"],
            palette=palette_hex,
        )

        seeded.append({
            "filename": upload.name,
            "asset_id": asset_id,
            "url": image_url,
            "palette": palette_hex,
        })

    return {"seed_count": len(seeded), "seeded": seeded}
