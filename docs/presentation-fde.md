---
marp: true
theme: default
class: invert
paginate: true
header: 'FDE Interview: Creative Automation PoC'
footer: 'Angelo Cisneros | 2025-10-14'
size: 16:9
style: |
  section {
    font-family: 'Arial', sans-serif;
  }
  h1 {
    color: #4a90e2;
  }
  h2 {
    color: #5ba3f5;
    font-size: 1em;
  }
  code {
    background: #2d2d2d;
    font-size: 0.3em;
  }
  pre {
    font-size: 0.8em;
  }
  .columns {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
  }
  .small-code {
    font-size: 0.75em;
  }
  .compact-text {
    font-size: 0.85em;
  }
  .compact-text li {
    margin: 0.3rem 0;
  }
---

<!-- _class: lead -->

# Creative Automation PoC

## Outside-In Development for Enterprise AI

**Forward Deployed Engineer Interview**
Angelo Cisneros
2025-10-14

**The Challenge:** Build a PoC in days, not months
**The Approach:** Lean-Clean methodology + Pragmatic Clean Architecture

<!--

## SLIDE: Title (Creative Automation PoC)

**Opening (30s):**

- "Built a production-ready PoC, (est to complete in 5 days) not 6 weeks"

- "Key differentiator: Lean-Clean methodology—write executable tests WITH stakeholders BEFORE burning API budgets"

- "This isn't just a code exercise—it's how I approach FDE work: outside-in, stakeholder-first, pragmatic architecture"

**Hook:** Traditional enterprise PoCs take weeks and $5K+ in API costs because engineering builds first, discovers requirements were wrong. This approach inverts that.

-->

---

<!-- _header: 'Implementation Roadmap' -->

## Roadmap: 5-Day PoC → Production Evolution

<div class="columns">
<div>

**Phase 1: Foundation** (Day 1) ✅
- Core entities & domain model
- Campaign brief schema (YAML)
- Fake adapters for all external services
- Acceptance tests with fakes

**Phase 2: Orchestration** ✅
- Orchestrator workflow implementation
- CLI + Streamlit drivers
- Multi-stakeholder workshop validation
- Iterate on fakes with stakeholders

**Phase 3: Real Adapters** (Day 3-4) 🔄
- OpenAI image generation
- Claude Vision brand analysis
- Claude multilingual localization
- Integration tests (real APIs)

</div>
<div>

**Phase 4: Production Ready** (Day 5) 📅
- E2E smoke tests
- MinIO → S3 storage migration
- Monitoring & logging
- Stakeholder demo

**Phase 5: Adv. Features** (Week 2-3) 📅
- Weaviate vector search (asset reuse)
- Brand compliance validation
- Legal content filtering
- A/B test framework

**Phase 6: Agentic System** (Week 4) 📅
- Automated monitoring
- Alert generation with context
- Model Context Protocol
- Stakeholder communication automation

</div>
</div>

**Legend:** ✅ Complete | 🔄 In Progress | 📅 Planned

**Key Insight:** 5 days from workshop to production-ready PoC, then iterative enhancements based on usage.

<!--

## SLIDE: Roadmap (5-Day PoC → Production Evolution)

**Key Points (2 min):**

**Phase 1-2 (Day 1-2):** Fake adapters + multi-stakeholder workshop = $0 spent, all stakeholders aligned

  - "No OpenAI key needed yet—validate behavior with deterministic fakes"

  - "Creative Lead, Legal, Ad Ops, IT all see it working and sign off"

**Phase 3 (Day 3-4):** Real adapters implemented in PARALLEL after approval
  - "Because we have the contract (acceptance tests), engineers can parallelize"

  - "OpenAI adapter, Claude localization, image gen—independent teams, same interfaces"

**Phase 4-6 (Week 2-4):** Production hardening + advanced features
  - "Agentic system (Task 3) builds on this foundation—same architecture, adds monitoring/alerts"


**FDE Angle:** 

As FDE, you need to deliver fast demos that evolve to production. This roadmap shows progressive refinement, not throwaway spikes.

**Anticipate:** 

"Why fake adapters first?" → Because stakeholders reject 30% of PoCs after seeing them work. Validate behavior before expensive implementation.

