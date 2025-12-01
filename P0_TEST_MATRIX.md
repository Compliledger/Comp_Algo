# CompALGO P0 Test Matrix

**Purpose**: Comprehensive testing strategy for P0-ready CompALGO SDK  
**Scope**: Analyze → Event → Hash → Anchor → Verify flow  
**Date**: December 2024

---

## Test Categories

### 1. Event Hashing Tests
**Target**: Deterministic canonical JSON + SHA-256  
**Location**: `tests/test_verdict_hashing.py`

| Test ID | Description | Input | Expected Output | Status |
|---------|-------------|-------|-----------------|--------|
| TH-001 | Canonical JSON determinism | Same verdict object created twice | Identical JSON strings | ✅ Implemented |
| TH-002 | Hash determinism | Same verdict data | Identical SHA-256 hashes | ✅ Implemented |
| TH-003 | Hash uniqueness | Different verdict status | Different hashes | ✅ Implemented |
| TH-004 | Key ordering | Verdict with unordered fields | Sorted keys in JSON | ✅ Implemented |
| TH-005 | Compact format | Canonical JSON | No spaces after `:` or `,` | ✅ Implemented |
| TH-006 | Unicode handling | Verdict with unicode chars | Correct UTF-8 encoding | 🆕 NEW |
| TH-007 | Large rule lists | 100+ rules triggered | Deterministic ordering | 🆕 NEW |
| TH-008 | Timestamp precision | Microsecond timestamps | Preserved in hash | 🆕 NEW |
| TH-009 | Empty verdict | No violations | Valid hash | 🆕 NEW |
| TH-010 | Metadata inclusion | Verdict with metadata field | Included in hash | 🆕 NEW |

---

### 2. Anchor Tests (On-Chain)
**Target**: PaymentTxn-to-self with `CLG1|sha256:<hash>` note  
**Location**: `tests/test_anchor_txn.py`

| Test ID | Description | Input | Expected Output | Status |
|---------|-------------|-------|-----------------|--------|
| TA-001 | Basic anchor | Simple verdict | TXID returned | ✅ Implemented |
| TA-002 | Note format | Anchored txn | Note = `CLG1\|sha256:<hex>` | ✅ Implemented |
| TA-003 | Explorer URL | TXID on testnet | Valid AlgoExplorer URL | ✅ Implemented |
| TA-004 | Mainnet anchor | Same verdict | Mainnet explorer URL | 🆕 NEW |
| TA-005 | Fee handling | Anchor with min fee | Fee >= 1000 microALGO | 🆕 NEW |
| TA-006 | Account balance | Insufficient balance | Error raised | 🆕 NEW |
| TA-007 | Network error | Algod offline | Connection error | 🆕 NEW |
| TA-008 | Duplicate anchor | Same verdict twice | Different TXIDs | 🆕 NEW |
| TA-009 | Large note | Verdict hash + metadata | Fits in note field | 🆕 NEW |
| TA-010 | Transaction confirmation | Anchored txn | Confirmed in 4 rounds | ✅ Implemented |

---

### 3. Verify Tests (Using Indexer)
**Target**: Fetch txn by TXID, decode note, compare hash  
**Location**: `tests/test_verify_indexer.py`

| Test ID | Description | Input | Expected Output | Status |
|---------|-------------|-------|-----------------|--------|
| TV-001 | Valid verification | Correct verdict + TXID | `True` | ✅ Implemented |
| TV-002 | Tamper detection | Modified verdict + original TXID | `False` | ✅ Implemented |
| TV-003 | Wrong TXID | Valid verdict + random TXID | `False` or error | 🆕 NEW |
| TV-004 | Historical proof | 30-day old TXID | `True` (requires Indexer) | 🆕 NEW |
| TV-005 | Non-CLG transaction | Random TXID | `False` | 🆕 NEW |
| TV-006 | Malformed note | TXID with bad note format | `False` | 🆕 NEW |
| TV-007 | Indexer fallback | Algod fails → Indexer lookup | `True` | 🆕 NEW |
| TV-008 | Multi-network verify | Testnet TXID on mainnet client | Error or `False` | 🆕 NEW |
| TV-009 | Partial hash match | Note with truncated hash | `False` | 🆕 NEW |
| TV-010 | Concurrent verification | 10 verdicts in parallel | All correct results | 🆕 NEW |

---

### 4. Rule Engine Tests (PyTeal/TEAL)
**Target**: 9 P0 rules on various contracts  
**Location**: `tests/test_rule_engine.py`

