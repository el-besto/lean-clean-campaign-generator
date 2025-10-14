"""
Shared Streamlit UI utilities

Helper functions for file upload and brief parsing.
"""
import io
import json
import yaml
from typing import Tuple, Dict, List
from datetime import datetime

from app.entities.campaign_brief import CampaignBrief, Product


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