-->

---

<!-- _header: 'Why Lean-Clean: Multi-Stakeholder Alignment' -->

## The Enterprise PoC Problem

**Traditional Approach:**
```text
Week 1-2:   Creative team writes requirements
Week 3-4:   Legal reviews, finds issues
Week 5-8:   Engineering builds, discovers Ad Ops needs weren't captured
Week 9-10:  IT flags integration problems
Week 11-12: Rework and compromises

Cost: $5,000+ in API bills | Time: 6-8 weeks | Result: Frustrated stakeholders
```

**Lean-Clean Approach:**
```text
Day 1: 90-min workshop → executable test captures ALL requirements
Day 2-3: Implement orchestrator with fakes → stakeholders see it working
Day 4-5: Implement real adapters in parallel → production-ready PoC

Cost: ~$200 in API testing | Time: 5-6 days | Result: Aligned stakeholders
```

**The Secret:** Write realistic, executable tests **with stakeholders present** before implementing expensive infrastructure.

<!--

## SLIDE: Enterprise PoC Problem (Traditional vs. Lean-Clean)

**Story Setup (2 min):**

- "Imagine global consumer goods company: Creative wants brand consistency, Legal needs compliance, Ad Ops wants A/B tests, IT needs cost control"

- "Traditional: sequential handoffs = 12 weeks of ping-pong, frustrated stakeholders"

- "Creative writes specs → Legal finds issues 3 weeks later → Engineering discovers Ad Ops requirements weren't captured → IT flags integration problems week 9"

**Key Contrast:**

- **Traditional:** $5K+ API bills discovering requirements were wrong

- **Lean-Clean:** $200 API testing AFTER stakeholder approval

**Lean-Clean Secret:** 
90-min workshop with ALL stakeholders present, writing executable tests as shared contract

**FDE Angle:** 

As FDE, you're the bridge. You can't afford to play telephone between stakeholders and engineering. Workshop format brings everyone to the table.

**Technical Credibility:** 

"This isn't just 'better communication'—it's a testing strategy. Acceptance tests with fakes are your stakeholder contract. Integration tests verify real APIs. E2E smoke tests prove it connects."

-->

---

<!-- _header: 'Why Lean-Clean: Outside-In Testing' -->

## Multi-Stakeholder Workshop → Executable Spec

**The 90-Minute Workshop:**

<div class="columns">
<div>

**Who's in the Room:**
- Creative Lead | Legal/Compliance
- Ad Operations
- IT/DevOps

**What They Define:**
- Success criteria (as assertions)
- Edge case priorities
- SLA requirements
- Integration points

</div>
<div>

**What You Deliver:**
- Acceptance test (with fakes)
- All stakeholders see it run
- Iterate in workshop
- Sign-off before spending

**Example Output:**
```python
async def test_campaign_generation():
    # Creative Lead requirement
    assert brand_compliant

    # Legal requirement
    assert content_filtered

    # Ad Ops requirement
    assert ab_test_assigned

    # IT requirement
    assert latency < 3.0
```

</div>
</div>

**Key Insight:** Fakes enable stakeholders to validate behavior **before** you burn API budgets or build infrastructure.

<!-- 

## SLIDE: Multi-Stakeholder Workshop → Executable Spec

**Workshop Structure (2 min):**

- **Who:** Creative Lead, Legal, Ad Ops, IT Architect
- **Duration:** 90 minutes
- **Output:** Executable acceptance test they all sign off on

**Demo Flow (walk through code example on slide):**

1. "Creative Lead defines brand compliance requirement → we write assertion with fake validator"

2. "Legal defines content filtering → we write assertion, configure fake to simulate failure"

3. "Ad Ops defines A/B test requirement → we write assertion, verify event tracking works"

4. "IT defines latency SLA → we write assertion, measure with fakes"

**Key Insight:** 

Stakeholders see it RUN in the workshop. Not a requirements doc. Not a mockup. Real code executing.

**FDE Skill Highlight:** 

"This is classic FDE work—translate business needs into executable specs, then show it working before you build the expensive parts"

**Anticipate:** 

"What if stakeholders don't understand code?" → Given/When/Then structure + plain English docstrings. They validate BEHAVIOR, not implementation.