| Test ID | Description | Contract Type | Expected Violations | Status |
|---------|-------------|---------------|---------------------|--------|
| TR-001 | Clean contract | Secure escrow | 0 violations | 🆕 NEW |
| TR-002 | Missing sender check | Admin function without check | `MISSING_ADMIN_SENDER_CHECK` | ✅ Implemented |
| TR-003 | Unsafe rekey | No RekeyTo == 0 assertion | `REKEY_NOT_ZERO` | ✅ Implemented |
| TR-004 | Unsafe close | No CloseRemainderTo check | `CLOSEREMAINDER_NOT_ZERO` | 🆕 NEW |
| TR-005 | Delete without auth | DeleteApplication unguarded | `DELETE_WITHOUT_ADMIN_CHECK` | ✅ Implemented |
| TR-006 | Update without auth | UpdateApplication unguarded | `UPDATE_WITHOUT_ADMIN_CHECK` | ✅ Implemented |
| TR-007 | Unvalidated args | Txn.application_args used raw | `MISSING_ARG_VALIDATION` | ✅ Implemented |
| TR-008 | State mutation | App.globalPut without check | `STATE_MUTATION_UNGUARDED` | ✅ Implemented |
| TR-009 | Inner txn unguarded | InnerTxn without validation | `INNER_TXN_UNGUARDED` | 🆕 NEW |
| TR-010 | Unbounded fees | Txn.fee not limited | `EXCESSIVE_FEE_UNBOUNDED` | 🆕 NEW |
| TR-011 | Combined violations | Multiple issues | All detected | ✅ Implemented |
| TR-012 | TEAL opcode detection | Pure TEAL file | Rules triggered | ✅ Implemented |
| TR-013 | Complex PyTeal | Nested Seq/Cond/If | Correct detection | 🆕 NEW |
| TR-014 | Score calculation | 1 critical + 2 high | Score = 60 | ✅ Implemented |
| TR-015 | Threshold pass/fail | Score 79 vs 81 (threshold 80) | Correct pass/fail | 🆕 NEW |

---

### 5. End-to-End Flow Tests
**Target**: Full analyze → verdict → anchor → verify pipeline  
**Location**: `tests/test_e2e_full_flow.py`

| Test ID | Description | Steps | Expected Result | Status |
|---------|-------------|-------|-----------------|--------|
| TE-001 | Happy path | Clean contract → anchor | Pass verdict, valid proof | 🆕 NEW |
| TE-002 | Violation flow | Vulnerable contract → anchor | Fail verdict, valid proof | ✅ Partial (demo) |
| TE-003 | Multiple contracts | 3 files → 3 verdicts → anchor | 3 TXIDs, all verifiable | 🆕 NEW |
| TE-004 | Policy comparison | Same contract, 2 policies | Different violations | 🆕 NEW |
| TE-005 | CLI workflow | `check → anchor → verify` | Success chain | 🆕 NEW |
| TE-006 | API workflow | Python SDK end-to-end | Programmatic success | ✅ Implemented |
| TE-007 | Verify after 24h | Anchor → wait → verify | Still valid (Indexer) | 🆕 NEW |
| TE-008 | Cross-session verify | Anchor in session 1, verify in 2 | Valid | 🆕 NEW |
| TE-009 | Mainnet production | Real contract on mainnet | Live proof URL | 🆕 NEW |
| TE-010 | Failure recovery | Network error → retry | Eventual success | 🆕 NEW |

---

## Test Contracts

### Test Contract 1: Clean Escrow (0 violations)
**File**: `tests/fixtures/clean_escrow.py`

```python
# Secure escrow with all P0 checks
- Admin sender verification: ✅
- RekeyTo == 0 check: ✅
- CloseRemainderTo == 0 check: ✅
- Arg validation: ✅
- State mutations guarded: ✅
```

### Test Contract 2: Vulnerable Escrow (7+ violations)
**File**: `examples/vulnerable_escrow.py` (already exists)

```python
# Missing checks (intentional)
- DELETE_WITHOUT_ADMIN_CHECK: ❌
- REKEY_NOT_ZERO: ❌
- MISSING_ARG_VALIDATION: ❌
- STATE_MUTATION_UNGUARDED: ❌
- UPDATE_WITHOUT_ADMIN_CHECK: ❌
- EXCESSIVE_FEE_UNBOUNDED: ❌
```

