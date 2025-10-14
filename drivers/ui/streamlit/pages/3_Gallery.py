"""
Page 2: Asset Gallery

View all generated assets across campaigns.
"""
import streamlit as st
from PIL import Image
from io import BytesIO

from app.infrastructure.factories import create_storage_adapter

st.set_page_config(page_title="Asset Gallery", page_icon="🖼️", layout="wide")

st.header("🖼️ Asset Gallery")

use_real = st.checkbox("Use real storage (MinIO)", value=False)

if use_real:
    storage = create_storage_adapter(use_real=True)

    # List all assets
    all_assets = storage.list("")

    if not all_assets:
        st.info("No assets found. Generate a campaign first!")
    else:
        st.write(f"Found {len(all_assets)} assets")

        # Filter options
        st.subheader("Filters")
        filter_text = st.text_input("Filter by path (e.g., 'lavender' or 'en-US')", "")

        if filter_text:
            filtered_assets = [a for a in all_assets if filter_text.lower() in a.lower()]
        else:
            filtered_assets = all_assets

        st.write(f"Showing {len(filtered_assets)} assets")

        # Display in grid
        cols = st.columns(3)
        for idx, asset_path in enumerate(filtered_assets):
            with cols[idx % 3]:
                try:
                    image_bytes = storage.load(asset_path)
                    image = Image.open(BytesIO(image_bytes))
                    st.image(image, caption=asset_path, use_container_width=True)

                    # Add download button
                    st.download_button(
                        label="Download",
                        data=image_bytes,
                        file_name=asset_path.split("/")[-1],
                        mime="image/png",
                        key=f"download_{idx}",
                    )
                except Exception as e:
                    st.error(f"Failed to load {asset_path}: {e}")
else:
    st.info("Enable real storage to view MinIO assets")

    st.markdown("""
    ### How to use:

    1. Start services: `make up`
    2. Generate campaign with real adapters (Page: Generate Campaign)
    3. Enable "Use real storage" checkbox above
    4. Browse and download generated assets
    """)
