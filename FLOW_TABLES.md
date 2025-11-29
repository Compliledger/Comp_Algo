# CompliLedger Algorand SDK — Flow Tables (v1 and v2)

This document captures end-to-end flows across the User UI, SDK, CLI, Backend, and Algorand on-chain.

---

## v1 (Day 1–3): Static Analysis (Algorand Baseline + PCI-DSS)

| Step | User action | SDK (local) | CLI | Backend API | On-chain | Output / UX |
|---|---|---|---|---|---|---|
| 1 | Choose policy pack(s) | `ComplianceChecker(policy_pack="algorand-baseline" or "pci-dss-algorand")` | `compliledger list-policies` | N/A | N/A | Shows available packs + rule counts |
| 2 | Run analysis on file/dir | `checker.check_file(...)` or `check_directory(...)` | `compliledger check contracts/ --policy algorand-baseline,pci-dss-algorand --threshold 80` | N/A | N/A | Starts analysis with selected policies |
| 3 | Parse source | PyTeal AST + TEAL regex parsing | Same via CLI | N/A | N/A | Extracts functions, asserts, state ops, tx usage |
| 4 | Apply rules | Baseline + PCI checks (sender check, amount validation, state guards, rekey, logging, asset safety, box size, limits, refunds, audit logs) | Same via CLI | N/A | N/A | Violations collected per rule with severity |
| 5 | Compute score | Severity-weighted scoring (0–100) | Same via CLI | N/A | N/A | Score + pass/fail vs threshold |
| 6 | View results | Python objects (violations, score, counts) | Rich terminal summary | N/A | N/A | Grouped by severity with remediation hints |
| 7 | Export report | `checker.generate_report(..., format="html|markdown|json")` | `compliledger report contracts/ --format html -o report.html` | N/A | N/A | HTML/MD/JSON reports for sharing |
| 8 | Iterate/fix | Update code, re-run | `compliledger check ... --fail-on-critical` | N/A | N/A | CI-friendly exit codes |
| 9 | Optional watch | N/A | `compliledger watch contracts/` | N/A | N/A | Auto re-check on file changes |
| 10 | Interactive (optional) | N/A | `compliledger analyze --interactive` | N/A | N/A | Menu: Quick Check, export, policy view |

---

## v1 (Day 6+): Proof Anchoring & Verification

| Step | User action | SDK (local) | CLI | Backend API | On-chain (Algorand) | Output / UX |
|---|---|---|---|---|---|---|
| 1 | Create compliance event | `client.create_compliance_event(...)` | `compliledger anchor --framework SOC2 --control CC6.1 --status pass` | `POST /v1/events` (optional) | — | Event JSON + canonical preview |
| 2 | Canonicalize + hash | `event.compute_hash()` (SHA-256) | CLI uses SDK | — | — | Stable `event_hash` |
| 3A | Prepare user-signed tx | `mint_proof()` prepares note & submits | `compliledger anchor ...` | `POST /v1/events/:id/prepare-tx` → txn bytes | — | Wallet prompt |
| 3B | Service-signed (CI) | Optional: — | `compliledger anchor --service-signed` | `POST /v1/events/:id/anchor` | Broadcast via service wallet | Lower friction CI |
| 4 | Submit & confirm | Wait 3–4 rounds | Spinner + status | `GET /v1/proofs/:txid` polling | PaymentTxn self-send, `note=b"CLG1|sha256:<hex>"` | TXID + explorer link |
| 5 | Verify proof | `verify_proof(event, txid)` | `compliledger verify --txid ... --event event.json` | `POST /v1/verify` | Indexer lookup, base64 decode note | Valid/Invalid + timestamp |
| 6 | History | — | `compliledger query --address ...` | `GET /v1/wallets/:addr/proofs` | Indexer aggregation | Paginated proofs |
| 7 | Reports | — | `compliledger report ...` | `POST /v1/reports` | — | Audit-ready HTML/MD/JSON |

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
