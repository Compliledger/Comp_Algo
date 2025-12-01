# CompliLedger Algorand SDK - Quick Start

Get started with the CompliLedger Algorand SDK in 5 minutes.

## Installation

```bash
# Clone and install
cd /path/to/Comp_Algo
pip install -e .

# Verify installation
compliledger --help
```

## Prerequisites

- Python 3.8+
- Algorand account with testnet ALGOs (for anchoring)
- Your account's 25-word mnemonic

**Get testnet ALGOs**: https://bank.testnet.algorand.network/

## 1. Scan a Contract

```bash
# Scan PyTeal contract
compliledger check examples/vulnerable_escrow.py

# Scan TEAL contract
compliledger check examples/vulnerable_contract.teal

# Use different policy
compliledger check examples/vulnerable_escrow.py --policy pci-dss-algorand

# Set custom threshold
compliledger check examples/vulnerable_escrow.py --threshold 90
```

**Output:**
```
Compliance Check (algorand-baseline)
┏━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┓
┃ File            ┃ Score ┃ Passed ┃ Critical/High/Med/Low ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━┩
│ vulnerable.py   │    25 │   ❌   │        1/5/1/0        │
└─────────────────┴───────┴────────┴───────────────────────┘
```

## 2. Generate Compliance Verdict

```bash
# Create verdict JSON (required for anchoring)
compliledger check examples/vulnerable_escrow.py --verdict-out my_verdict.json
```

**Creates:** `my_verdict.json`
```json
{
  "framework": "SOC2",
  "control_id": "CC6.1",
  "status": "fail",
  "contract": "examples/vulnerable_escrow.py",
  "rules_triggered": ["DELETE_WITHOUT_ADMIN_CHECK", "REKEY_NOT_ZERO"],
  "severity": "critical",
  "timestamp": "2024-12-01T09:24:50Z"
}
```

## 3. Anchor on Algorand

```bash
# Set your mnemonic
export ALGO_MNEMONIC="your 25 word mnemonic here"

# Anchor verdict on testnet
compliledger anchor --verdict my_verdict.json

# Or specify network explicitly
compliledger anchor \
  --verdict my_verdict.json \
  --network testnet \
  --algod-url https://testnet-api.algonode.cloud
```

**Output:**
```
✅ Anchored! TXID: CTOE5M6ZZDTKD2LHLDJKACXGCG6DVA4QN67JPDZVMN73VSZV7WNA
Explorer: https://testnet.algoexplorer.io/tx/CTOE5M6ZZ...
```

## 4. Verify Proof

```bash
# Verify verdict against blockchain
compliledger verify \
  --verdict my_verdict.json \
  --txid CTOE5M6ZZDTKD2LHLDJKACXGCG6DVA4QN67JPDZVMN73VSZV7WNA
```

**Output:**
```
✅ VALID
```

## 5. Export Reports

```bash
# JSON report
compliledger report examples/vulnerable_escrow.py \
  -o report.json \
  --format json

# Markdown report
compliledger report examples/vulnerable_escrow.py \
  -o report.md \
  --format markdown

# HTML report
compliledger report examples/vulnerable_escrow.py \
  -o report.html \
  --format html
```

## Python API Example

```python
from compliledger_algorand import ComplianceChecker, CompliLedgerClient
from compliledger_algorand.core.verdict import build_verdict

# 1. Scan
checker = ComplianceChecker(policy_pack="algorand-baseline")
result = checker.check_file("examples/vulnerable_escrow.py")

print(f"Score: {result.score}/100")
print(f"Violations: {len(result.violations)}")

# 2. Build verdict
verdict = build_verdict(
    contract=result.file_path,
    violations=result.violations,
    framework="SOC2",
    control_id="CC6.1",
    fail_on="medium"
)

# 3. Anchor
client = CompliLedgerClient(
    algod_url="https://testnet-api.algonode.cloud",
    algod_token="",
    sender_mnemonic="your mnemonic",
    network="testnet"
)

anchor_result = client.mint_verdict(verdict)
print(f"Anchored: {anchor_result.explorer_url}")

# 4. Verify
is_valid = client.verify_verdict(verdict, anchor_result.txid)
print(f"Valid: {is_valid}")
```

## Run Demo

```bash
export ALGO_MNEMONIC="your 25 word mnemonic"
python3 demo_p0.py
```

## Run Tests

```bash
# All tests (including E2E on testnet)
export ALGO_MNEMONIC="your mnemonic"
python3 tests/run_tests.py

# Individual test suites
python3 tests/test_verdict.py
python3 tests/test_parser.py
python3 tests/test_checker.py
python3 tests/test_e2e_anchor.py
```

## Available Policies

```bash
compliledger list-policies
```

- **algorand-baseline**: P0 baseline (9 rules)
- **pci-dss-algorand**: PCI-DSS subset (3 rules)

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ALGO_MNEMONIC` | - | Your 25-word mnemonic (required for anchoring) |
| `ALGO_URL` | `https://testnet-api.algonode.cloud` | Algorand node URL |
| `ALGO_TOKEN` | `""` | Algorand API token (empty for public nodes) |

## P0 Rules

1. **DELETE_WITHOUT_ADMIN_CHECK** (CRITICAL)
2. **UPDATE_WITHOUT_ADMIN_CHECK** (CRITICAL)
3. **REKEY_NOT_ZERO** (CRITICAL)
4. **CLOSEREMAINDER_NOT_ZERO** (CRITICAL)
5. **MISSING_ADMIN_SENDER_CHECK** (HIGH)
6. **MISSING_ARG_VALIDATION** (HIGH)
7. **STATE_MUTATION_UNGUARDED** (HIGH)
8. **INNER_TXN_UNGUARDED** (HIGH)
9. **EXCESSIVE_FEE_UNBOUNDED** (MEDIUM)

See `SECURITY_RULES.md` for details.

## Next Steps

- Read the full [README.md](README.md)
- Review [SECURITY_RULES.md](SECURITY_RULES.md) for rule details
- Check [DEV_10_DAY_PLAN.md](DEV_10_DAY_PLAN.md) for roadmap
- Explore [examples/](examples/) for test contracts

## Support

- GitHub Issues: [Report bugs or request features]
- Documentation: See `README.md` and `SECURITY_RULES.md`
- Community: [TBD - Discord/Telegram]

---

**Ready to ship secure Algorand contracts with immutable compliance proofs!** 🚀
