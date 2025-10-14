"""
Page 1: Generate Campaign

Interactive campaign brief form with real-time generation.
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
)

st.set_page_config(page_title="Generate Campaign", page_icon="🎨", layout="wide")

st.header("🎨 Generate Campaign")

# Sidebar: Campaign Brief Form
st.sidebar.header("Campaign Brief")

use_real = st.sidebar.checkbox(
    "Use real adapters",
    value=False,
    help="Toggle between fake (testing) and real (OpenAI + MinIO + Weaviate) adapters",
)

if use_real:
    st.sidebar.info("⚠️ Real adapters enabled. Requires:\n- Docker services running\n- OPENAI_API_KEY set")
else:
    st.sidebar.info("ℹ️ Using fake adapters (testing mode)")

brand_id = st.sidebar.selectbox("Brand", ["natural-suds-co"])
campaign_slogan = st.sidebar.text_input("Campaign Slogan", value="Gift Wellness")
target_region = st.sidebar.text_input("Target Region", value="North America")
target_audience = st.sidebar.text_input("Target Audience", value="Gift shoppers 25-45")

st.sidebar.subheader("Locales")
locale_en = st.sidebar.checkbox("English (en-US)", value=True)
locale_es = st.sidebar.checkbox("Spanish (es-US)", value=True)
locales = []
if locale_en:
    locales.append("en-US")
if locale_es:
    locales.append("es-US")

st.sidebar.subheader("Products")
num_products = st.sidebar.number_input("Number of Products", min_value=1, max_value=5, value=2)
products = []
for i in range(int(num_products)):
    product_name = st.sidebar.text_input(
        f"Product {i+1} Name",
        value=["Lavender Soap", "Citrus Shower Gel"][i] if i < 2 else f"Product {i+1}",
        key=f"product_{i}",
    )
    if product_name:
        products.append(Product(name=product_name, palette_words=["vibrant", "modern"]))

st.sidebar.subheader("Aspect Ratios")
aspect_1x1 = st.sidebar.checkbox("Square (1:1)", value=True)
aspect_9x16 = st.sidebar.checkbox("Story (9:16)", value=True)
aspect_16x9 = st.sidebar.checkbox("Landscape (16:9)", value=False)
aspects = []
if aspect_1x1:
    aspects.append("1:1")
if aspect_9x16:
    aspects.append("9:16")
if aspect_16x9:
    aspects.append("16:9")

# Main: Generate Campaign
if st.sidebar.button("Generate Campaign", type="primary"):
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

            generate_uc = GenerateCampaignUC(ai_adapter, storage_adapter)
            validate_uc = ValidateCampaignUC()
            orchestrator = CampaignOrchestrator(generate_uc, validate_uc, brand_repo)

            result = orchestrator.generate_campaign(brief)

        # Store in session state
        st.session_state["result"] = result
        st.session_state["use_real"] = use_real

# Display Results
if "result" in st.session_state:
    result = st.session_state["result"]
    use_real_for_display = st.session_state.get("use_real", False)

    # Summary
    st.header("Campaign Summary")
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
    st.info("👈 Configure your campaign in the sidebar and click **Generate Campaign** to get started")

    st.subheader("🎯 Quick Demo")
    st.markdown("""
    1. Keep default settings in sidebar
    2. Click **Generate Campaign**
    3. View 8 localized assets (2 products × 2 locales × 2 aspects)
    4. See Spanish localization: "Regalo Bienestar"
    """)