-->

---

<!-- _header: 'Why Lean-Clean: Three-Layer Testing Strategy' -->

## The Testing Pyramid

```text
                    ▲
                   ╱ ╲
                  ╱ E2E ╲          3-5 tests
                 ╱ Smoke ╲         Run before deploy
                ╱─────────╲        Slow ($2-5), uses REAL services
               ╱           ╲
              ╱ Integration╲      10-20 tests per adapter
             ╱   Adapters   ╲     Run nightly
            ╱───────────────  ╲   Medium speed ($0.50-2)
           ╱                   ╲  Tests REAL OpenAI, DAM, etc.
          ╱    Acceptance       ╲   50-100+ tests
         ╱    (Stakeholder       ╲  Run on EVERY commit
        ╱      Contract)          ╲ Fast (<5s), FREE
       ╱─────────────────────────  ╲ Uses FAKES
      ╱          ALWAYS FAKES       ╲
     ╱─────────────────────────────  ╲
```

**Layer 1 (Acceptance):** ALWAYS uses fakes - this is your stakeholder contract
**Layer 2 (Integration):** Tests REAL adapters (OpenAI, DAM) in isolation
**Layer 3 (E2E):** Minimal smoke tests proving everything connects

**Why This Works:** You validate **business logic** cheaply (Layer 1), then verify **integrations** work correctly (Layer 2), then confirm **everything connects** (Layer 3).

<!-- 

## SLIDE: Three-Layer Testing Strategy (Pyramid)

**Visual Walkthrough (2 min):**

**Layer 1 (Bottom - Wide):** Acceptance Tests

- "Always fakes, always fast (<5s), always run on every commit"
- "This is the stakeholder contract—never changes to use real services"
- "50-100+ tests covering business logic, edge cases, workflows"

**Layer 2 (Middle):** Integration Tests

- "Real APIs in isolation—just the adapter, not full orchestration"
- "Run nightly or on-demand, costs ~$0.50-2 per run"
- "10-20 tests per adapter verifying contract matches reality"

**Layer 3 (Top - Narrow):** E2E Smoke Tests

- "Full system with all real services—run before deploy only"
- "3-5 critical path tests, costs ~$2-5 per run"
- "Proves everything connects, not comprehensive coverage"

**Why This Works (key insight):**

- "Validate business logic cheaply (Layer 1)"
- "Verify integrations work correctly (Layer 2)"
- "Confirm everything connects (Layer 3)"

**FDE Angle:** 

"As FDE, you need fast feedback loops with customers. Layer 1 lets you iterate in front of stakeholders without API costs. Layers 2-3 give you production confidence."

**Anticipate:** 

"Don't you need to test the REAL API?" → Yes! That's Layer 2. But AFTER stakeholders approve the behavior in Layer 1.

-->

---

<!-- _header: 'Architecture: Clean Architecture Layers' -->

## System Architecture: Pragmatic Clean Architecture

```text
┌───────────────────────────────────────────────────────────┐
│   Drivers Layer (ALWAYS PRESENT from Day 1)               │
│   ─────────────────────────────────────────────           │
│   CLI (Typer):          Streamlit UI:                     │
│   - Automation          - Creative Lead: Visual review    │
│   - CI/CD integration   - Legal: Approve/reject           │
│   - Batch processing    - Ad Ops: Performance metrics     │
│                         - IT: System monitoring           │
│                                                           │
│   FastAPI (When Needed):                                  │
│   - Enterprise integrations                               │
│   - External webhooks                                     │
└────────────┬──────────────────────────────────────────────┘
             │ Calls orchestrators
┌────────────▼──────────────────────────────────────────────┐
│   Orchestrator Layer                                      │
│   - Campaign workflow coordination                        │
│   - Multi-market batch processing                         │
│   - Event emission (campaign_generated, ab_test_assigned) │
└────────────┬──────────────────────────────────────────────┘
             │
┌────────────▼──────────────────────────────────────────────┐
│   Use Case Layer (Business Logic)                         │
│   - Brand validation rules                                │
│   - Content filtering (Legal)                             │
│   - Cultural adaptation                                   │
│   - Regulatory compliance per market                      │
└────────────┬──────────────────────────────────────────────┘
             │
      ┌──────┴───────┐
      │              │
┌─────▼───────┐  ┌───▼───────────────┐
│ Adapters    │  │ Infrastructure    │
│ (External)  │  │ (Persistence)     │
│             │  │                   │
│ - OpenAI    │  │ - Campaign repo   │
│ - Claude    │  │   (Postgres)      │
│ - DAM       │  │ - Creative repo   │
│ - Analytics │  │   (MongoDB)       │
└─────────────┘  └───────────────────┘
```

