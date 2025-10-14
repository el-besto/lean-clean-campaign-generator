"""
Page 0: Upload Seeds

Upload brand asset images (seed images) to MinIO and index in Weaviate.
These seeds are used for vector similarity search during campaign generation.
"""
import streamlit as st
from PIL import Image
from io import BytesIO

from drivers.ui.streamlit.shared import upload_seed_assets

st.set_page_config(page_title="Upload Seeds", page_icon="📤", layout="wide")

st.header("📤 Upload Seed Assets")

st.markdown("""
Upload brand asset images (product photos, lifestyle shots, etc.) to build your asset library.

**How it works:**
1. Upload images for a specific product
2. Images are stored in MinIO and indexed in Weaviate
3. During campaign generation, similar existing assets are reused when possible
4. Color palettes are automatically extracted for brand consistency

**Requirements:** Real adapters must be enabled (Docker services + Weaviate + MinIO)
""")

# Sidebar: Configuration
st.sidebar.header("Upload Configuration")

use_real = st.sidebar.checkbox(
    "Enable real adapters",
    value=True,
    help="Required for uploading. Ensure Docker services are running.",
)

if not use_real:
    st.warning("⚠️ Real adapters must be enabled to upload seed assets. Check the box in the sidebar.")
    st.stop()

brand_id = st.sidebar.selectbox("Brand", ["natural-suds-co"])
product_name = st.sidebar.text_input(
    "Product Name",
    value="Lavender Soap",
    help="Product these seed images belong to"
)

# Main: File Upload
st.subheader("Select Images")

uploaded_files = st.file_uploader(
    "Upload seed images (PNG, JPG, WebP)",
    type=["png", "jpg", "jpeg", "webp"],
    accept_multiple_files=True,
    help="Select one or more brand asset images to upload",
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

# Upload button
if st.button("Upload Seeds", type="primary", disabled=not uploaded_files):
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
                    with st.expander("Upload Details", expanded=True):
                        for item in result["seeded"]:
                            st.markdown(f"""
**{item['filename']}**
- Asset ID: `{item['asset_id']}`
- URL: `{item['url']}`
- Palette: {', '.join(item['palette'][:3])}
""")

            except Exception as e:
                st.error(f"Upload failed: {e}")
                st.exception(e)

# Help section
with st.expander("ℹ️ How to use", expanded=False):
    st.markdown("""
    ### Step-by-step guide:

    1. **Start services**: `make up` (starts Weaviate + MinIO)
    2. **Enable real adapters** in sidebar
    3. **Select brand and product** name
    4. **Upload images** (one or more)
    5. **Click Upload Seeds**

    ### What happens:
    - Images are stored in MinIO (S3-compatible storage)
    - Image vectors are created using multi2vec-clip
    - Color palettes are extracted automatically
    - Assets are tagged as "seed" for easy filtering

    ### Next steps:
    Go to **Generate Campaign** page to create new assets. The system will search
    for similar existing seeds before generating new images.
    """)
