# CompliLedger Algorand SDK — Flow Tables (v1 and v2)

This document captures end-to-end flows across the User UI, SDK, CLI, Backend, and Algorand on-chain.

---

## v1 (Day 1–3): P0 — Scan → Verdict → Anchor

| Step | User action | SDK (local) | CLI | Backend API | On-chain | Output / UX |
|---|---|---|---|---|---|---|
| 1 | Choose policy pack(s) | `ComplianceChecker(policy_pack="algorand-baseline" or "pci-dss-algorand")` | `compliledger list-policies` | — | — | Shows available packs + rule counts |
| 2 | Run analysis on file/dir | `checker.check_file(...)` or `check_directory(...)` | `compliledger check contracts/ --policy algorand-baseline,pci-dss-algorand --threshold 80` | — | — | Starts analysis with selected policies |
| 3 | Parse source | PyTeal AST + TEAL regex parsing | Same via CLI | — | — | Extracts functions, asserts, state ops, tx usage |
| 4 | Apply rules | P0 rule engine (Application/Account/Fee/Asset/Logic) | Same via CLI | — | — | Violations with severity + control mapping |
| 5 | Build verdict | `verdict.build(...)` (framework, control_id, status, rules_triggered, severity, contract, timestamp) | `compliledger report ...` to preview | — | — | Compliance Verdict Object (deterministic JSON) |
| 6 | Anchor verdict | `client.mint_proof(verdict)` → hash → txn note | `compliledger anchor --verdict verdict.json` | `POST /v1/events` (optional) | PaymentTxn self-send, `note=b"CLG1|sha256:<hex>"` | TXID + explorer URL |
| 7 | Verify | `client.verify_proof(verdict, txid)` | `compliledger verify --txid ... --verdict verdict.json` | `POST /v1/verify` | Indexer lookup & note decode | Valid/Invalid + block time |
| 8 | Export report | `report(..., format="html|markdown|json")` | `compliledger report ... -o report.html` | — | — | Audit-ready report + rule matches |
| 9 | Optional watch | — | `compliledger watch contracts/` | — | — | Auto re-check on save |
| 10 | Interactive (optional) | — | `compliledger analyze --interactive` | — | — | Quick Check → if pass/waived → Anchor |

---

## v1: CI/CD (PR → Main)

| Stage | User action | SDK/CLI | Backend API | On-chain | Outcome |
|---|---|---|---|---|---|
| PR checks | Open PR | `compliledger check contracts/ --policy algorand-baseline,pci-dss-algorand --fail-on-critical` | — | — | PR fails on criticals / below threshold |
| Main merge | Merge to main | `compliledger anchor --service-signed` (CI job) | `POST /v1/events` → `POST /v1/events/:id/anchor` | Proof txn confirmed | CI outputs TXID + explorer link |
| Artifacts | — | `compliledger report ... --format html` | `POST /v1/reports` | — | HTML/JSON reports stored as artifacts |

---

## v2: Org & Policy Management (RBAC, Thresholds, Suppressions)

| Step | User action | SDK (local) | CLI | Backend API | On-chain | Output / UX |
|---|---|---|---|---|---|---|
| 1 | Sign-in & org switch | — | — | `/auth/nonce` → `/auth/verify` | — | JWT session (org-scoped) |
| 2 | Manage policy packs | `policy_pack="<org-pack-id>"` | `compliledger list-policies --org` | `GET/PUT /v1/orgs/:id/policies` | — | Enable/disable rules, thresholds, custom mappings |
| 3 | Suppressions/exceptions | Pass suppress file | `--suppress path/to/suppress.yml` | `POST /v1/suppressions` | — | Time-bound suppressions with rationale |
| 4 | Roles & approvals | — | — | `GET/PUT /v1/orgs/:id/roles`, `GET/PUT /v1/orgs/:id/approvals` | — | RBAC and approval matrix defined |

---

## v2: Approval Workflow & Anchoring Policy

| Step | User action | SDK (local) | CLI | Backend API | On-chain | Output / UX |
|---|---|---|---|---|---|---|
| 1 | Request anchoring | `client.request_anchor(event)` | `compliledger anchor --request` | `POST /v1/anchors/requests` | — | Ticket created with status "Pending" |
| 2 | Approvals | — | — | `POST /v1/anchors/:id/approve` (N-of-M) | — | Approval history captured |
| 3 | Prepare tx | — | — | `POST /v1/anchors/:id/prepare-tx` | — | Txn bytes ready |
| 4A | User-signed | — | — | — | Wallet signs & sends | Anchored with user wallet |
| 4B | Service-signed | — | — | `POST /v1/anchors/:id/execute` | Broadcast | Anchored with service wallet |
| 5 | Finalize | — | — | `GET /v1/proofs/:txid` | Confirm | Attestation artifact returned |

---

## v2: Auditor Portal & Reporting

| Step | User action | SDK (local) | CLI | Backend API | On-chain | Output / UX |
|---|---|---|---|---|---|---|
| 1 | Auditor sign-in | — | — | `/auth/nonce` → `/auth/verify` (read-only role) | — | Read-only session |
| 2 | Search proofs | — | — | `GET /v1/search?txid=&framework=&resource=` | Indexer-backed | Filtered result list |
| 3 | Verify | — | `compliledger verify --txid --event` | `POST /v1/verify` | Indexer lookup | Valid/Invalid + evidence |
| 4 | Export | — | `compliledger report ...` | `POST /v1/reports` | — | Signed HTML/MD/JSON package |

---

## v2: Compliance Explorer (Public/Org Share)

| Step | User action | SDK (local) | CLI | Backend API | On-chain | Output / UX |
|---|---|---|---|---|---|---|
| 1 | Share link | — | — | `POST /v1/shares` (scope: public/org) | — | URL generated |
| 2 | View explorer | — | — | `GET /v1/explorer?org=...` | Indexer-backed | Paginated proofs, filters, explorer links |

---

## v2: Multi-Sig Anchoring (Optional)

| Step | User action | SDK (local) | CLI | Backend API | On-chain | Output / UX |
|---|---|---|---|---|---|---|
| 1 | Configure multisig | — | — | `POST /v1/wallets/multisig` | — | Multisig address params stored |
| 2 | Prepare group | — | — | `POST /v1/events/:id/prepare-tx?multisig=1` | Multisig txn | Partially-signed blob |
| 3 | Collect signatures | — | — | `POST /v1/multisig/:id/attach` | — | Signatures collected |
| 4 | Submit | — | — | `POST /v1/multisig/:id/submit` | Submit to algod | TXID + explorer |

---

## v2: ZK Proof Attestation (Future/Optional)

| Step | User action | SDK (local) | CLI | Backend API | On-chain | Output / UX |
|---|---|---|---|---|---|---|
| 1 | Generate ZK proof | `zk.prove(result)` | `compliledger zk prove` | `POST /v1/zk/prove` | — | zkSNARK/zkVM artifact |
| 2 | Anchor proof digest | `client.mint_proof(digest)` | `compliledger anchor --digest` | `POST /v1/events` → anchor | Note carries digest | Verifiable without raw data |
| 3 | Verify | `zk.verify(...)` | `compliledger zk verify` | `POST /v1/zk/verify` | — | Proof valid/invalid |

---

Notes:
- v2 emphasizes organizational control (RBAC, policies), approvals before anchoring, auditor UX, and optional advanced attestations (multisig, ZK).
