# FDE Interview Presentation Notes
**Audience:** AI Core Team Dev + Existing FDE
**Duration:** 30 minutes
**Goal:** Show FDE skills = engineering + systems design + stakeholder collaboration

---

## SLIDE: Title (Creative Automation PoC)

**Opening (30s):**
- "Built a production-ready PoC in 5 days, not 6 weeks"
- "Key differentiator: Lean-Clean methodology—write executable tests WITH stakeholders BEFORE burning API budgets"
- "This isn't just a code exercise—it's how I approach FDE work: outside-in, stakeholder-first, pragmatic architecture"

**Hook:** Traditional enterprise PoCs take weeks and $5K+ in API costs because engineering builds first, discovers requirements were wrong. This approach inverts that.

---

## SLIDE: Roadmap (5-Day PoC → Production Evolution)

**Key Points (2 min):**
- **Phase 1-2 (Day 1-2):** Fake adapters + multi-stakeholder workshop = $0 spent, all stakeholders aligned
  - "No OpenAI key needed yet—validate behavior with deterministic fakes"
  - "Creative Lead, Legal, Ad Ops, IT all see it working and sign off"

- **Phase 3 (Day 3-4):** Real adapters implemented in PARALLEL after approval
  - "Because we have the contract (acceptance tests), engineers can parallelize"
  - "OpenAI adapter, Claude localization, image gen—independent teams, same interfaces"

- **Phase 4-6 (Week 2-4):** Production hardening + advanced features
  - "Agentic system (Task 3) builds on this foundation—same architecture, adds monitoring/alerts"

**FDE Angle:** As FDE, you need to deliver fast demos that evolve to production. This roadmap shows progressive refinement, not throwaway spikes.

**Anticipate:** "Why fake adapters first?" → Because stakeholders reject 30% of PoCs after seeing them work. Validate behavior before expensive implementation.

---

## SLIDE: Enterprise PoC Problem (Traditional vs. Lean-Clean)

**Story Setup (2 min):**
- "Imagine global consumer goods company: Creative wants brand consistency, Legal needs compliance, Ad Ops wants A/B tests, IT needs cost control"
- "Traditional: sequential handoffs = 12 weeks of ping-pong, frustrated stakeholders"
- "Creative writes specs → Legal finds issues 3 weeks later → Engineering discovers Ad Ops requirements weren't captured → IT flags integration problems week 9"

**Key Contrast:**
- **Traditional:** $5K+ API bills discovering requirements were wrong
- **Lean-Clean:** $200 API testing AFTER stakeholder approval

**Lean-Clean Secret:** 90-min workshop with ALL stakeholders present, writing executable tests as shared contract

**FDE Angle:** As FDE, you're the bridge. You can't afford to play telephone between stakeholders and engineering. Workshop format brings everyone to the table.

**Technical Credibility:** "This isn't just 'better communication'—it's a testing strategy. Acceptance tests with fakes are your stakeholder contract. Integration tests verify real APIs. E2E smoke tests prove it connects."

---

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

**Key Insight:** Stakeholders see it RUN in the workshop. Not a requirements doc. Not a mockup. Real code executing.

**FDE Skill Highlight:** "This is classic FDE work—translate business needs into executable specs, then show it working before you build the expensive parts"

**Anticipate:** "What if stakeholders don't understand code?" → Given/When/Then structure + plain English docstrings. They validate BEHAVIOR, not implementation.

---

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

**FDE Angle:** "As FDE, you need fast feedback loops with customers. Layer 1 lets you iterate in front of stakeholders without API costs. Layers 2-3 give you production confidence."

**Anticipate:** "Don't you need to test the REAL API?" → Yes! That's Layer 2. But AFTER stakeholders approve the behavior in Layer 1.

---

## SLIDE: System Architecture (Clean Architecture Layers)

**Architecture Walkthrough (2 min):**

**Why Drivers Layer from Day 1:**
- "CLI for automation/CI/CD (engineers)"
- "Streamlit for visual feedback (Creative Lead needs to SEE images, not read logs)"
- "FastAPI when needed (enterprise integrations)"

