# 🚀 CompliLedger Algorand SDK — 10‑Day Developer Plan

Goal: Ship a basic v1 (MVP) by Day 3 that delivers static analysis baseline + PCI‑DSS. Defer proof anchoring/hashing to later and deliver full v1 by Day 9. Day 10 is buffer/QA.

## 🎯 Objectives
- v1 (Basic, Day 3):
  - SDK Analyzer: PyTeal/TEAL static analysis engine.
  - Policies: Algorand baseline + PCI‑DSS (7 core checks).
  - CLI: `check`, `report`, `list-policies`, minimal interactive menu.
  - Docs: Quickstart, SECURITY_RULES overview, sample contracts & reports.
- v1 (Complete, Day 9):
  - Proof Anchoring: Event canonicalization + hashing + on‑chain note anchoring + verification.
  - CLI: `anchor`, `verify`, `watch`, polished interactive TUI.
  - Backend (minimal): nonce auth, prepare‑tx, submit‑tx, verify, history.
  - Frontend (minimal Vercel): connect wallet, new proof, verify, history.

## 🔗 Scope & Deliverables
- Static Analysis (PyTeal/TEAL): parser (AST for PyTeal), core rules (sender checks, amount validation, state mutation guards, rekey), PCI‑DSS basic.
- CLI: analysis commands (`check`, `report`, `list-policies`), minimal interactive TUI, HTML/JSON/MD reports.
- Policies: `algorand-baseline.json`, `pci-dss-algorand.json` with rule/control mappings.
- Phase 2 (Day 6+): Proof Anchoring Engine (Algorand) — event canonicalization, hashing, txn note format, explorer links, confirm/verify; backend & frontend minimal for anchoring flows.

## 📅 Day‑by‑Day Plan

### Day 1 — Scaffolding & Analyzer Bootstrap
- Code:
  - Create `compliledger_algorand/` structure: `analyzer/`, `cli/`, `policies/`, `core/`, `client/` (reserved for Day 6+ anchoring).
  - `pyproject.toml` (copy from comp‑leo, keep analysis deps; add `py-algorand-sdk` but unused until Day 6).
  - `analyzer/parser.py`: PyTeal parser via Python AST — capture functions, `Assert(...)`, `App.globalPut/localPut/box*`, `InnerTxnBuilder.Submit`, `Txn.*` usage.
  - `analyzer/checker.py`: port skeleton (scoring, models), wire to parser.
  - `policies/algorand-baseline.json`: initial 10 rules; `policies/pci-dss-algorand.json`: initial 7 rules.
  - `cli/main.py`: add `check`, `list-policies`; basic terminal output.
- Docs: Minimal README Quickstart for analysis.
- Tests: Parser nodes and smoke rule tests.
- DoD: `compliledger check examples/*.py` runs and prints baseline findings.

### Day 2 — Core Rules, Reporting, PCI Basics
- Code:
  - Implement core baseline rules:
    - Missing sender verification (critical) — require `Assert(Txn.sender() == Global.creator_address())` or allowlist.
    - Amount validation (high) — bounds on `Btoi(Txn.application_args[i])`.
    - State mutation guards (high) — guard `App.globalPut/localPut/box*` with asserts.
    - Rekey‑to protection (high) — Assert `Txn.rekey_to() == Global.zero_address()`.
    - Logging presence (medium) — require `Log(...)` around critical paths.
  - CLI: `report` command; HTML/Markdown formatters.
  - Policies: finalize `algorand-baseline` and `pci-dss-algorand` mappings.
- Tests: Golden HTML/MD report snapshots; PCI fixtures (PAN/CVV patterns) for exposure flags.
- DoD: Baseline + PCI produce scores, severities, and reports.

### Day 3 — Ship Basic v1 (Analysis Baseline + PCI‑DSS)
- Stabilize: severity weights, thresholds, clear remediation messages.
- CLI: minimal interactive menu; `list-policies` shows packs with counts.
- Docs: SECURITY_RULES (rule list, detection heuristics), Quickstart, examples.
- Release: Tag `v0.1.0a` (internal) or PyPI pre‑release.
- DoD: Analyzer v1 shipped — `check/report/list-policies` stable; baseline + PCI pass tests.

### Day 4 — TEAL Parser & Expanded Baseline
- Code:
  - `analyzer/teal_parser.py`: regex parser for `.teal` (assert, `app_global_put/local_put`, `box_*`, inner txns).
  - Expand rules: unchecked return heuristics; privacy exposure hints.
  - CLI polish: improved grouping, colors; JSON output option.
- Tests: TEAL fixtures; mixed PyTeal/TEAL projects.
- DoD: Mixed codebases analyzed with consistent results.

