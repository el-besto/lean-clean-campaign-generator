# Demo Instructions

## Quick Demo (5 minutes)

### 1. CLI Demo (1 minute)

```bash
make demo
```

**What to show:**
- 8 assets generated (2 products × 2 locales × 2 aspects)
- Campaign summary with metrics
- Spanish localization working ("Regalo Bienestar")

### 2. Run Tests (30 seconds)

```bash
make test-features
```

**What to show:**
- Feature test passes in < 0.02s
- 12 assets validated
- No external dependencies (all fakes)

### 3. Streamlit UI (2 minutes)

```bash
make ui
```

**What to demonstrate:**
1. Sidebar configuration (products, locales, aspects)
2. Click "Generate Campaign"
3. View summary metrics
4. Expand product sections to see localized assets
5. Check validation report (all passed)

### 4. Architecture Overview (1-2 minutes)

**Key Points:**
- **Pragmatic Clean Architecture** (5 layers)
- **Dependency Inversion**: Use cases depend on protocols, not implementations
- **Fake adapters**: No API keys required, fast testing
- **Easy evolution**: Swap fakes for real adapters without changing business logic

**Show code structure:**
```bash
ls -la app/
ls -la drivers/
```

Point out:
- `app/entities/` - Domain models
- `app/use_cases/` - Business logic (framework-agnostic)
- `app/adapters/` - Fake implementations
- `drivers/` - CLI + UI (interchangeable)

---

## Recording Demo Video (5 minutes)

### Setup

1. Open terminal
2. Navigate to project: `cd lean-clean-campaign-generator`
3. Open browser (for Streamlit demo)
4. Start recording (QuickTime, OBS, etc.)

### Script

**[0:00-0:30] Introduction**
```
"Hi, I'm demonstrating the Campaign Generator PoC,
built with Pragmatic Clean Architecture.

This generates localized social ad campaigns
without requiring any API keys."
```

**[0:30-1:30] CLI Demo**
```bash
make demo
```
```
"Here's the CLI generating 8 assets for 2 products
across 2 locales and 2 aspect ratios.

Notice the Spanish localization: 'Regalo Bienestar'
translates 'Pure Wellness'."
```

**[1:30-2:00] Testing**
```bash
make test-features
```
```
"Our acceptance test validates the complete workflow
in under 20 milliseconds using fake adapters."
```

**[2:00-4:00] Streamlit UI**
```bash
make ui
```
```
"The Streamlit UI provides an interactive interface.

[Configure in sidebar]
Let me configure a campaign with:
- 2 products (Lavender Soap, Citrus Gel)
- 2 locales (English, Spanish)
- 2 aspect ratios (Square, Portrait)

[Click Generate]
Campaign generated successfully!

[Show results]
We got 8 assets with localized messages,
organized by product.

All validation checks passed."
```

**[4:00-5:00] Architecture**
```bash
ls -la app/
```
```
"The architecture follows Clean Architecture principles:

- Entities: Domain models
- Use Cases: Business logic
- Adapters: Fake implementations (no API keys!)
- Drivers: CLI and UI

Dependencies flow inward - use cases depend on
interfaces, not implementations.

This makes it easy to swap fakes for real AI services
without changing any business logic.

Thank you!"
```

---

## Next Steps for GitHub

1. **Create GitHub repository** (if not exists)
   ```bash
   # Create repo on GitHub, then:
   git remote add origin <repository-url>
   ```

2. **Push code**
   ```bash
   git push -u origin main
   ```

3. **Verify README displays** on GitHub

4. **Optional: Add badges**
   - Test status
   - Python version
   - License

5. **Optional: GitHub Actions**
   - Auto-run tests on push
   - Generate coverage report

---

## Presentation Slides (Optional)

**Slide 1: Title**
- Campaign Generator PoC
- Pragmatic Clean Architecture Demo

**Slide 2: Problem**
- Manual campaign creation is slow
- Localization is error-prone
- Hard to maintain consistency

**Slide 3: Solution**
- AI-driven automation
- Multi-locale support
- Brand guideline enforcement

**Slide 4: Architecture**
- [Architecture diagram from README]
- 5 layers, dependency inversion

**Slide 5: Demo**
- CLI + UI screenshots
- Test results

**Slide 6: Future Work (Task 3)**
- Model Context Protocol
- Real AI adapters
- Vector similarity search

---

## Troubleshooting

**Port already in use (Streamlit)**
```bash
# Find and kill process
lsof -ti:8501 | xargs kill -9
```

**Dependencies missing**
```bash
make install
```

**Tests failing**
```bash
make clean
make test
```