<!-- 

## SLIDE: System Architecture (Clean Architecture Layers)

**Architecture Walkthrough (2 min):**

**Why Drivers Layer from Day 1:**

- "CLI for automation/CI/CD (engineers)"
- "Streamlit for visual feedback (Creative Lead needs to SEE images, not read logs)"
- "FastAPI when needed (enterprise integrations)"

**Key Point:** 

"Enterprise PoCs need multiple entry points. Creative Lead won't approve a campaign by reading terminal output."

**Orchestrator Layer (emphasize this):**

- "Coordinates multiple use cases—generate + validate + emit events"
- "This is where multi-stakeholder requirements converge"
- "Chose 'Orchestrator' over 'Controller' because stakeholders understand orchestration"

**Use Case Layer:**

- "Pure business logic—brand validation, content filtering, cultural adaptation"
- "Framework-agnostic, easy to test with fakes"

**Adapters + Infrastructure:**

- "External services (OpenAI, Claude) vs. persistence (Postgres, MongoDB)"
- "Fake implementations live here—not in test utilities"

**Dependency Flow (critical):**

- "All dependencies point INWARD"
- "Use cases depend on adapter INTERFACES, not implementations"
- "Swap fakes for real OpenAI without changing use case code"

**FDE Angle:** 

"As FDE, you need architecture that evolves. Today's PoC becomes tomorrow's production system. Dependency inversion means you can swap implementations without rewriting business logic."

-->

---

<!-- _header: 'Architecture: Dependency Flow' -->

<style scoped>
pre {
  font-size: 0.4em;
}
</style>

## Dependency Inversion + Adapter Pattern

<div class="columns">
<div>

**The Dependency Rule:**
```text
User Request (CLI/UI)
    ↓
Drivers
    ↓
Orchestrators
    ↓
Use Cases
    ↓
Entities ←─────────┐
    ↑              │
    │              │
    │ Uses via     │ Implements
    │ Interface    │ Interface
    │              │
Protocols  →  Concrete Adapters
```

**Dependencies point INWARD**
- Use Cases depend on interfaces
- Adapters implement interfaces
- Swap implementations without changing Use Cases

</div>
<div>

**Adapter Substitution:**
```python
# Use Case depends on interface
class GenerateCampaign:
    def __init__(
        self,
        ai_adapter: IAIAdapter  # Interface!
    ):
        self.ai = ai_adapter

# Fake for workshop
class FakeAIAdapter(IAIAdapter):
    def generate_image(self, prompt):
        return placeholder_image()

# Real for production
class OpenAIAdapter(IAIAdapter):
    def generate_image(self, prompt):
        return openai.images.generate(...)

# Claude alternative
class ClaudeAdapter(IAIAdapter):
    def generate_image(self, prompt):
        return anthropic.messages.create(...)
```

**Swap at runtime via config**

</div>
</div>

<!-- 

## SLIDE: Dependency Inversion + Adapter Pattern

**Code Walkthrough (2 min):**

**Left Side (Dependency Rule):**

- "Use cases depend on interfaces (protocols)"
- "Adapters implement interfaces"
- "Orchestrators coordinate use cases"

**Right Side (Adapter Substitution):**

- Walk through code example:
  - `IAIAdapter` protocol
  - `FakeAIAdapter` for workshop
  - `OpenAIAdapter` for production
  - `ClaudeAdapter` as alternative

**Key Demo:** "Same interface, three implementations. Swap at runtime via config."

**FDE Value:**

- "Customer wants to switch from OpenAI to Claude? One config change."
- "Customer's compliance team blocks OpenAI API access? Fall back to fakes, demo still works."
- "This is FDE flexibility—you're not locked into vendor decisions at architecture level"

