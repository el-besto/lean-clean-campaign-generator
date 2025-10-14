"""
Page 1: Generate Campaign

Simple, single-page workflow for campaign generation:
1. Upload brief (optional)
2. Upload seed images (optional)
3. Configure campaign
4. Generate
"""
import streamlit as st
from datetime import datetime
from io import BytesIO
from PIL import Image

from app.entities.campaign_brief import CampaignBrief, Product
from app.use_cases.generate_campaign_uc import GenerateCampaignUC
from app.use_cases.validate_campaign_uc import ValidateCampaignUC
from app.interface_adapters.orchestrators.campaign_orchestrator import CampaignOrchestrator
from app.infrastructure.factories import (
    create_ai_adapter,
    create_storage_adapter,
    create_brand_repository,
    create_asset_repository,
)
from drivers.ui.streamlit.shared import parse_brief_file, upload_seed_assets

st.set_page_config(page_title="Generate Campaign", page_icon="🎨", layout="wide")

st.header("🎨 Generate Campaign")

# ============================================================================
# SECTION 1: CONFIGURATION
# ============================================================================
st.subheader("⚙️ Configuration")

col1, col2 = st.columns([1, 1])

with col1:
    use_real = st.checkbox(
        "Use real adapters (OpenAI + MinIO + Weaviate)",
        value=False,
        help="Requires Docker services running and OPENAI_API_KEY set",
    )

with col2:
    brand_id = st.selectbox("Brand", ["natural-suds-co"])

if use_real:
    st.info("✓ Real adapters enabled. Ensure services are running: `make up`")
else:
    st.info("ℹ️ Using fake adapters (testing mode - no API keys needed)")

st.markdown("---")

# ============================================================================
# SECTION 2: UPLOAD BRIEF (OPTIONAL)
# ============================================================================
st.subheader("📁 Upload Brief (Optional)")

brief_file = st.file_uploader(
    "Upload campaign brief (YAML or JSON)",
    type=["yaml", "yml", "json"],
    help="Auto-populate form below from file",
)

uploaded_brief = None
if brief_file:
    try:
        uploaded_brief, _ = parse_brief_file(brief_file)
        st.success(f"✓ Loaded brief: {uploaded_brief.brief_id}")
    except Exception as e:
        st.error(f"Failed to parse brief: {e}")

st.markdown("---")

# ============================================================================
# SECTION 3: UPLOAD SEED IMAGES (OPTIONAL)
# ============================================================================
if use_real:
    st.subheader("🖼️ Upload Seed Images (Optional)")

    st.markdown("""
    Upload brand asset images (product photos, lifestyle shots) to build your asset library.
    The system will search these before generating new images.
    """)

    col1, col2 = st.columns([2, 1])

    with col1:
        seed_files = st.file_uploader(
            "Select seed images",
            type=["png", "jpg", "jpeg", "webp"],
            accept_multiple_files=True,
            help="Upload brand assets for this campaign",
        )

    with col2:
        seed_product = st.text_input(
            "Product name for seeds",
            value="Lavender Soap",
            help="Which product are these seed images for?",
        )

    if seed_files and st.button("Upload Seeds", key="upload_seeds_btn"):
        with st.spinner(f"Uploading {len(seed_files)} seed image(s)..."):
            try:
                result = upload_seed_assets(
                    brand_id=brand_id,
                    product_name=seed_product,
                    uploaded_files=seed_files,
                    use_real=use_real,
                )

                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success(f"✓ Uploaded {result['seed_count']} seed(s)")

                    # Show preview
                    cols = st.columns(min(4, len(result["seeded"])))
                    for idx, item in enumerate(result["seeded"]):
                        with cols[idx % 4]:
                            st.caption(f"{item['filename']}")
                            st.caption(f"Palette: {', '.join(item['palette'][:2])}")
            except Exception as e:
                st.error(f"Upload failed: {e}")

    st.markdown("---")

# ============================================================================
# SECTION 4: CAMPAIGN CONFIGURATION
# ============================================================================
st.subheader("📝 Campaign Configuration")

# Basic info
col1, col2 = st.columns(2)

with col1:
    campaign_slogan = st.text_input(
        "Campaign Slogan",
        value=uploaded_brief.campaign_slogan if uploaded_brief else "Gift Wellness",
    )
    target_region = st.text_input(
        "Target Region",
        value=uploaded_brief.target_region if uploaded_brief else "North America",
    )

with col2:
    target_audience = st.text_input(
        "Target Audience",
        value=uploaded_brief.target_audience if uploaded_brief else "Gift shoppers 25-45",
    )

# Locales
st.markdown("**Locales**")
col1, col2, col3 = st.columns(3)

default_locales = uploaded_brief.target_locales if uploaded_brief else ["en-US", "es-US"]

with col1:
    locale_en = st.checkbox("English (en-US)", value="en-US" in default_locales)
with col2:
    locale_es = st.checkbox("Spanish (es-US)", value="es-US" in default_locales)

locales = []
if locale_en:
    locales.append("en-US")
if locale_es:
    locales.append("es-US")

# Products
st.markdown("**Products**")
default_products = uploaded_brief.products if uploaded_brief else []
num_products = st.number_input(
    "Number of Products",
    min_value=1,
    max_value=5,
    value=len(default_products) if default_products else 2,
)

products = []
cols = st.columns(int(num_products))