### Test Contract 3: Partial Violations (2-3 violations)
**File**: `tests/fixtures/partial_violations.py`

```python
# Some checks present, some missing
- Admin checks: ✅
- RekeyTo check: ❌
- Arg validation: ❌
```

### Test Contract 4: TEAL Only
**File**: `tests/fixtures/vulnerable.teal`

```teal
# TEAL opcodes for detection
- app_global_del (unguarded)
- txna RekeyTo (not checked)
- app_global_put (no sender check)
```

---

## Environment Setup

### Required Environment Variables

```bash
# For anchor & verify tests
export ALGO_MNEMONIC="your 25 word mnemonic here"
export ALGO_MNEMONIC_2="second account for multi-account tests"

# Algorand endpoints
export ALGO_ALGOD_URL="https://testnet-api.algonode.cloud"
export ALGO_ALGOD_TOKEN=""
export ALGO_INDEXER_URL="https://testnet-idx.algonode.cloud"
export ALGO_INDEXER_TOKEN=""

# Network selection
export ALGO_NETWORK="testnet"  # or "mainnet"
```

### Test Fixtures Directory

```
tests/
├── fixtures/
│   ├── clean_escrow.py          # 0 violations
│   ├── partial_violations.py    # 2-3 violations
│   ├── vulnerable.teal          # TEAL with violations
│   └── complex_nested.py        # Complex PyTeal patterns
├── test_verdict_hashing.py      # Hashing tests (TH-*)
├── test_anchor_txn.py           # Anchor tests (TA-*)
├── test_verify_indexer.py       # Verify tests (TV-*)
├── test_rule_engine.py          # Rule tests (TR-*)
├── test_e2e_full_flow.py        # E2E tests (TE-*)
└── conftest.py                  # Pytest fixtures & config
```

---

## Test Execution

### Run All Tests
```bash
pytest tests/ -v --tb=short
```

### Run by Category
```bash
pytest tests/test_verdict_hashing.py -v   # Hashing only
pytest tests/test_anchor_txn.py -v        # Anchor only
pytest tests/test_verify_indexer.py -v    # Verify only
pytest tests/test_rule_engine.py -v       # Rules only
pytest tests/test_e2e_full_flow.py -v     # E2E only
```

### Skip Network Tests (for CI without secrets)
```bash
pytest tests/ -v -m "not network"
```

### Run Only Network Tests (with env vars set)
```bash
pytest tests/ -v -m "network"
```

---

## Coverage Goals

| Component | Target Coverage | Current | Gap |
|-----------|-----------------|---------|-----|
| `verdict.py` | 100% | ~90% | Hash edge cases |
| `checker.py` | 90% | ~80% | Policy loading |
| `algorand.py` | 85% | ~70% | Indexer integration |
| `parser.py` | 80% | ~75% | Complex PyTeal |
| `cli/main.py` | 70% | ~60% | CLI commands |
| **Overall** | **85%** | **75%** | **10%** |

---

## Test Markers (pytest)

```python
# Mark network-dependent tests
@pytest.mark.network
def test_anchor_on_testnet():
    ...

# Mark slow tests
@pytest.mark.slow
def test_historical_verification():
    ...

# Mark integration tests
@pytest.mark.integration
def test_e2e_flow():
    ...

# Mark unit tests
@pytest.mark.unit
def test_hash_determinism():
    ...
```

---

## Success Criteria

### P0 Ready Checklist

- ✅ All TH (hashing) tests pass
- ✅ All TA (anchor) tests pass on testnet
- ✅ All TV (verify) tests pass with Indexer
- ✅ All TR (rule) tests detect violations correctly
- ✅ All TE (E2E) tests complete successfully
- ✅ Test coverage >= 85%
- ✅ No hardcoded secrets in code
- ✅ CI/CD pipeline green
- ✅ Example script runs without errors
- ✅ Documentation updated

---

## Next Steps After Testing

1. **Bug Fixes**: Address any test failures
2. **Indexer Integration**: Complete TV-004, TV-007 (historical verification)
3. **Performance**: Benchmark anchor/verify speed
4. **Security Audit**: Review mnemonic handling
5. **Documentation**: Update README with test results
6. **CI/CD**: Add GitHub Actions workflow
7. **PyPI Release**: Publish v0.1.0

---

**Status Legend**:
- ✅ Implemented & Passing
- 🆕 NEW - To be implemented
- ⚠️ Partial - Needs completion
- ❌ Failing - Needs fix