**Technical Depth:** 

"Using Python protocols (structural typing), not inheritance. More flexible than abstract base classes."

-->

---

<!-- _header: 'Architecture: Two Types of Fakes' -->

<style scoped>
pre {
  font-size: 0.4em;
}
</style>

## Fakes: The Key to Velocity

<div class="columns">
<div>

**Type 1: Fake Adapters**
*(External Services)*

```python
# Business stakeholders see these
class FakeImageGenAdapter:
    """Demo without API keys"""
    def generate_image(self, prompt):
        return self._placeholder_image()

class FakeDAMIntegration:
    """Simulate DAM upload"""
    def upload(self, asset):
        self.uploaded_assets.append(asset)
        return fake_dam_id()

class FakeEventTracker:
    """Capture events for assertions"""
    def track(self, event):
        self.events.append(event)
```

**Use in:** Acceptance tests
**Purpose:** Fast feedback, no API costs

</div>
<div>

**Type 2: In-Memory Repositories**
*(Persistence)*

```python
# DevOps/IT stakeholders see these
class InMemoryCampaignRepo:
    """No database needed"""
    def __init__(self):
        self.campaigns = {}

    def save(self, campaign):
        self.campaigns[campaign.id] = campaign

    def get(self, campaign_id):
        return self.campaigns.get(campaign_id)

class PostgresCampaignRepo:
    """Production persistence"""
    def save(self, campaign):
        self.db.execute(
            "INSERT INTO campaigns..."
        )
```

**Use in:** Integration tests
**Purpose:** Isolate persistence logic

</div>
</div>

**Critical Insight:** Fakes live in production code (not test utils) so stakeholders can run them in workshops.

<!-- 

## SLIDE: Two Types of Fakes

**Critical Distinction (2 min):**

**Type 1: Fake Adapters (External Services)**

- Location: `app/adapters/` (production code!)
- Audience: Business stakeholders
- Examples: `FakeImageGenAdapter`, `FakeDAMIntegration`, `FakeEventTracker`
- "Creative Lead sees these in workshop—placeholder images, simulated DAM upload"

**Type 2: In-Memory Repositories (Persistence)**

- Location: `app/infrastructure/repositories/` (production code!)
- Audience: IT/DevOps stakeholders
- Examples: `InMemoryCampaignRepo`
- "IT sees this in workshop—no database needed, data stored in dict"

**Why Fakes in Production Code:**

- "Used in workshops, local dev, CI/CD, stakeholder demos"
- "Deterministic (tests don't flake), realistic (simulate latency, costs)"
- "NOT mocks—no magic, no mocking frameworks"

**FDE Angle:** 

"In customer workshops, you boot up the system with fakes. No VPN, no API keys, no database. Just show them it works. THEN get approvals for real infrastructure."

**Anticipate:** 

"Don't fakes diverge from reality?" → Layer 2 integration tests catch that. Keep fakes simple—match interface, not complex API behavior.

-->

---

<!-- _header: 'Task 3: Agentic System Design' -->

## AI-Driven Monitoring & Alerts

<div class="columns">
<div>

**Agent Responsibilities:**
1. **Monitor** incoming campaign briefs
2. **Trigger** automated generation tasks
3. **Track** creative variant count/diversity
4. **Flag** missing/insufficient assets
5. **Alert** stakeholders with contextual info

**Alert Types:**
- ⚠️ Missing assets (< 3 variants)
- ⚠️ Generation failures (API errors)
- ⚠️ Validation failures (legal/compliance)
- ⚠️ Approval timeouts (HITL bottlenecks)

</div>
<div>

**Model Context Protocol:**
```python
context = {
    "brief_id": "holiday-2025-01",
    "issue": "insufficient_variants",
    "expected": 12,
    "actual": 8,
    "missing": ["lavender-soap/es-US/9x16"],
    "reason": "OpenAI API rate limit"
}

# LLM generates stakeholder message:
"Holiday Gift campaign delayed.
Generated 8 of 12 assets. Missing
4 Spanish story-format images due
to API rate limits. Resolution: 2hrs.
Recommend: Approve English assets
now, Spanish separately."
```

