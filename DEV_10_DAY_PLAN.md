# 🚀 CompliLedger Algorand SDK — 10‑Day Developer Plan

Goal: Ship a basic v1 (MVP) by Day 3 that delivers: Scan → Detect → Compliance Verdict → Anchor on Algorand → Return TXID/Explorer/Outcome/Rule matches. Full v1 by Day 9. Day 10 is buffer/QA.

## 🎯 Objectives
- v1 (Basic, Day 3):
  - SDK Analyzer: PyTeal/TEAL scanning with a narrow, rule-based engine.
  - Compliance Verdict Object: generated from scan results (severity, rules matched, control mapping, timestamp).
  - Anchoring: Hash the verdict, write to Algorand (txn note), verify via Indexer.
  - CLI: `check`, `report`, `list-policies`, `anchor`, `verify`; minimal interactive menu.
  - Outputs: TXID, Explorer URL, scan outcome, rule matches.
  - PyPI pre-release.
- v1 (Complete, Day 9):
  - Expanded rules & policies (Algorand baseline + PCI‑DSS finalized), reports, watch, polished interactive TUI.
  - Backend (minimal): nonce auth, prepare‑tx, submit‑tx, verify, history.
  - Frontend (minimal Vercel): connect wallet, new proof (verdict), verify, history.

## 🔗 Scope & Deliverables
- Static Analysis (PyTeal/TEAL): parser (AST for PyTeal) + TEAL regex, small but real rule engine.
- Compliance Verdict Object: deterministic JSON of outcome (framework/control/status/rules/severity/timestamp/contract).
- Anchoring: verdict → SHA‑256 → Algorand txn note; TXID + explorer URL; verification via Indexer.
- CLI: `check`, `report`, `list-policies`, `anchor`, `verify`, minimal interactive TUI; HTML/JSON/MD reports.
- Policies: `algorand-baseline.json`, `pci-dss-algorand.json` with control mappings.

## ⚠️ P0 Core Rule Categories (Small but Real)

- **🛑 Application Control**
  - Detect DeleteApplication
  - Detect UpdateApplication
  - Verify admin check enforcement
- **🔑 Account Control**
  - Flag `RekeyTo != ZeroAddress`
  - Flag `CloseRemainderTo != ZeroAddress`
- **💰 Fee Abuse Patterns**
  - Excessive fee assignment (inner txn)
  - Fee pooling without bounds
- **🪙 Asset Safety**
  - Clawback abuse
  - Freeze authority missing
  - Unsafe opt-ins
- **🧠 Logic Patterns**
  - No sender checks
  - No argument validation

Each rule emits: Severity, control mapping (SOC 2 / PCI / FedRAMP), human‑readable description, and participates in the Compliance Verdict Object.

## 📅 Day‑by‑Day Plan

### Day 1 — Scaffolding, Parser, Verdict Schema
- Code:
  - Create `compliledger_algorand/` structure: `analyzer/`, `cli/`, `policies/`, `core/`, `client/`.
  - `pyproject.toml` (copy from comp‑leo); include `py-algorand-sdk`.
  - `analyzer/parser.py`: PyTeal AST; detect: `Assert(...)`, `App.globalPut/localPut/box*`, `InnerTxnBuilder.*`, `Txn.*` (RekeyTo/CloseRemainderTo/Fee), `Txn.on_completion()`.
  - `analyzer/teal_parser.py`: regex for `.teal` (assert/app_global_put/app_local_put/box_*/inner txns).
  - `analyzer/checker.py`: skeleton + scoring + rule plumbing.
  - `core/verdict.py`: Compliance Verdict Object schema + canonicalization (sorted keys) + SHA‑256 helper.
  - `cli/main.py`: `check`, `list-policies`, `report` basics.
- Docs: Quickstart for analysis + verdict format.
- Tests: Parser node extraction; verdict canonicalization determinism.
- DoD: `compliledger check examples/*.py` prints findings; verdict JSON generated locally.

### Day 2 — Implement P0 Rules + Anchoring Path
- Code:
  - Implement P0 rule categories (Application/Account/Fee/Asset/Logic) with minimal, explainable heuristics.
  - `policies/algorand-baseline.json` + `pci-dss-algorand.json`: initial control mappings.
  - CLI: `report` (HTML/MD/JSON) with rule matches and severity.
  - `client/algorand.py`: algod wrapper; PaymentTxn self‑send amt=0; note `CLG1|sha256:<hex>`; wait/confirm.
  - `cli`: add `anchor` (anchors verdict) and `verify` (recompute verdict hash vs chain note).
