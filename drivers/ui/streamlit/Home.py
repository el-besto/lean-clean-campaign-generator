"""
Streamlit UI for Campaign Generator - Home Page

Multi-page app structure:
- Home: Welcome and navigation
- Generate Campaign: Interactive campaign generation
- Gallery: View generated assets
"""
import streamlit as st

# Page config
st.set_page_config(
    page_title="Campaign Generator",
    page_icon="🎨",
    layout="wide",
)

st.title("🎨 Creative Campaign Generator")
st.markdown("AI-driven automation for social ad campaigns")

st.markdown("""
### Navigation

Use the sidebar to navigate between pages:

1. **🎨 Generate Campaign** - Complete workflow (upload brief, upload seeds, configure, generate)
2. **📤 Upload Seeds** - Bulk upload seed images (optional - can also upload inline on Generate page)
3. **🖼️ Gallery** - View all generated assets (MinIO storage)

### Adapter Modes

- **Fake Adapters** (default): Fast testing mode, no external dependencies
- **Real Adapters**: OpenAI image generation, MinIO storage, Weaviate search
  - Requires: Docker services running + `OPENAI_API_KEY` set

### Quick Start (Fake Mode)

1. Navigate to "Generate Campaign"
2. Click "Generate Campaign" (uses defaults)
3. View 8 localized assets instantly

### Quick Start (Real Mode)

1. Start services: `make up`
2. Set API key: `export OPENAI_API_KEY="sk-..."`
3. Navigate to "Generate Campaign", enable "Use real adapters"
4. Optionally upload seeds first (or use Upload Seeds page)
5. Generate!

---

## Architecture Overview

This PoC demonstrates **Pragmatic Clean Architecture** with:

- **Entities**: 6 domain models (BrandSummary, CampaignBrief, CreativeAsset, etc.)
- **Use Cases**: Business logic (Generation, Validation)
- **Orchestrator**: Workflow coordination
- **Adapters**: Fake + Real implementations (OpenAI, MinIO, Weaviate)
- **Drivers**: CLI (Typer) + UI (Streamlit)

**Testing**: 1 feature-level acceptance test validates complete workflow (<100ms execution)

---

**Tip:** Use fake adapters for testing, real adapters for production-quality output.
""")

st.caption("Built with Lean-Clean methodology | FDE Take-Home Exercise")