**Outcome:** Structured data → LLM → Human-readable stakeholder communication

</div>
</div>

<!-- 

## SLIDE: Agentic System Design (Task 3)

**Quick Overview (1 min - optional depending on time):**

**Agent Responsibilities:**

- Monitor campaign briefs → trigger generation → track variants → flag issues → alert stakeholders

**Model Context Protocol Example:**

- "Structured data (missing assets, API error) → LLM generates human-readable message → stakeholders get context, not raw errors"

**Example:** 

"Holiday campaign delayed. Generated 8 of 12 assets. Missing 4 Spanish story-format images due to API rate limits. Resolution: 2hrs. Recommend: Approve English assets now, Spanish separately."

**FDE Value:** 

"This is where AI meets enterprise operations. You're not just building creative automation—you're building the monitoring layer that keeps it running. Agentic system translates system state into stakeholder communication."

**Connection to PoC:** 

"Same architecture—orchestrators coordinate, use cases implement logic, adapters call LLMs. Just adding a monitoring layer on top."

-->

---

<!-- _class: compact-text -->
<!-- _header: 'Core Decisions: Architecture & Testing' -->

## Key Design Decisions

**Decision 1: Pragmatic Clean Architecture (not just scripts)**
- ✅ **Pro:** Testable, maintainable, production evolution path
- ❌ **Con:** More upfront structure than quick script
- **Why:** Interview context + real-world PoCs need to scale

**Decision 2: Dual AI Implementation (Fake + Real from Day 1)**
- ✅ **Pro:** Demo without API keys, workshop velocity
- ❌ **Con:** More code to maintain (2x adapters)
- **Why:** Stakeholder alignment before spending

**Decision 3: CLI + UI Drivers from Day 1 (not just CLI)**
- ✅ **Pro:** Creative Lead needs visual feedback, not logs
- ❌ **Con:** More complex than CLI-only PoC
- **Why:** Enterprise PoCs have non-technical stakeholders

<!-- 

## SLIDE: Core Decisions (Architecture & Testing)

**Quick Hits (1 min):**

**Decision 1: Pragmatic Clean Architecture**

- Pro: Testable, evolvable, production path
- Con: More upfront structure than quick script
- Why: Interview context (show architectural thinking) + PoCs that scale

**Decision 2: Dual AI Implementation (Fake + Real)**

- Pro: Demo without API keys, workshop velocity
- Con: 2x adapters to maintain
- Why: Stakeholder alignment BEFORE spending

**Decision 3: CLI + UI Drivers from Day 1**

- Pro: Creative Lead needs visual feedback
- Con: More complex than CLI-only
- Why: Enterprise PoCs have non-technical stakeholders

**Meta-Point:** 

"These are FDE trade-offs. You're balancing technical excellence with customer delivery speed. Pragmatic CA is the sweet spot."

-->

---

<!-- _class: compact-text -->
<!-- _header: 'Core Decisions: Trade-offs & Constraints' -->

## Trade-offs & Constraints

**Decision 4: YAML for Campaign Briefs (not JSON or API)**
- ✅ **Pro:** Human-readable, comment-friendly, version control
- ✅ **Pro:** Stakeholders can hand-craft without tooling
- ❌ **Con:** Requires parser, not as ubiquitous as JSON
- **Why:** Lean-Clean principle - optimize for human readability

**Decision 5: Campaign-Level Localization**
- ✅ **Pro:** "One campaign, many locales" natural model
- ✅ **Pro:** Simpler implementation for 6-8 hour timebox
- ❌ **Con:** Product names not localized (assumes English)

**Key Meta-Decision:** Optimize for **interview context** (demonstrate skill + thinking) while maintaining **production viability** (not throwaway code).

<!-- 

## SLIDE: Trade-offs & Constraints

**Quick Hits (1 min):**

**Decision 4: YAML for Campaign Briefs**

- Pro: Human-readable, comment-friendly, version control
- Con: Requires parser
- Why: Stakeholders can hand-edit without tooling

**Decision 5: Campaign-Level Localization**

- Pro: "One campaign, many locales" natural model
- Con: Product names not localized (assumes English)
- Why: Simpler for 6-8 hour timebox