- Tests: Golden report snapshots; verdict → hash test vectors; anchor/verify against testnet using a sandbox mnemonic.
- DoD: Scan → Verdict → Anchor on testnet → Verify, end‑to‑end working via CLI.

### Day 3 — Ship P0 (Scan → Verdict → Anchor)
- Stabilize: rule messages, control mappings, thresholds, failure codes.
- CLI: minimal interactive menu (Quick Check → Anchor if pass/waived).
- Docs: SECURITY_RULES (rule list + heuristics), Verdict schema, Anchoring Quickstart.
- Release: PyPI pre‑release (`v0.1.0a`).
- DoD: Live demo: run `check` → show verdict → `anchor` → show TXID + Explorer URL → `verify` returns valid + rule matches.

### Day 4 — TEAL Parser & Expanded Baseline
- Code:
  - `analyzer/teal_parser.py`: regex parser for `.teal` (assert, `app_global_put/local_put`, `box_*`, inner txns).
  - Expand rules: unchecked return heuristics; privacy exposure hints.
  - CLI polish: improved grouping, colors; JSON output option.
- Tests: TEAL fixtures; mixed PyTeal/TEAL projects.
- DoD: Mixed codebases analyzed with consistent results.

### Day 5 — Expanded Rules, Reports, Watch, PCI Policy
- Code:
  - Rules: asset transfer safety (InnerTxn AssetTransfer), box storage size (≤32KB) + MBR hints, refund mechanism presence, transaction limit assertions; fee upper bounds per policy.
  - Reports: HTML/Markdown export (reuse comp‑leo formatters), `report` command.
  - Watch mode (watchdog) for auto re‑checks.
  - PCI: finalize 7 controls (3.2, 3.4, 6.5.1, 7.1, 10.2, 11.3.4, 12.10.6) with examples.
- Tests: Golden report snapshots; PCI fixtures; watch smoke test.
- DoD: Baseline + PCI policy packs usable end‑to‑end.

### Day 6 — Backend (FastAPI) Minimal
- Code:
  - Endpoints: `/auth/nonce`, `/auth/verify`; `/events` (create verdict), `/events/{id}/prepare-tx`, `/events/{id}/submit-tx`, `/verify`, `/wallets/{addr}/proofs`.
  - In‑memory store or SQLite; simple rate limits; idempotency headers; optional service‑signed path.
- SDK Integration: optional `ConnectedClient` using backend instead of local algod.
- DoD: cURL flow: create verdict → prepare → sign → submit → confirm → verify.

### Day 7 — Frontend (Vercel) Minimal
- Code (Next.js):
  - Connect wallet (Pera Wallet Connect).
  - New Proof: show verdict preview → call prepare‑tx → sign/submit → show TXID.
  - Verify: txid + optional verdict JSON → valid/invalid + timestamp.
  - History: list proofs by wallet.
- DoD: Deployed preview on Vercel; testnet anchoring E2E.

### Day 8 — CI/CD, Examples, Polish
- Code:
  - GitHub Action template: `check` on PR; `anchor` on main (service‑signed) with API key.
  - Pre‑commit hook; packaging; error messaging polish; progress/spinners.
  - Example contracts: vulnerable vs compliant PyTeal; demo script.
- Tests: Integration suite `analyze → anchor → verify` passing.
- DoD: CI template ready; examples included; docs updated.

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
- Day 3: End‑to‑end P0: `check` → Compliance Verdict generated → `anchor` verdict → TXID + Explorer URL returned → `verify` validates hash vs note; reports produced.
- Day 5: Expanded rules (asset, box, refund, limits), polished reports, watch mode.
- Day 7: Frontend minimal connects wallet, shows verdict preview, anchors/verify.
- Day 8: CI template runs `check` on PR and anchors on main (service‑signed).
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
- Unit: parser nodes, rule functions, verdict canonicalization.
- Integration: `analyze → anchor → verify` (CLI and SDK).
- E2E: CLI interactive snapshots; frontend Cypress smoke.
- Golden: HTML/MD report snapshots (baseline + PCI); verdict → hash test vectors.

## 📦 Artifacts per Milestone
- Day 3: Policy JSONs, CLI (`check/report/list-policies/anchor/verify`), SECURITY_RULES.md, sample reports, example contracts, Compliance Verdict Object examples, anchored proof (TXID + explorer URL).
- Day 5: Expanded policies, watch mode, polished HTML/MD reports.
- Day 7: Live Vercel URL (frontend preview).
- Day 8: Backend OpenAPI schema, cURL examples, Postman collection, CI templates.
- Day 9: API docs, GH Action example, release notes.