for i in range(int(num_products)):
    with cols[i]:
        default_name = ""
        if default_products and i < len(default_products):
            default_name = default_products[i].name
        elif i < 2:
            default_name = ["Lavender Soap", "Citrus Shower Gel"][i]
        else:
            default_name = f"Product {i+1}"

        product_name = st.text_input(
            f"Product {i+1}",
            value=default_name,
            key=f"product_{i}",
        )
        if product_name:
            palette = default_products[i].palette_words if (default_products and i < len(default_products)) else ["vibrant", "modern"]
            products.append(Product(name=product_name, palette_words=palette))

# Aspect Ratios
st.markdown("**Aspect Ratios**")
col1, col2, col3 = st.columns(3)

default_aspects = uploaded_brief.aspects if uploaded_brief else ["1:1", "9:16"]

with col1:
    aspect_1x1 = st.checkbox("Square (1:1)", value="1:1" in default_aspects)
with col2:
    aspect_9x16 = st.checkbox("Story (9:16)", value="9:16" in default_aspects)
with col3:
    aspect_16x9 = st.checkbox("Landscape (16:9)", value="16:9" in default_aspects)

aspects = []
if aspect_1x1:
    aspects.append("1:1")
if aspect_9x16:
    aspects.append("9:16")
if aspect_16x9:
    aspects.append("16:9")

st.markdown("---")

# ============================================================================
# SECTION 5: GENERATE
# ============================================================================
if st.button("🚀 Generate Campaign", type="primary", use_container_width=True):
    if not locales or not products or not aspects:
        st.error("Please select at least one locale, product, and aspect ratio.")
    else:
        # Create brief
        brief = CampaignBrief(
            brief_id=f"ui-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            brand_id=brand_id,
            campaign_slogan=campaign_slogan,
            target_region=target_region,
            target_audience=target_audience,
            target_locales=locales,
            products=products,
            aspects=aspects,
            created_at=datetime.now(),
        )

        # Generate campaign
        with st.spinner("Generating campaign... This may take a moment."):
            # Create orchestrator with selected adapters
            ai_adapter = create_ai_adapter(use_real=use_real)
            storage_adapter = create_storage_adapter(use_real=use_real)
            brand_repo = create_brand_repository(use_real=use_real)
            asset_repo = create_asset_repository(use_real=use_real)

            generate_uc = GenerateCampaignUC(ai_adapter, storage_adapter, asset_repo)
            validate_uc = ValidateCampaignUC()
            orchestrator = CampaignOrchestrator(generate_uc, validate_uc, brand_repo)

            result = orchestrator.generate_campaign(brief)

        # Store in session state
        st.session_state["result"] = result
        st.session_state["use_real"] = use_real

st.markdown("---")

# ============================================================================
# SECTION 6: RESULTS
# ============================================================================
if "result" in st.session_state:
    result = st.session_state["result"]
    use_real_for_display = st.session_state.get("use_real", False)

    st.header("📊 Campaign Results")

    # Summary
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Assets", result["summary"]["total_assets"])
    col2.metric("Products", result["summary"]["products"])
    col3.metric("Locales", result["summary"]["locales"])
    col4.metric("Aspect Ratios", result["summary"]["aspects"])

    # Validation
    st.subheader("Validation Results")
    passed = result["summary"]["validation_passed"]
    failed = result["summary"]["validation_failed"]
    if failed == 0:
        st.success(f"✅ All {passed} assets passed validation")
    else:
        st.warning(f"⚠️ {failed} assets failed validation, {passed} passed")

    # Assets Gallery
    st.subheader("Generated Assets")
    assets = result["assets"]

    # Group by product
    products_dict = {}
    for asset in assets:
        if asset.product_name not in products_dict:
            products_dict[asset.product_name] = []
        products_dict[asset.product_name].append(asset)

    for product_name, product_assets in products_dict.items():
        with st.expander(f"📦 {product_name} ({len(product_assets)} assets)", expanded=True):
            # Group by locale
            for locale in sorted(set(a.locale for a in product_assets)):
                st.markdown(f"**Locale: {locale}**")
                locale_assets = [a for a in product_assets if a.locale == locale]

                cols = st.columns(min(3, len(locale_assets)))
                for idx, asset in enumerate(locale_assets):
                    with cols[idx % 3]:
                        st.markdown(f"**{asset.aspect_ratio}**")
                        st.markdown(f"*{asset.message}*")

                        # Show reused flag
                        if hasattr(asset, 'reused') and asset.reused:
                            st.caption("♻️ Reused from asset library")

                        # Display image if using real adapters
                        if use_real_for_display:
                            try:
                                storage = create_storage_adapter(use_real=True)
                                # Extract path from S3 URI (s3://bucket/path -> path)
                                path = asset.image_url.replace(f"s3://{storage.bucket}/", "")
                                image_bytes = storage.load(path)
                                image = Image.open(BytesIO(image_bytes))
                                st.image(image, use_container_width=True)
                            except Exception as e:
                                st.error(f"Failed to load image: {e}")
                        else:
                            st.caption(f"Asset ID: {asset.asset_id}")
                            st.caption(f"Path: {asset.image_url}")
                            st.info("Enable real adapters to display images")

    # Raw Data
    with st.expander("📊 Raw Data (JSON)", expanded=False):
        st.json({
            "brief_id": result["brief_id"],
            "brand_id": result["brand_id"],
            "summary": result["summary"],
            "generated_at": result["generated_at"],
        })
else:
    st.info("""
    👆 Configure your campaign above and click **Generate Campaign** to get started.

    **Quick Start:**
    1. Keep default settings (fake adapters)
    2. Click "Generate Campaign"
    3. View 8 localized assets (2 products × 2 locales × 2 aspects)
    """)
