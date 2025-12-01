# CompALGO - CLI User Flows & Examples

Complete guide to CompALGO CLI workflows with example commands.

---

## Table of Contents

1. [Quick Analysis Flow](#quick-analysis-flow)
2. [Full Compliance Flow (Check → Anchor → Verify)](#full-compliance-flow)
3. [Multi-File Analysis Flow](#multi-file-analysis-flow)
4. [Policy Comparison Flow](#policy-comparison-flow)
5. [Report Generation Flow](#report-generation-flow)
6. [CI/CD Integration Flow](#cicd-integration-flow)
7. [Audit & Verification Flow](#audit--verification-flow)

---

## Quick Analysis Flow

**Use Case**: Quickly scan a single contract for security issues

### Step 1: Check a Contract

```bash
# Basic check with default policy (algorand-baseline)
compalgo check examples/vulnerable_escrow.py
```

**What it does**:
- Scans the PyTeal/TEAL contract
- Applies algorand-baseline policy (9 P0 rules)
- Shows violations table with severity breakdown
- Exits with code 1 if score < 80 (default threshold)

**Output**:
```
                   Compliance Check (algorand-baseline)                   
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┓
┃ File                          ┃ Score ┃ Passed ┃ Critical/High/Med/Low ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━┩
│ examples/vulnerable_escrow.py │    25 │   ❌   │        1/5/1/0        │
└───────────────────────────────┴───────┴────────┴───────────────────────┘

Details: examples/vulnerable_escrow.py
CRITICAL DELETE_WITHOUT_ADMIN_CHECK: DeleteApplication without admin check
HIGH UPDATE_WITHOUT_ADMIN_CHECK: UpdateApplication without admin check
...
```

### Step 2: Check with Specific Policy

```bash
# Use PCI-DSS Standard policy (stricter, 90% threshold)
compalgo check examples/vulnerable_escrow.py --policy pci-dss-standard
```

**What it does**:
- Applies 15 comprehensive PCI-DSS v4.0 rules
- Higher threshold (90 vs 80)
- More detailed compliance controls

### Step 3: Check with Custom Threshold

```bash
# Require 95% score to pass
compalgo check examples/vulnerable_escrow.py --threshold 95
```

**What it does**:
- Uses custom pass/fail threshold
- Useful for high-security requirements

---

## Full Compliance Flow (Check → Anchor → Verify)

**Use Case**: Generate compliance proof and anchor it on Algorand blockchain

### Step 1: Scan Contract and Generate Verdict JSON

```bash
# Scan contract and output Compliance Verdict JSON
compalgo check examples/vulnerable_escrow.py \
  --policy algorand-baseline \
  --threshold 80 \
  --verdict-out verdict.json
```

**What it does**:
- Scans contract for violations
- Generates deterministic Compliance Verdict JSON
- Saves verdict to `verdict.json`
- Verdict includes: framework, control_id, status, rules_triggered, severity, timestamp

**Output File** (`verdict.json`):
```json
{
  "framework": "SOC2",
  "control_id": "CC6.1",
  "status": "fail",
  "contract": "examples/vulnerable_escrow.py",
  "rules_triggered": [
    "DELETE_WITHOUT_ADMIN_CHECK",
    "REKEY_NOT_ZERO"
  ],
  "severity": "critical",
  "timestamp": "2025-12-01T09:24:50.327749+00:00"
}
```

### Step 2: Anchor Verdict on Algorand

```bash
# Set your Algorand testnet account mnemonic
export ALGO_MNEMONIC="your 25 word mnemonic here"

# Anchor the verdict hash on Algorand testnet
compalgo anchor --verdict verdict.json

# Or specify network explicitly
compalgo anchor \
  --verdict verdict.json \
  --network testnet \
  --algod-url https://testnet-api.algonode.cloud \
  --algod-token ""
```

**What it does**:
- Computes SHA-256 hash of canonical JSON verdict
- Sends 0-ALGO self-payment transaction with note: `CLG1|sha256:<hash>`
- Returns TXID and AlgoExplorer URL
- Proof is permanently anchored on blockchain

**Output**:
```
✅ Anchored! TXID: CTOE5M6ZZDTKD2LHLDJKACXGCG6DVA4QN67JPDZVMN73VSZV7WNA
Explorer: https://testnet.algoexplorer.io/tx/CTOE5M6ZZDTKD...
```

### Step 3: Verify Verdict Against Blockchain

```bash
# Verify that the verdict matches the on-chain proof
compalgo verify \
  --verdict verdict.json \
  --txid CTOE5M6ZZDTKD2LHLDJKACXGCG6DVA4QN67JPDZVMN73VSZV7WNA
```

**What it does**:
- Recomputes verdict hash
- Fetches transaction from Algorand
- Compares verdict hash with on-chain note
- Returns VALID or INVALID

**Output**:
```
✅ VALID
```

---

## Multi-File Analysis Flow

**Use Case**: Scan an entire project directory

### Step 1: Scan Directory

```bash
# Scan all PyTeal files in contracts/ directory
compalgo check contracts/

# Scan specific subdirectory
compalgo check src/smart_contracts/
```

**What it does**:
- Recursively scans all `.py` and `.teal` files
- Reports violations for each file
- Shows summary table
- Exits with code 1 if any file fails

**Output**:
```
                   Compliance Check (algorand-baseline)                   
┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┓
┃ File                 ┃ Score ┃ Passed ┃ Critical/High/Med/Low ┃
┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━┩
│ contracts/escrow.py  │    25 │   ❌   │        1/5/1/0        │
│ contracts/auction.py │    90 │   ✅   │        0/0/2/0        │
│ contracts/swap.py    │    75 │   ❌   │        0/2/3/1        │
└──────────────────────┴───────┴────────┴───────────────────────┘

Failed 2/3 file(s)
```

---

## Policy Comparison Flow

**Use Case**: Compare how a contract performs under different policies

### Step 1: List Available Policies

```bash
# See all available policy packs
compalgo list-policies
```

**Output**:
```
Available policies:
- algorand-baseline      (Algorand-specific PyTeal/TEAL rules) ⭐
- security-baseline      (General security patterns) ⭐
- pci-dss-algorand      (PCI-DSS subset for Algorand)
- pci-dss-basic         (Essential PCI-DSS v4.0)
- pci-dss-standard      (Comprehensive PCI-DSS v4.0)
- pci-secure-software   (PCI Secure Software Standard)
- pci-tokenization      (PCI Tokenization/TSP)
- aleo-baseline         (Cross-chain reference)
- controls_catalog      (Controls reference)

⭐ = Recommended for most Algorand projects
```

### Step 2: Test Against Different Policies

```bash
# Test with baseline (lenient)
compalgo check contract.py --policy algorand-baseline

# Test with PCI-DSS Basic (essential payment rules)
compalgo check contract.py --policy pci-dss-basic

# Test with PCI-DSS Standard (comprehensive, stricter)
compalgo check contract.py --policy pci-dss-standard --threshold 90

# Test with Secure Software Standard
compalgo check contract.py --policy pci-secure-software
```

**What it does**:
- Compares contract against different compliance frameworks
- Helps identify which policy best fits your use case
- Shows different violation patterns

---

## Report Generation Flow

**Use Case**: Export detailed compliance reports for documentation, audits, or CI/CD

### JSON Report (Machine-Readable)

```bash
# Export JSON report
compalgo report examples/vulnerable_escrow.py \
  -o reports/compliance-report.json \
  --format json \
  --policy algorand-baseline
```

**What it does**:
- Generates structured JSON with all violations
- Includes file paths, scores, violation details
- Perfect for CI/CD integration, dashboards

**Output File**:
```json
{
  "policy": "algorand-baseline",
  "results": [
    {
      "file": "examples/vulnerable_escrow.py",
      "score": 25,
      "passed": false,
      "violations": [...]
    }
  ]
}
```

### Markdown Report (Human-Readable)

```bash
# Export Markdown report
compalgo report examples/vulnerable_escrow.py \
  -o reports/compliance-report.md \
  --format markdown \
  --policy pci-dss-standard
```

**What it does**:
- Generates formatted Markdown documentation
- Ideal for README, audit docs, PR comments

**Output File**:
```markdown
# Compliance Report (pci-dss-standard)

## examples/vulnerable_escrow.py
Score: 25  Passed: No
- **CRITICAL** DELETE_WITHOUT_ADMIN_CHECK: DeleteApplication without admin check
- **HIGH** UPDATE_WITHOUT_ADMIN_CHECK: UpdateApplication without admin check
...
```

### HTML Report (Shareable)

```bash
# Export HTML report
compalgo report examples/vulnerable_escrow.py \
  -o reports/compliance-report.html \
  --format html \
  --policy algorand-baseline
```

**What it does**:
- Generates standalone HTML file
- Can be shared via email, Slack, or hosted
- No external dependencies

---

## CI/CD Integration Flow

**Use Case**: Automate compliance checks in GitHub Actions, GitLab CI, etc.

### GitHub Actions Example

```yaml
# .github/workflows/compliance.yml
name: Compliance Check

on: [push, pull_request]

jobs:
  compliance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install CompALGO
        run: pip install compalgo
      
      - name: Run Compliance Check
        run: |
          compalgo check contracts/ \
            --policy pci-dss-standard \
            --threshold 90
      
      - name: Generate Report
        if: always()
        run: |
          compalgo report contracts/ \
            -o compliance-report.json \
            --format json
      
      - name: Upload Report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: compliance-report
          path: compliance-report.json
```

### Pre-Commit Hook Example

```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "Running CompALGO compliance check..."

# Check staged PyTeal files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(py|teal)$')

if [ -n "$STAGED_FILES" ]; then
    for file in $STAGED_FILES; do
        compalgo check "$file" --policy algorand-baseline --threshold 80
        if [ $? -ne 0 ]; then
            echo "❌ Compliance check failed for $file"
            exit 1
        fi
    done
fi

echo "✅ All checks passed"
```

### Command-Line CI Flow

```bash
# 1. Scan all contracts
compalgo check contracts/ --policy pci-dss-standard --threshold 90

# 2. Generate report
compalgo report contracts/ -o report.json --format json

# 3. Parse results (using jq)
FAILED=$(cat report.json | jq -r '.results[] | select(.passed == false) | .file')

# 4. Exit with error if any failures
if [ -n "$FAILED" ]; then
    echo "Failed files: $FAILED"
    exit 1
fi
```

---

## Audit & Verification Flow

**Use Case**: Auditor verifies a previously anchored compliance proof

### Step 1: Auditor Receives Verdict and TXID

Developer provides:
- `verdict.json` (Compliance Verdict JSON)
- TXID (e.g., `CTOE5M6ZZDTKD2LHLDJKACXGCG6DVA4QN67JPDZVMN73VSZV7WNA`)
- Network (testnet or mainnet)

### Step 2: Auditor Verifies Proof

```bash
# Verify the verdict against the blockchain
compalgo verify \
  --verdict verdict.json \
  --txid CTOE5M6ZZDTKD2LHLDJKACXGCG6DVA4QN67JPDZVMN73VSZV7WNA \
  --network testnet
```

**What it does**:
- Fetches transaction from Algorand
- Computes verdict hash
- Compares with on-chain note
- Confirms verdict hasn't been tampered with

**Output**:
```
✅ VALID
```

### Step 3: Auditor Inspects Blockchain Proof

```bash
# Open AlgoExplorer to view transaction
open "https://testnet.algoexplorer.io/tx/CTOE5M6ZZDTKD2LHLDJKACXGCG6DVA4QN67JPDZVMN73VSZV7WNA"
```

**What they see**:
- Transaction timestamp (immutable)
- Note field: `CLG1|sha256:<hash>`
- Sender address
- Network confirmation

### Step 4: Auditor Re-Scans Contract (Optional)

```bash
# Re-run the scan to verify the verdict was accurate
compalgo check examples/vulnerable_escrow.py \
  --policy algorand-baseline \
  --verdict-out auditor-verdict.json

# Compare with original verdict
diff verdict.json auditor-verdict.json
```

**What it does**:
- Independently verifies the scan results
- Ensures verdict matches actual contract state
- Provides additional assurance

---

## Advanced Workflows

### Multi-Policy Audit

```bash
# Create reports for multiple compliance frameworks
for policy in algorand-baseline pci-dss-basic pci-dss-standard; do
    compalgo check contract.py --policy $policy > "audit-${policy}.txt"
done
```

### Threshold Testing

```bash
# Find minimum passing score
for threshold in 60 70 80 90 95; do
    echo "Testing threshold: $threshold"
    compalgo check contract.py --threshold $threshold
done
```

### Batch Verdict Generation

```bash
# Generate verdicts for all contracts
for contract in contracts/*.py; do
    filename=$(basename "$contract" .py)
    compalgo check "$contract" \
      --verdict-out "verdicts/verdict-${filename}.json"
done
```

### Multi-Network Anchoring

```bash
# Anchor on testnet
compalgo anchor --verdict verdict.json --network testnet

# Anchor on mainnet (for production)
export ALGO_MNEMONIC_MAINNET="mainnet mnemonic"
compalgo anchor \
  --verdict verdict.json \
  --network mainnet \
  --algod-url https://mainnet-api.algonode.cloud \
  --mnemonic "$ALGO_MNEMONIC_MAINNET"
```

---

## Environment Variables

Set these to avoid passing parameters repeatedly:

```bash
# Algorand Configuration
export ALGO_MNEMONIC="your 25 word mnemonic"
export ALGO_URL="https://testnet-api.algonode.cloud"  # or mainnet
export ALGO_TOKEN=""  # Usually empty for public nodes

# Now commands are simpler
compalgo anchor --verdict verdict.json
compalgo verify --verdict verdict.json --txid TXID
```

---

## Exit Codes

CompALGO uses standard exit codes for CI/CD integration:

- **0**: All checks passed, no violations above threshold
- **1**: One or more checks failed (score below threshold)

---

## Quick Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `check` | Scan contract(s) for violations | `compalgo check contract.py` |
| `report` | Export detailed report | `compalgo report contract.py -o report.json` |
| `list-policies` | Show available policy packs | `compalgo list-policies` |
| `anchor` | Anchor verdict on Algorand | `compalgo anchor --verdict verdict.json` |
| `verify` | Verify verdict against TXID | `compalgo verify --verdict v.json --txid TXID` |

---

## Getting Help

```bash
# Show all commands
compalgo --help

# Show help for specific command
compalgo check --help
compalgo anchor --help
compalgo verify --help
```

---

**Ready to secure your Algorand smart contracts with CompALGO!** 🚀
