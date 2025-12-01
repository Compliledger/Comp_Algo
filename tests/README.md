# CompALGO Test Suite

Comprehensive test suite for the CompALGO P0 implementation.

## Test Structure

```
tests/
├── conftest.py                  # Pytest configuration & fixtures
├── fixtures/                    # Test contract fixtures
│   ├── clean_escrow.py         # 0 violations (secure)
│   ├── partial_violations.py   # 2-3 violations
│   └── vulnerable.teal         # TEAL with violations
├── test_verdict_hashing.py     # TH-* tests (hashing)
├── test_rule_engine.py         # TR-* tests (rule detection)
├── test_verify_indexer.py      # TV-* tests (verification)
├── test_e2e_full_flow.py       # TE-* tests (end-to-end)
├── test_verdict.py             # Basic verdict tests (existing)
├── test_parser.py              # Parser tests (existing)
├── test_checker.py             # Checker tests (existing)
└── test_e2e_anchor.py          # Basic anchor test (existing)
```

## Running Tests

### All Tests
```bash
pytest tests/ -v
```

### By Category
```bash
pytest tests/ -v -m unit           # Unit tests only
pytest tests/ -v -m integration    # Integration tests
pytest tests/ -v -m network        # Network-dependent tests
pytest tests/ -v -m "not network"  # Skip network tests
pytest tests/ -v -m "not slow"     # Skip slow tests
```

### Specific Test Files
```bash
pytest tests/test_verdict_hashing.py -v     # Hashing tests
pytest tests/test_rule_engine.py -v         # Rule engine tests
pytest tests/test_verify_indexer.py -v      # Verification tests
pytest tests/test_e2e_full_flow.py -v       # E2E flow tests
```

### With Coverage
```bash
pytest tests/ --cov=compalgo --cov-report=html
```

## Environment Variables

Network tests require Algorand testnet access:

```bash
# Required for network tests
export ALGO_MNEMONIC="your 25 word testnet mnemonic"

# Optional (defaults provided)
export ALGO_ALGOD_URL="https://testnet-api.algonode.cloud"
export ALGO_INDEXER_URL="https://testnet-idx.algonode.cloud"
export ALGO_NETWORK="testnet"
```

## Test Markers

- `@pytest.mark.unit` - Fast unit tests, no external dependencies
- `@pytest.mark.integration` - Integration tests with multiple components
- `@pytest.mark.network` - Requires network access to Algorand
- `@pytest.mark.slow` - Takes >5 seconds to run

## Test Matrix Reference

See [P0_TEST_MATRIX.md](../P0_TEST_MATRIX.md) for the complete test plan.

### Test IDs
- **TH-001 to TH-010**: Verdict hashing tests
- **TA-001 to TA-010**: Anchor transaction tests
- **TV-001 to TV-010**: Verification tests
- **TR-001 to TR-015**: Rule engine tests
- **TE-001 to TE-010**: End-to-end flow tests

## Continuous Integration

Skip network tests in CI:
```bash
pytest tests/ -v -m "not network" --tb=short
```

Run with pytest-xdist for parallel execution:
```bash
pytest tests/ -v -n auto -m "not network"
```

## Test Fixtures

### PyTeal Contracts
- `clean_escrow.py` - Secure contract with all P0 checks
- `partial_violations.py` - Some checks missing
- `vulnerable_escrow.py` (examples/) - Multiple violations

### TEAL Contracts
- `vulnerable.teal` - Raw TEAL with violations
- `vulnerable_contract.teal` (examples/) - Existing TEAL test

## Expected Test Results

With all environment variables set:

- **Unit tests**: ~30 tests, all should pass
- **Rule engine tests**: ~15 tests, all should pass
- **Verification tests**: ~10 tests, 8+ should pass (some require Indexer)
- **E2E tests**: ~10 tests, 8+ should pass (some require network)

Total: ~65 tests, 95%+ pass rate

## Troubleshooting

### "ALGO_MNEMONIC not set"
Network tests require a funded testnet account. Get testnet ALGO from:
https://dispenser.testnet.aws.algodev.network/

### "Indexer not configured"
Some tests require Indexer for historical lookups. Set:
```bash
export ALGO_INDEXER_URL="https://testnet-idx.algonode.cloud"
```

### "Fixture not found"
Run from the repository root:
```bash
cd /path/to/Comp_Algo
pytest tests/ -v
```

### Slow test execution
Run faster subset:
```bash
pytest tests/ -v -m "unit" -n auto
```
