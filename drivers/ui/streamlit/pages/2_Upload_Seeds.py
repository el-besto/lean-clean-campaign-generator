"""
Page 2: Upload Seeds (Optional)

Separate page for bulk seed asset uploads.
Users can also upload seeds inline on the Generate Campaign page.
"""
import streamlit as st
from PIL import Image
from io import BytesIO

from drivers.ui.streamlit.shared import upload_seed_assets

st.set_page_config(page_title="Upload Seeds", page_icon="📤", layout="wide")

st.header("📤 Upload Seed Assets")

st.markdown("""
Upload brand asset images (product photos, lifestyle shots) to build your asset library.

**Note:** You can also upload seeds inline on the **Generate Campaign** page. This page is for bulk uploads.
""")

# Configuration
st.subheader("Configuration")

col1, col2 = st.columns(2)

with col1:
    use_real = st.checkbox(
        "Enable real adapters",
        value=True,
        help="Required for uploading. Ensure Docker services are running.",
    )

with col2:
    brand_id = st.selectbox("Brand", ["natural-suds-co"])

if not use_real:
    st.warning("⚠️ Real adapters must be enabled to upload seed assets.")
    st.stop()

st.markdown("---")

# Seed upload
st.subheader("Upload Seeds")

col1, col2 = st.columns([2, 1])

with col1:
    uploaded_files = st.file_uploader(
        "Select seed images (PNG, JPG, WebP)",
        type=["png", "jpg", "jpeg", "webp"],
        accept_multiple_files=True,
        help="Upload multiple brand asset images",
    )

with col2:
    product_name = st.text_input(
        "Product Name",
        value="Lavender Soap",
        help="Which product are these seed images for?",
    )

# Preview uploaded images
if uploaded_files:
    st.write(f"**{len(uploaded_files)} image(s) selected**")

    # Show previews in grid
    cols = st.columns(min(4, len(uploaded_files)))
    for idx, upload in enumerate(uploaded_files):
        with cols[idx % 4]:
            image = Image.open(BytesIO(upload.getvalue()))
            st.image(image, caption=upload.name, use_container_width=True)

st.markdown("---")

# Upload button
if st.button("🚀 Upload Seeds", type="primary", disabled=not uploaded_files, use_container_width=True):
    if not product_name:
        st.error("Please enter a product name")
    else:
        with st.spinner(f"Uploading {len(uploaded_files)} image(s)..."):
            try:
                result = upload_seed_assets(
                    brand_id=brand_id,
                    product_name=product_name,
                    uploaded_files=uploaded_files,
                    use_real=use_real,
                )

                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success(f"✅ Uploaded {result['seed_count']} seed asset(s)")

                    # Show details
                    st.subheader("Upload Details")
                    for item in result["seeded"]:
                        with st.expander(f"📷 {item['filename']}", expanded=False):
                            st.markdown(f"""
- **Asset ID**: `{item['asset_id']}`
- **URL**: `{item['url']}`
- **Color Palette**: {', '.join(item['palette'][:5])}
""")

                    st.info("💡 **Tip:** Go to Generate Campaign page to use these seeds in your campaign!")

            except Exception as e:
                st.error(f"Upload failed: {e}")
                st.exception(e)

st.markdown("---")

# Help section
with st.expander("ℹ️ How it works", expanded=False):
    st.markdown("""
    ### Seed Upload Workflow:

    1. **Upload images** → Stored in MinIO (S3-compatible storage)
    2. **Extract palettes** → Automatic color extraction with ColorThief
    3. **Vectorize** → Images indexed in Weaviate with multi2vec-clip
    4. **Tag** → Assets tagged as "seed" for filtering

    ### During Campaign Generation:

    - System searches Weaviate for similar existing seeds
    - If found: Reuses seed (no OpenAI call needed)
    - If not found: Generates new image via OpenAI
    - New images are auto-indexed for future reuse

    ### Benefits:

    - **Cost savings**: Reuse existing assets instead of generating
    - **Brand consistency**: Search finds visually similar assets
    - **Speed**: Skip generation when good assets exist
    """)