### Day 5 — Expanded Rules, Reports, Watch, PCI Policy
- Code:
  - Rules: asset transfer safety (InnerTxn AssetTransfer), box storage size (≤32KB) + MBR hints, refund mechanism presence, transaction limit assertions.
  - Reports: HTML/Markdown export (reuse comp‑leo formatters), `report` command.
  - Watch mode (watchdog) for auto re‑checks.
  - PCI: finalize 7 controls (3.2, 3.4, 6.5.1, 7.1, 10.2, 11.3.4, 12.10.6) with examples.
- Tests: Golden report snapshots; PCI fixtures; watch smoke test.
- DoD: Baseline + PCI policy packs usable end‑to‑end.

### Day 6 — Proof Anchoring (SDK + CLI)
- Code:
  - `client/events.py`: `ComplianceEvent` + canonical JSON + SHA‑256 hashing.
  - `client/algorand.py`: algod wrapper; PaymentTxn self‑send amt=0; note `CLG1|sha256:<hex>`; confirmation helper.
  - `CompliLedgerClient.mint_proof()` + `verify_proof()`; CLI `anchor`/`verify` (testnet).
- Docs: Anchoring Quickstart; fees; explorer links; privacy guidance.
- Tests: Anchor/verify integration on testnet with test mnemonic.
- DoD: End‑to‑end anchor/verify succeeds < 10s.

### Day 7 — Backend (FastAPI) Minimal
- Code:
  - Endpoints: `/auth/nonce`, `/auth/verify`; `/events` (create), `/events/{id}/prepare-tx`, `/events/{id}/submit-tx`, `/verify`, `/wallets/{addr}/proofs`.
  - In‑memory store or SQLite; simple rate limits; idempotency headers; optional service‑signed path.
- SDK Integration: optional `ConnectedClient` hitting backend instead of local algod.
- DoD: cURL flow works: create → prepare → sign → submit → confirm → verify.

### Day 8 — Frontend (Vercel) Minimal
- Code (Next.js):
  - Connect wallet (Pera Wallet Connect).
  - New Proof: form → canonical preview → call prepare‑tx → sign/submit → show txid.
  - Verify: txid + optional event JSON → valid/invalid + timestamp.
  - History: list proofs by wallet.
- DoD: Deployed preview on Vercel; testnet anchoring E2E.

### Day 9 — Full v1 Complete
- Hardening:
  - Analyzer: rule tuning, severity weights; policy docs; interactive menu polish.
  - Anchoring: confirm polling with backoff; structured logs; idempotency; quotas (basic).
  - Docs: full README, SECURITY_RULES, PCI guide, API reference, Quickstart.
- CI/CD: GitHub Action — `check` on PR; `anchor` on main (service‑signed) with API key.
- Release: Tag `v0.1.0`; optional PyPI stable.
- DoD: Analysis v1 + Anchoring v1 + minimal backend/frontend.

### Day 10 — Buffer / QA / Fixes
- Bug bash; perf pass; UX copy; edge case fixes; smoke across Mac/Linux; finalize roadmap for v0.2.0.

## ✅ Acceptance Criteria Summary
- Day 3: `check/report/list-policies` functional; Algorand baseline + PCI‑DSS rules produce expected results with docs and examples.
- Day 5: Expanded rules (asset, box, refund, limits) and reports/watch in place.
- Day 7: Backend minimal for anchoring APIs confirmed via cURL.
- Day 8: Vercel dApp connects wallet, anchors/verify, shows history.
- Day 9: Full docs, interactive CLI, backend endpoints stable, CI templates published.

## 🧩 Dependencies
- SDK: `py-algorand-sdk`, `click`, `rich`, `pydantic`, `watchdog`, `questionary`.
- Backend: `fastapi`, `uvicorn`, `python-jose` (or sign‑txn verification util), `redis` (optional), SQLite.
- Frontend: Next.js, Tailwind, shadcn/ui, `@perawallet/connect`.

## ⚠️ Risks & Mitigations
- Parser accuracy: start with common PyTeal idioms; grow coverage; provide suppression pragmas.
- Indexer latency: pending state UI + retries; allow algod fallback for recent txns.
- PCI false positives: configurable thresholds; policy toggles; rule rationale in reports.
- Wallet UX friction: support service‑signed for CI; batch actions later.

## 🧪 Testing Plan
- Unit: parser nodes, rule functions, canonicalization (from Day 6).
- Integration: `analyze → report` (Day 3+), `analyze → anchor → verify` (Day 6+).
- E2E: CLI interactive snapshots; frontend Cypress smoke.
- Golden: HTML/MD report snapshots (baseline + PCI).

## 📦 Artifacts per Milestone
- Day 3: Policy JSONs, CLI (`check/report/list-policies`), SECURITY_RULES.md, sample reports, example contracts.
- Day 5: Expanded policies, watch mode, polished HTML/MD reports.
- Day 7: Backend OpenAPI schema, cURL examples, Postman collection.
- Day 8: Live Vercel URL.
- Day 9: API docs, GH Action example, release notes.
