"""
Streamlit UI for Campaign Generator

Interactive dashboard for campaign generation and visualization.
"""
import streamlit as st
from datetime import datetime

from app.entities.campaign_brief import CampaignBrief, Product
from app.adapters.ai.fake import FakeAIAdapter
from app.adapters.storage.fake import FakeStorageAdapter
from app.infrastructure.repositories.brand.in_memory import InMemoryBrandRepository
from app.use_cases.generate_campaign_uc import GenerateCampaignUC
from app.use_cases.validate_campaign_uc import ValidateCampaignUC
from app.interface_adapters.orchestrators.campaign_orchestrator import CampaignOrchestrator


# Page config
st.set_page_config(
    page_title="Campaign Generator PoC",
    page_icon="🎨",
    layout="wide",
)

# Title
st.title("🎨 Campaign Generator")
st.markdown("**Pragmatic Clean Architecture Demo** - AI-driven creative automation for localized campaigns")
st.markdown("---")


@st.cache_resource
def build_orchestrator():
    """Build orchestrator with fake adapters."""
    ai_adapter = FakeAIAdapter()
    storage_adapter = FakeStorageAdapter()
    brand_repo = InMemoryBrandRepository()

    generate_uc = GenerateCampaignUC(ai_adapter, storage_adapter)
    validate_uc = ValidateCampaignUC()

    return CampaignOrchestrator(generate_uc, validate_uc, brand_repo)


# Sidebar - Campaign Configuration
st.sidebar.header("📋 Campaign Configuration")

brand_id = st.sidebar.text_input("Brand ID", value="natural-suds-co")
campaign_slogan = st.sidebar.text_input("Campaign Slogan", value="Gift Wellness")

st.sidebar.subheader("Products")
product1 = st.sidebar.text_input("Product 1", value="Lavender Soap")
product2 = st.sidebar.text_input("Product 2", value="Citrus Shower Gel")
products = [p for p in [product1, product2] if p]

st.sidebar.subheader("Target Locales")
locale_en = st.sidebar.checkbox("English (en-US)", value=True)
locale_es = st.sidebar.checkbox("Spanish (es-US)", value=True)
locales = []
if locale_en:
    locales.append("en-US")
if locale_es:
    locales.append("es-US")

st.sidebar.subheader("Aspect Ratios")
aspect_1x1 = st.sidebar.checkbox("Square (1:1)", value=True)
aspect_9x16 = st.sidebar.checkbox("Portrait (9:16)", value=True)
aspect_16x9 = st.sidebar.checkbox("Landscape (16:9)", value=False)
aspects = []
if aspect_1x1:
    aspects.append("1:1")
if aspect_9x16:
    aspects.append("9:16")
if aspect_16x9:
    aspects.append("16:9")

# Calculate expected assets
expected_assets = len(products) * len(locales) * len(aspects)
st.sidebar.markdown(f"**Expected Assets:** {expected_assets}")

generate_button = st.sidebar.button("🚀 Generate Campaign", type="primary", use_container_width=True)

# Main content
if generate_button:
    if not products:
        st.error("Please add at least one product")
    elif not locales:
        st.error("Please select at least one locale")
    elif not aspects:
        st.error("Please select at least one aspect ratio")
    else:
        with st.spinner("Generating campaign..."):
            # Build brief
            brief = CampaignBrief(
                brief_id=f"ui-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                brand_id=brand_id,
                campaign_slogan=campaign_slogan,
                target_region="North America",
                target_audience="General",
                target_locales=locales,
                products=[Product(name=p, palette_words=["clean", "natural"]) for p in products],
                aspects=aspects,
                created_at=datetime.now(),
            )

            # Generate campaign
            orchestrator = build_orchestrator()
            result = orchestrator.generate_campaign(brief)

            # Display summary
            st.success("✅ Campaign generation complete!")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Assets", result["summary"]["total_assets"])
            with col2:
                st.metric("Validation Passed", result["summary"]["validation_passed"])
            with col3:
                st.metric("Validation Failed", result["summary"]["validation_failed"])
            with col4:
                st.metric("Products", len(products))

            st.markdown("---")

            # Group assets by product
            st.subheader("📦 Generated Assets")

            for product in products:
                with st.expander(f"**{product}**", expanded=True):
                    product_assets = [a for a in result["assets"] if a.product_name == product]

                    # Display assets in columns
                    cols = st.columns(min(len(product_assets), 3))
                    for idx, asset in enumerate(product_assets):
                        with cols[idx % len(cols)]:
                            st.markdown(f"**{asset.aspect_ratio}** / {asset.locale}")
                            st.info(f"💬 \"{asset.message}\"")
                            st.caption(f"Asset ID: `{asset.asset_id[:8]}...`")

            # Validation details
            st.markdown("---")
            st.subheader("✅ Validation Report")
            failed_validations = [v for v in result["validation_results"] if not v.is_valid]

            if failed_validations:
                st.warning(f"{len(failed_validations)} assets failed validation")
                for v in failed_validations:
                    st.error(f"Asset {v.asset_id}: {', '.join([i.message for i in v.issues])}")
            else:
                st.success("All assets passed validation checks")

else:
    # Welcome screen
    st.info("👈 Configure your campaign in the sidebar and click **Generate Campaign** to get started")

    st.subheader("🏛️ Architecture Overview")
    st.markdown("""
    This PoC demonstrates **Pragmatic Clean Architecture** with:

    - **Entities**: 6 domain models (BrandSummary, CampaignBrief, CreativeAsset, etc.)
    - **Use Cases**: Business logic (Generation, Validation)
    - **Orchestrator**: Workflow coordination
    - **Adapters**: Fake AI, Storage, Brand Repository (no API keys required!)
    - **Drivers**: CLI (Typer) + UI (Streamlit)

    **Testing**: 1 feature-level acceptance test validates complete workflow (<100ms execution)
    """)

    st.subheader("🎯 Quick Demo")
    st.markdown("""
    1. Keep default settings in sidebar
    2. Click **Generate Campaign**
    3. View 8 localized assets (2 products × 2 locales × 2 aspects)
    4. See Spanish localization: "Regalo Bienestar"
    """)

    st.markdown("---")
    st.caption("Built with Lean-Clean methodology | FDE Take-Home Exercise Task 2")