**Key Point:** "Enterprise PoCs need multiple entry points. Creative Lead won't approve a campaign by reading terminal output."

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

**FDE Angle:** "As FDE, you need architecture that evolves. Today's PoC becomes tomorrow's production system. Dependency inversion means you can swap implementations without rewriting business logic."

---

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

**Technical Depth:** "Using Python protocols (structural typing), not inheritance. More flexible than abstract base classes."

---

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

**FDE Angle:** "In customer workshops, you boot up the system with fakes. No VPN, no API keys, no database. Just show them it works. THEN get approvals for real infrastructure."

**Anticipate:** "Don't fakes diverge from reality?" → Layer 2 integration tests catch that. Keep fakes simple—match interface, not complex API behavior.

---

## SLIDE: Agentic System Design (Task 3)

**Quick Overview (1 min - optional depending on time):**

**Agent Responsibilities:**
- Monitor campaign briefs → trigger generation → track variants → flag issues → alert stakeholders

**Model Context Protocol Example:**
- "Structured data (missing assets, API error) → LLM generates human-readable message → stakeholders get context, not raw errors"

**Example:** "Holiday campaign delayed. Generated 8 of 12 assets. Missing 4 Spanish story-format images due to API rate limits. Resolution: 2hrs. Recommend: Approve English assets now, Spanish separately."

**FDE Value:** "This is where AI meets enterprise operations. You're not just building creative automation—you're building the monitoring layer that keeps it running. Agentic system translates system state into stakeholder communication."

**Connection to PoC:** "Same architecture—orchestrators coordinate, use cases implement logic, adapters call LLMs. Just adding a monitoring layer on top."

---

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

**Meta-Point:** "These are FDE trade-offs. You're balancing technical excellence with customer delivery speed. Pragmatic CA is the sweet spot."

---

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

**Meta-Decision (emphasize this):** "Optimize for interview context (demonstrate skill + thinking) while maintaining production viability (not throwaway code)"

**FDE Angle:** "This is FDE thinking—what can I cut to deliver fast while keeping quality high? What's the MVP that still impresses stakeholders?"

---

## SLIDE: Questions for Discussion

**Transition (30s):**
- "I've shown you the what and how. Let's discuss the why and what-if."

**Your Prepared Talking Points:**

**Architecture:**
- "Pragmatic CA vs. simpler patterns: I chose this because PoCs often become production. Simpler patterns (single file, no DI) don't evolve well. But happy to discuss trade-offs."
- "Adapter pattern for AI: Swapping providers is real need in enterprises. OpenAI → Claude, on-prem models, vendor lock-in avoidance."

**Stakeholder Alignment:**
- "Multi-stakeholder workshops: I've simulated this here, but in real FDE work, this is THE critical skill. Getting Legal, Creative, IT in one room with executable tests prevents months of rework."
- "Conflicting requirements: Workshop format forces real-time negotiation. Example: Legal wants zero risk (fail on content filter outage) vs. Ad Ops wants partial success (launch some markets). You negotiate, document decision in test."

**Forward Deployment:**
- "Challenges deploying to customers: API access/compliance (hence fake adapters for demos), data residency (Europe won't use US OpenAI), cost controls (customer won't approve $5K API testing)."
- "Adapting for different contexts: Financial services needs Legal-first PoC. Startup needs speed-first. FDE adjusts workshop priorities, same methodology."

**Engage Them:**
- "What patterns do you see in successful FDE projects at [company]?"
- "How do you typically handle stakeholder alignment in PoCs?"

---

## CLOSING THOUGHTS (if time permits)

**Summary (30s):**
- "I built this to show FDE thinking: stakeholder collaboration, pragmatic architecture, rapid delivery"
- "Lean-Clean methodology is my approach to bridging business and engineering"
- "This PoC is production-ready, but more importantly, it's EVOLVABLE"

