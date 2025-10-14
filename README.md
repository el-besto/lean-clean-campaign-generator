# Campaign Generator PoC

**AI-driven creative automation for localized social ad campaigns**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Clean Architecture](https://img.shields.io/badge/architecture-clean-green.svg)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
[![Tests Passing](https://img.shields.io/badge/tests-passing-brightgreen.svg)](#testing)

> FDE Take-Home Exercise - Task 2: Proof-of-concept demonstrating Pragmatic Clean Architecture for multi-locale campaign generation.

---

## 🎯 Overview

This PoC generates **localized creative assets** for social ad campaigns across multiple products, locales, and aspect ratios. Built with **Pragmatic Clean Architecture**, it demonstrates:

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

---

## 📦 Quick Start

### Prerequisites

- Python 3.11 or higher
- `make` (optional, but recommended)

### Installation

```bash
# Clone repository
git clone <repository-url>
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
# Opens browser at http://localhost:8501
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

**Get help**:
```bash
python -m drivers.cli.commands generate --help
```

### Streamlit UI

```bash
make ui

## or
source .venv/bin/activate 
PYTHONPATH=. streamlit run drivers/ui/streamlit/app.py
```

Then:
1. Configure campaign in sidebar (products, locales, aspects)
2. Click **Generate Campaign**
3. View generated assets with localized messages
4. Check validation report

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
│  Layer 1: ADAPTERS & INFRASTRUCTURE  │  FakeAIAdapter, FakeStorageAdapter
│  External services, repositories     │  InMemoryBrandRepository
└──────────────────────────────────────┘
```

### Dependency Rule

**Dependencies flow INWARD** (outer layers depend on inner layers, never reverse):
- Use cases depend on **adapter interfaces** (protocols), not implementations
- Easy to swap fakes for real implementations (OpenAI, MinIO, Weaviate, etc.)
- Business logic (use cases) remains pure and testable

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
- **Uses ONLY fake adapters** (no external dependencies)
- **Fast execution** (<100ms)
- **Outside-In TDD**: Test written first, implementation driven by test

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
```

### Adding Real Adapters

To replace fakes with real implementations:

1. **Create adapter** implementing protocol:
   ```python
   # app/adapters/ai/openai.py
   class OpenAIAdapter:
       def generate_image(self, prompt: str, aspect_ratio: str) -> bytes:
           # Call OpenAI DALL-E 3 API
           ...
   ```

2. **Update dependency injection**:
   ```python
   # drivers/cli/commands.py
   ai_adapter = OpenAIAdapter()  # Instead of FakeAIAdapter()
   ```

3. **No use case changes required** (Dependency Inversion Principle)

---

## 🎓 Design Patterns Demonstrated

- **Dependency Inversion Principle**: Use cases depend on adapter protocols
- **Adapter Pattern**: Multiple adapter implementations (fake, real)
- **Orchestrator Pattern**: Coordinates multiple use cases
- **Presenter Pattern**: Formats results for different outputs
- **Repository Pattern**: Brand persistence abstraction
- **Protocol/Interface Segregation**: Python protocols define contracts

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

Built with:
- **Lean-Clean Methodology**: Pragmatic Clean Architecture principles
- **Python 3.11+**: Modern Python features (dataclasses, protocols)
- **Typer**: CLI framework
- **Streamlit**: Web UI framework
- **pytest**: Testing framework

---

**🤖 Generated with [Claude Code](https://claude.com/claude-code)**

**Co-Authored-By: Claude <noreply@anthropic.com>**
