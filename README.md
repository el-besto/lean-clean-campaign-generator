# Campaign Generator PoC

**AI-driven creative automation for localized social ad campaigns**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Clean Architecture](https://img.shields.io/badge/architecture-clean-green.svg)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

> FDE Take-Home Exercise - Task 2: Proof-of-concept demonstrating Pragmatic Clean Architecture for multi-locale campaign generation.

---

## 🎯 Overview

This PoC generates **localized creative assets** for social ad campaigns across multiple products, locales, and aspect ratios. Built with [**Pragmatic Lean-Clean Architecture**][lean-clean-pca], it demonstrates:

- ✅ **Clean separation of concerns** (5 architectural layers)
- ✅ **Dependency Inversion Principle** (use cases depend on interfaces, not implementations)
- ✅ **Testability** (fake adapters enable fast testing without external dependencies)
- ✅ **Extensibility** (easy to swap fake adapters for real AI/storage services)

### Key Features

- **Localized campaigns**: Generate assets for multiple locales (English, Spanish, etc.)
- **Multiple formats**: Support for various aspect ratios (1:1, 9:16, 16:9)
- **Validation**: Built-in legal compliance checks (prohibited words)
- **Two interfaces**: CLI (Typer) + Web UI (Streamlit)
- **Fast testing**: Uses fake adapters (no API keys required, <100ms execution)

[lean-clean-pca]: https://github.com/el-besto/lean-clean-methodology/blob/main/docs/framework-folder-structures.md#1-pragmatic-ca-the-sweet-spot

---

## 📊 Presentation

**[View the 30-minute FDE interview presentation →](presentation/presentation-fde.md)**

This presentation covers:

- **Lean-Clean Methodology**: Why Outside-In development with stakeholders ([read more](https://github.com/el-besto/lean-clean-methodology))
- **Architecture Deep-Dive**: Pragmatic Clean Architecture decisions
- **Testing Strategy**: Three-layer testing pyramid (Acceptance → Integration → E2E)
- **Design Trade-offs**: Key decisions with pros/cons
- **Agentic System Design**: AI-driven monitoring and alerts (Task 3)

📄 [PDF version](presentation/presentation-fde.pdf)

---

## 📦 Quick Start

### Prerequisites

- Python 3.11 or higher
- `make` (optional, but recommended)

### Installation

```bash
# Clone repository
git clone https://github.com/el-besto/lean-clean-campaign-generator
cd lean-clean-campaign-generator

# Install dependencies
make install

# Or manually:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run Demo

**Option 1: CLI Demo**
```bash
make demo
```

**Option 2: Streamlit UI**
```bash
make ui
# Opens browser at http://localhost:8501 (default Streamlit port)
```

---

## 🐳 Infrastructure Setup (Real Adapters)

**Optional**: Use real adapters for production-quality output (OpenAI + MinIO + Weaviate).

### Prerequisites

- Docker + Docker Compose (or Podman)
- OpenAI API key

### Start Services

```bash
# Start Weaviate + MinIO services
make up

# Check Weaviate readiness
make readiness

# Set API key
export OPENAI_API_KEY="sk-..."
```

### Service URLs

- **Weaviate API**: http://localhost:8080
- **MinIO Console**: http://localhost:9001 (login: minio / minio123)

### Seed Brand Data

```bash
# Populate Weaviate with example brand
make seed

# or
.venv/bin/python tools/seed_brand.py
```

### Run with Real Adapters

```bash
# CLI with real adapters
python -m drivers.cli.commands generate --real

# Streamlit UI (toggle real adapters in sidebar)
make ui
```

### Stop Services

```bash
# Stop services
make down

# Stop and remove volumes (fresh start)
make clean-infra
```

---

## 🚀 Usage

### CLI Interface

**Quick demo** (2 products × 2 locales × 2 aspects = 8 assets):
```bash
python -m drivers.cli.commands demo
```

**Custom campaign**:
```bash
python -m drivers.cli.commands generate \
  --brand natural-suds-co \
  --slogan "Pure Wellness" \
  --product "Lavender Soap" \
  --product "Citrus Gel" \
  --locale en-US \
  --locale es-US \
  --aspect 1:1 \
  --aspect 9:16 \
  --aspect 16:9 \
  --verbose
```

**With real adapters** (requires `make up` and `OPENAI_API_KEY`):
```bash
python -m drivers.cli.commands generate --real
```

**Get help**:
```bash
python -m drivers.cli.commands generate --help
```

### Streamlit UI

```bash
make ui
# Opens browser at http://localhost:8501
```

**Multi-page app**:
1. **Home**: Architecture overview and navigation
2. **Generate Campaign**: Interactive form with fake/real adapter toggle
3. **Gallery**: Browse and download assets from MinIO

**To use real adapters in UI**:
1. Start services: `make up`
2. Set API key: `export OPENAI_API_KEY="sk-..."`
3. Navigate to "Generate Campaign"
4. Check "Use real adapters" in sidebar
5. Generate and view images inline!

---

## 🏛️ Architecture

### Pragmatic Clean Architecture (5 Layers)

```
┌──────────────────────────────────────┐
│  Layer 5: DRIVERS                    │  CLI (Typer), UI (Streamlit)
│  Entry points for user interaction   │
└────────────────┬─────────────────────┘
                 ↓
┌──────────────────────────────────────┐
│  Layer 4: INTERFACE ADAPTERS         │  Orchestrators, Presenters
│  Workflow coordination & formatting  │
└────────────────┬─────────────────────┘
                 ↓
┌──────────────────────────────────────┐
│  Layer 3: USE CASES                  │  GenerateCampaignUC, ValidateCampaignUC
│  Business logic (framework-agnostic) │
└────────────────┬─────────────────────┘
                 ↓
┌──────────────────────────────────────┐
│  Layer 2: ENTITIES                   │  BrandSummary, CampaignBrief, CreativeAsset
│  Domain models (pure Python)         │
└────────────────┬─────────────────────┘
                 ↑
┌──────────────────────────────────────┐
│  Layer 1: ADAPTERS & INFRASTRUCTURE  │  Fake: FakeAIAdapter, FakeStorageAdapter
│  External services, repositories     │  Real: OpenAIImageAdapter, MinIOStorageAdapter
│                                      │        WeaviateBrandRepository
└──────────────────────────────────────┘
```

### Dependency Rule

**Dependencies flow INWARD** (outer layers depend on inner layers, never reverse):
- Use cases depend on **adapter interfaces** (protocols), not implementations
- Easy to swap fakes for real implementations (OpenAI, MinIO, Weaviate, etc.)
- Business logic (use cases) remains pure and testable

> **Learn more:** [Pragmatic Clean Architecture patterns →](https://github.com/el-besto/lean-clean-methodology/blob/main/docs/framework-folder-structures.md)

### Project Structure

```
campaign-generator/
├── app/
│   ├── entities/            # Domain models (BrandSummary, CampaignBrief, etc.)
│   ├── use_cases/           # Business logic (Generate, Validate)
│   ├── interface_adapters/  # Orchestrators, Presenters
│   ├── adapters/            # AI, Storage adapters (fake + protocols)
│   └── infrastructure/      # Brand repository
├── drivers/
│   ├── cli/                 # Typer CLI
│   └── ui/streamlit/        # Streamlit dashboard
├── tests/
│   └── features/            # Acceptance tests
├── Makefile                 # Development commands
├── requirements.txt         # Dependencies
├── pytest.ini               # Test configuration
└── README.md               # This file
```

---

## 🧪 Testing

### Run All Tests

```bash
make test
```

### Run Feature Tests Only

```bash
make test-features
```

### Test Output

```
✓ 12 assets generated (2 products × 3 aspects × 2 locales)
✓ Localization working (es-US: "Regalo Bienestar")
✓ All validation passing
✓ Test execution: 0.02s
```

### Testing Strategy

- **One feature-level acceptance test** validates complete workflow
- **One use-case test** for demonstration
- **Uses ONLY fake adapters** (no external dependencies)
- **Fast execution** (<100ms)
- **Outside-In TDD**: Test written first, implementation driven by test

> **Learn more:** [Outside-In testing with stakeholders →](https://github.com/el-besto/lean-clean-methodology/blob/main/docs/lean-clean-axioms.md#axiom-7-fakes-in-production-code)

---

## 📋 Requirements Met

### PDF Requirements

- ✅ **Minimum 2 products**: Lavender Soap, Citrus Shower Gel
- ✅ **Minimum 3 aspect ratios**: 1:1, 9:16, 16:9
- ✅ **English + Spanish locales**: en-US, es-US
- ✅ **Organized folder structure**: `out/assets/{product}/{locale}/{aspect}/`
- ✅ **Brand guidelines**: Loaded from YAML/in-memory repository
- ✅ **Validation**: Legal checks (prohibited words)

### Architectural Decisions

- ✅ **Pragmatic Clean Architecture**: 5 layers, dependency inversion
- ✅ **Fake adapters**: Demo without API keys
- ✅ **YAML config**: Human-readable brand/brief configuration
- ✅ **Protocol-based ports**: Easy adapter substitution
- ✅ **Dual interfaces**: CLI + UI for different stakeholders

---

## 🛠️ Development

### Available Commands

```bash
make help           # Show all available commands
make install        # Install dependencies
make test           # Run all tests
make test-features  # Run feature tests only
make demo           # Run CLI demo
make cli            # Run CLI (use: make cli ARGS="generate --help")
make ui             # Run Streamlit UI
make clean          # Clean generated files
make seed           # Generate the first brand

# Infrastructure (real adapters)
make up             # Start Weaviate + MinIO services
make down           # Stop services
make clean-infra    # Stop services and remove volumes
make readiness      # Check Weaviate health
make open           # Open service UIs in browser
```

### Adapter Modes

**Fake Adapters** (default):
- Fast testing mode (<100ms execution)
- No external dependencies
- Deterministic output
- Use for: Tests, demos without API keys

**Real Adapters** (production):
- OpenAI gpt-image-1 for image generation
- MinIO for S3-compatible blob storage
- Weaviate for vector-based brand search
- Use for: Production-quality output

**Toggle via**:
- CLI: `--real` flag
- UI: Checkbox in sidebar
- Code: `create_ai_adapter(use_real=True)`

---

## 🎓 Design Patterns Demonstrated

- **Dependency Inversion Principle**: Use cases depend on adapter protocols
- **Adapter Pattern**: Multiple adapter implementations (fake, real)
- **Orchestrator Pattern**: Coordinates multiple use cases
- **Presenter Pattern**: Formats results for different outputs
- **Repository Pattern**: Brand persistence abstraction
- **Protocol/Interface Segregation**: Python protocols define contracts

> **Learn more:** [Lean-Clean architectural principles →](https://github.com/el-besto/lean-clean-methodology/blob/main/docs/lean-clean-axioms.md)

---

## 🔮 Future Enhancements (Task 3)

**Agentic System Extensions**:
- Model Context Protocol integration for stakeholder communication
- Automated alerts for validation failures
- Asset reuse via vector similarity search (Weaviate)
- HITL approval workflows
- Performance monitoring and optimization

**Production Evolution**:
- Real AI adapters (OpenAI DALL-E 3, Claude Vision/Multilingual)
- Cloud storage (MinIO/S3)
- Vector database (Weaviate)
- Async task queue (Celery)
- API server (FastAPI)

---

## 📝 License

This is a proof-of-concept for educational purposes (FDE Take-Home Exercise).

---

## 🙏 Acknowledgments

<div style="text-align: center;">
<pre>
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  LEAN-CLEAN METHODOLOGY                ┃
┃  ────────────────────────              ┃
┃  Write Tests WITH Stakeholders         ┃
┃  Validate BEFORE Building              ┃
┃  Evolve WITHOUT Rewrites               ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
</pre>
</div>

Built with:
- **Lean-Clean Methodology**: Pragmatic Clean Architecture principles, [read more](https://github.com/el-besto/lean-clean-methodology)
- **Python 3.11+**: Modern Python features (dataclasses, protocols)
- **Typer**: CLI framework
- **Streamlit**: Web UI framework
- **pytest**: Testing framework

---

**🤖 Generated with [Claude Code](https://claude.com/claude-code)**

**Co-Authored-By: Claude <noreply@anthropic.com>**