**Why I Want This Role:**
- "FDE is where AI research meets real-world constraints"
- "I love the challenge of making cutting-edge tech work in messy enterprise contexts"
- "This PoC shows I can deliver fast, collaborate with stakeholders, and build systems that scale"

---

## ANTICIPATED QUESTIONS & RESPONSES

**"Why not just use [simpler approach]?"**
→ "Great question. For a pure spike, yes—simpler works. But enterprise PoCs have two requirements: (1) fast stakeholder validation, (2) potential production path. Simpler approaches force rewrites. This evolves."

**"Isn't Lean-Clean just Clean Architecture?"**
→ "No—it's a synthesis. I took CA's dependency inversion, Hexagonal's ports/adapters, BDD's stakeholder tests, Lean's customer focus. The innovation is making them work together for AI PoCs specifically."

**"How do you know fakes match reality?"**
→ "Layer 2 integration tests. I run those nightly against real APIs. If OpenAI changes response format, integration test fails, I update fake. Acceptance tests catch regressions."

**"What if stakeholders can't code?"**
→ "They don't need to. Given/When/Then docstrings in plain English. They validate BEHAVIOR by watching tests run. Example: 'When I generate a campaign, then all assets are brand compliant' → they see it execute, green checkmark."

**"How does this scale to production?"**
→ "Progressive refinement. Today's Pragmatic CA evolves to Full CA by adding: separate entities from ORM, event sourcing, CQRS, async task queue. But stakeholder contract (acceptance tests) stays stable."

**"What about real-time collaboration in workshops?"**
→ "I write code live. Stakeholder says 'What if all markets fail?' → I write test in 2 minutes, run it, show them the error message. They say 'Add the support email to that error' → I add assertion, re-run. Instant feedback."

**"How do you handle skeptical stakeholders?"**
→ "Show, don't tell. Boot up Streamlit UI with fakes, generate campaign in front of them. They see images, localized text, brand compliance scores. THEN explain architecture. Seeing is believing."

**"What's your biggest lesson from this PoC?"**
→ "Terminology matters. I originally used 'Controller'—realized stakeholders were confused with MVC web controllers. Switched to 'Orchestrator'—clicked immediately. Small change, huge impact on workshop effectiveness."

---

## TIME ALLOCATION (30 min total)

- Title + Roadmap: 3 min
- Problem + Workshop: 5 min
- Testing Strategy + Architecture: 6 min
- Dependency Inversion + Fakes: 4 min
- Agentic + Decisions: 3 min
- Questions/Discussion: 9 min

**Flexibility:** If they're engaged, go deeper on architecture. If they're curious about stakeholders, go deeper on workshop mechanics. Read the room.

---

## BODY LANGUAGE & DELIVERY TIPS

**Energy:** Enthusiastic but not overselling. You're excited about FDE work, not desperate.

**Technical Depth:** Adjust based on who's asking. AI core team dev wants protocol details. FDE wants stakeholder stories.

**Confidence Calibration:** "I'm confident this approach works for AI PoCs, but I'm here to learn your context. How do you handle this at [company]?"

**Whiteboard Moment:** If they have a whiteboard, offer to draw the three-layer testing pyramid or dependency flow. Kinesthetic engagement.

---

## WHAT MAKES THIS FDE-RELEVANT

**Core FDE Skills Demonstrated:**

1. **Stakeholder Collaboration:** Multi-stakeholder workshop pattern
2. **Rapid Delivery:** 5 days to production-ready PoC
3. **Technical Depth:** Clean Architecture, DI, testing strategy
4. **Systems Thinking:** Three-layer testing, progressive refinement
5. **Pragmatism:** Trade-offs documented, not dogmatic purity
6. **Communication:** Presentation itself shows teaching/explaining ability
7. **Business Acumen:** Cost control ($200 vs. $5K), ROI focus
8. **Adaptability:** Fake adapters enable offline demos, customer constraints

**The Meta-Message:** "I don't just write code—I bridge engineering and business. That's FDE."
