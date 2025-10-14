# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI-driven creative automation for generating localized social ad campaigns. Built with **Pragmatic Clean Architecture** following the Lean-Clean methodology.

**FDE Take-Home Exercise - Task 2:** Working PoC demonstrating multi-locale campaign generation with fake adapters (no API keys required).

## Development Commands

```bash
# Install dependencies
make install

# Run tests
make test
make test-features  # Feature tests only

# Clean generated files
make clean
```

## Architecture

### Pragmatic Clean Architecture (5 Layers)

```
drivers/ (CLI, UI)
    ↓
interface_adapters/ (orchestrators, presenters)
    ↓
use_cases/ (business logic)
    ↓
entities/ (domain models)
    ↑
adapters/ + infrastructure/ (external services, repositories)
```

### Key Components

**Entities** (`app/entities/`)
- `BrandSummary`: Brand identity and guidelines
- `CampaignBrief`: Input contract (products, locales, aspects)
- `CreativeAsset`: Generated output (image + localized message)
- `ValidationResult`, `Approval`, `Alert`: Supporting entities

**Use Cases** (`app/use_cases/`)
- `GenerateCampaignUC`: Generate assets (product × aspect × locale)
- `ValidateCampaignUC`: Legal and brand compliance checks

**Orchestrator** (`app/interface_adapters/orchestrators/`)
- `CampaignOrchestrator`: Coordinates complete workflow

**Adapters** (`app/adapters/`, `app/infrastructure/`)
- `FakeAIAdapter`: Deterministic testing without API keys
- `FakeStorageAdapter`: In-memory storage
- `InMemoryBrandRepository`: Seeded brand data

### Testing Strategy

One feature-level acceptance test validates complete workflow:
- 12 assets (2 products × 3 aspects × 2 locales)
- Uses ONLY fakes (no external dependencies)
- Fast execution (<100ms)

**Run:** `make test-features`

## Implementation Notes

- All dependencies flow inward (Dependency Inversion Principle)
- Use cases depend on adapter protocols, not implementations
- Easy to swap fakes for real AI/storage adapters
- Python 3.11+, dataclasses for entities
- pytest for testing