**Meta-Decision (emphasize this):** 

"Optimize for interview context (demonstrate skill + thinking) while maintaining production viability (not throwaway code)"

**FDE Angle:** 

"This is FDE thinking—what can I cut to deliver fast while keeping quality high? What's the MVP that still impresses stakeholders?"

-->

---

<!-- _class: lead -->

## Questions for Discussion

**Architecture:**
- Thoughts on Pragmatic CA vs. simpler patterns for PoCs?
- Experience with adapter pattern for AI service substitution?

**Stakeholder Alignment:**
- Experience with multi-stakeholder workshops?
- How would you handle conflicting requirements?

**Forward Deployment:**
- What challenges do you see in deploying this to customers?
- How would you adapt this for different customer contexts?

<!-- 

## SLIDE: Questions for Discussion

**Transition (30s):**

- "I've shown you the what and how. Let's discuss the why and what-if."

**Your Prepared Talking Points:**

**Architecture:**

- "Pragmatic CA vs. simpler patterns: I chose this because PoCs often become production. Simpler patterns (single file, no DI) don't evolve well. But happy to discuss trade-offs."

- "Adapter pattern for AI: Swapping providers is real need in enterprises. OpenAI → Claude, on-prem models, vendor lock-in avoidance."

**Stakeholder Alignment:**

- "Multi-stakeholder workshops: 

    - I've simulated this here, but in real FDE work, this is THE critical skill. Getting Legal, Creative, IT in one room with executable tests prevents months of rework."

- "Conflicting requirements:

  - Workshop format forces real-time negotiation. 

    - Example: Legal wants zero risk (fail on content filter outage) vs. Ad Ops wants partial success (launch some markets). You negotiate, document decision in test."

**Forward Deployment Considerations:**

- "Challenges deploying to customers: 
    - API access/compliance (hence fake adapters for demos), 
    - data residency (Europe won't use US OpenAI), 
    - cost controls (customer won't approve $5K API testing)."

- "Adapting for different contexts: 
  - Financial services needs Legal-first PoC. 
  - Startup needs speed-first. 
  - FDE adjusts workshop priorities, same methodology."

**Engage Them:**

- "What patterns do you see in successful FDE projects at the company?"

- "How do you typically handle stakeholder alignment in PoCs?"

-->

---

<!-- _class: lead -->

# Thank You

<div class="columns">
<div>

**Repository:** [GitHub link](https://github.com/el-besto/lean-clean-campaign-generator)

**Let's discuss:**
- Deep dive on any architectural decisions
- Testing strategy refinements
- Real-world deployment considerations
- Forward deployment scenarios

</div>

<div>

```
    __                           ________
   / /   ___  ____ _____        / ____/ /__  ____ _____
  / /   / _ \/ __ `/ __ \______/ /   / / _ \/ __ `/ __ \
 / /___/  __/ /_/ / / / /_____/ /___/ /  __/ /_/ / / / /
/_____/\___/\__,_/_/ /_/      \____/_/\___/\__,_/_/ /_/


```

<div style="text-align: center; margin-top: 2rem; margin-left:4rem">
  <img src="https://github.com/el-besto.png" alt="GitHub Avatar" style="width: 150px; border-radius: 50%;">
</div>

**Lean-Clean Methodology:** <br>[The Secret Sauce: Outside-In with All Stakeholders](https://github.com/el-besto/lean-clean-methodology/blob/main/blog/lean-clean-the-secret-sauce.md)

</div>
</div>

<!-- 

## CLOSING THOUGHTS (if time permits)

**Summary (30s):**

- "I built this to show FDE thinking: 

    - stakeholder collaboration, 
    - pragmatic architecture, 
    - rapid delivery"

- "Lean-Clean methodology is my approach to bridging business and engineering"

- "This PoC is production-ready, but more importantly, it's EVOLVABLE"

**Why I Want This Role:**

- "FDE is where AI technology adoption meets real-world constraints"

- "I love the challenge of making cutting-edge tech work in messy enterprise contexts"

- "This PoC shows I can deliver fast, collaborate with stakeholders, and build systems that scale"

-->

<!-- End of Presentation -->
