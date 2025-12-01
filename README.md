# 🔒 CompALGO – Algorand Smart Contract Compliance Analyzer

**Static Analysis + On-Chain Proof Anchoring for Algorand Smart Contracts**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Algorand](https://img.shields.io/badge/Algorand-Ready-00D4AA.svg)](https://algorand.com)

**SOC 2** • **PCI DSS** • **FedRAMP** • **Smart Contract Security**

---

## 🎯 What is CompALGO?

CompALGO is a comprehensive compliance and security toolkit for Algorand smart contracts that provides **two powerful capabilities**:

### 1. 🛡️ Smart Contract Security Analysis
Analyze PyTeal and TEAL contracts for vulnerabilities and compliance issues during development with **8 policy packs** covering PCI-DSS, SOC2, and security best practices.

### 2. 🔐 Compliance Proof Anchoring
Create cryptographically verifiable compliance verdicts and anchor them immutably on the Algorand blockchain for audit trails and regulatory evidence.

---

## 📚 Documentation

- **[CLI User Flows & Examples](CLI_USER_FLOWS.md)** - Complete guide with step-by-step workflows
- **[Security Rules Reference](SECURITY_RULES.md)** - All P0 rules and detection logic
- **[Quick Start Guide](QUICKSTART.md)** - Get started in 5 minutes

---

## ✨ Features

### Proof-of-Compliance Anchoring
- ✅ Create structured compliance event objects
- ✅ Hash compliance data locally (SHA-256)
- ✅ Anchor proof hashes on Algorand via transaction notes
- ✅ Provide verifiable on-chain timestamps
- ✅ Query and verify historical proofs
- ✅ Works on testnet and mainnet (~0.001 ALGO per proof)

### Smart Contract Security Analysis
- 🔍 Static analysis for PyTeal and TEAL
- 🛡️ 15+ security rules (access control, reentrancy, overflow)
- 💳 PCI-DSS compliance for payment/DeFi apps
- 📊 Smart scoring system (0-100)
- 🎨 Beautiful interactive CLI
- 📈 Export formats (JSON, HTML, Markdown)
- 🤖 CI/CD ready (GitHub Actions, GitLab CI)
- 🔒 **100% local** - code never leaves your machine

---

## 🚀 Why Algorand?

- **Immutable Proof-of-Compliance** – Cryptographic anchors on Layer-1
- **Low-Cost High-Frequency** – Enterprise scale at ~0.001 ALGO per proof
- **Fast Finality** – Proofs verifiable in ~3.3 seconds
- **Carbon Neutral** – Sustainable enterprise compliance
- **No Bridge Risk** – Layer-1 security without wrapped tokens

Algorand is not just storage — **it's the trust layer for CompliLedger**.

---

## 📦 Installation

```bash
# Install CompALGO
pip install compalgo

# With interactive menu mode
pip install compalgo[interactive]

# With file watching (auto-check on save)
pip install compalgo[watch]

# Development install
git clone https://github.com/compliledger/compalgo.git
cd compalgo
pip install -e .
```

---

## 🎬 Quickstart

### 1️⃣ Scan a Contract

```bash
# Quick security scan with default policy
compalgo check examples/escrow.py

# Scan with specific policy and threshold
compalgo check contracts/payment.py --policy pci-dss-standard --threshold 90

# Scan entire directory
compalgo check contracts/
```

### 2️⃣ Generate Compliance Verdict

```bash
# Scan and create verdict JSON
compalgo check examples/escrow.py --verdict-out verdict.json

# View all available policies
compalgo list-policies
```

### 3️⃣ Anchor Proof on Algorand

```bash
# Set your Algorand account (testnet)
export ALGO_MNEMONIC="your 25 word mnemonic here"

# Anchor the verdict hash on Algorand blockchain
compalgo anchor --verdict verdict.json

# Output:
# ✅ Anchored! TXID: CTOE5M6ZZD...
# Explorer: https://testnet.algoexplorer.io/tx/CTOE5M6ZZD...
```

### 4️⃣ Verify Proof

```bash
# Verify verdict against blockchain
compalgo verify --verdict verdict.json --txid CTOE5M6ZZD...

# Output:
# ✅ VALID
```

### 5️⃣ Python API

```python
from compalgo import ComplianceChecker, CompliLedgerClient
from compalgo.core.verdict import build_verdict

# Scan contract
checker = ComplianceChecker(policy_pack="algorand-baseline", threshold=80)
result = checker.check_file("contract.py")

# Build compliance verdict
verdict = build_verdict(
    contract=result.file_path,
    violations=result.violations,
    framework="SOC2",
    control_id="CC6.1",
    fail_on="medium"
)

# Anchor on Algorand
client = CompliLedgerClient(
    algod_url="https://testnet-api.algonode.cloud",
    algod_token="",
    sender_mnemonic="your mnemonic",
    network="testnet"
)
anchor_result = client.mint_verdict(verdict)
print(f"TXID: {anchor_result.txid}")
print(f"Explorer: {anchor_result.explorer_url}")

# Verify
is_valid = client.verify_verdict(verdict, anchor_result.txid)
assert is_valid  # ✅ True
```

---

## 📋 Supported Frameworks

| Framework | Controls | Use Case |
|-----------|----------|----------|
| **SOC 2** | Trust Services | SaaS & Web3 infrastructure |
| **PCI DSS** | Payment Security | Payment & crypto custody |
| **FedRAMP** | Federal Baseline | Government cloud services |
| **Algorand Security** | Smart contracts | dApp development |

---

## 💻 CLI Commands & User Flows

CompALGO provides a comprehensive CLI for all workflows. See **[CLI_USER_FLOWS.md](CLI_USER_FLOWS.md)** for complete examples.

### Quick Reference

```bash
# Scan contracts
compalgo check contract.py                    # Quick scan
compalgo check contracts/ --policy pci-dss-standard  # Directory scan
compalgo check contract.py --threshold 95      # Custom threshold
compalgo check contract.py --verdict-out v.json  # Generate verdict

# Export reports
compalgo report contract.py -o report.json --format json
compalgo report contract.py -o report.md --format markdown
compalgo report contract.py -o report.html --format html

# Policy management
compalgo list-policies                        # Show all policies

# Blockchain anchoring
export ALGO_MNEMONIC="your 25 word mnemonic"
compalgo anchor --verdict verdict.json        # Anchor on testnet
compalgo anchor --verdict v.json --network mainnet  # Anchor on mainnet

# Verification
compalgo verify --verdict verdict.json --txid TXID  # Verify proof
```

### Available User Flows

1. **Quick Analysis Flow** - Fast security scan
2. **Full Compliance Flow** - Check → Anchor → Verify
3. **Multi-File Analysis** - Scan entire projects
4. **Policy Comparison** - Test multiple policies
5. **Report Generation** - Export JSON/HTML/Markdown
6. **CI/CD Integration** - GitHub Actions, GitLab CI
7. **Audit & Verification** - Independent proof verification

👉 **See [CLI_USER_FLOWS.md](CLI_USER_FLOWS.md) for complete step-by-step examples**

### Available Policy Packs

Run `compalgo list-policies` to see all 9 available policy packs:

| Policy Pack | Rules | Threshold | Target |
|-------------|-------|-----------|--------|
| **algorand-baseline** ⭐ | 9 | 80 | Algorand-specific (PyTeal/TEAL) |
| **security-baseline** ⭐ | 10 | 75 | General security patterns (all chains) |
| **pci-dss-algorand** | 3 | 80 | Algorand payment subset |
| **pci-dss-basic** | 7 | 85 | Payment/DeFi (essential) |
| **pci-dss-standard** | 15 | 90 | Payment/DeFi (comprehensive) |
| **pci-secure-software** | 7 | 90 | Software vendors |
| **pci-tokenization** | 4 | 90 | Token service providers |

⭐ = Recommended for most Algorand projects

---

## 🔐 Compliance Verdict Examples

### PCI DSS Payment Contract Analysis

```python
from compalgo import ComplianceChecker, CompliLedgerClient
from compalgo.core.verdict import build_verdict

# Scan payment contract with PCI-DSS Standard policy
checker = ComplianceChecker(policy_pack="pci-dss-standard", threshold=90)
result = checker.check_file("contracts/payment_app.py")

print(f"Score: {result.score}/100")
print(f"Violations: {len(result.violations)}")

# Build compliance verdict
verdict = build_verdict(
    contract=result.file_path,
    violations=result.violations,
    framework="PCI-DSS",
    control_id="6.5.1",
    fail_on="high"
)

# If compliant, anchor proof on Algorand
if result.passed:
    client = CompliLedgerClient(
        algod_url="https://testnet-api.algonode.cloud",
        algod_token="",
        sender_mnemonic=os.getenv("ALGO_MNEMONIC"),
        network="testnet"
    )
    anchor_result = client.mint_verdict(verdict)
    print(f"✅ Proof anchored: {anchor_result.explorer_url}")
```

### SOC 2 Access Control Verification

```python
from compalgo import ComplianceChecker
from compalgo.core.verdict import build_verdict

# Check contract for SOC 2 compliance (access controls)
checker = ComplianceChecker(policy_pack="algorand-baseline", threshold=80)
result = checker.check_file("contracts/auth_contract.py")

# Build SOC 2 verdict
verdict = build_verdict(
    contract=result.file_path,
    violations=result.violations,
    framework="SOC2",
    control_id="CC6.1",  # Logical and Physical Access Controls
    fail_on="medium"
)

# Verdict includes: status, severity, rules_triggered, timestamp
print(f"Status: {verdict.status}")
print(f"Severity: {verdict.severity}")
print(f"Rules triggered: {verdict.rules_triggered}")
```

### Multi-Policy Comparison

```python
from compalgo import ComplianceChecker

policies = ["algorand-baseline", "pci-dss-basic", "pci-dss-standard"]
contract = "contracts/payment.py"

for policy in policies:
    checker = ComplianceChecker(policy_pack=policy)
    result = checker.check_file(contract)
    print(f"{policy}: Score={result.score}, Passed={result.passed}")
```

---

## 🛡️ Smart Contract Security Checks

### Algorand-Specific Rules

**Access Control**
- ✅ Missing sender verification
- ✅ Unprotected admin functions
- ✅ Missing RBAC

**Input Validation**
- ✅ Unvalidated transaction amounts
- ✅ Missing bounds checks
- ✅ Unsafe type conversions

**State Management**
- ✅ Unprotected global state mutations
- ✅ Missing state existence checks
- ✅ Race conditions

**Asset Security**
- ✅ Unsafe asset transfers
- ✅ Missing asset freeze checks
- ✅ Clawback vulnerabilities

**Payment Security (PCI-DSS)**
- ✅ Forbidden data storage (CVV, PIN)
- ✅ Cardholder data exposure
- ✅ Payment input validation
- ✅ Transaction limits
- ✅ Refund mechanisms
- ✅ Audit logging

**Logic & Optimization**
- ✅ Reentrancy risks
- ✅ Integer overflow/underflow
- ✅ Unchecked return values
- ✅ Gas optimization

### Example Security Report

```
╭────────────────────── ⚠️  5 Violation(s) Found ──────────────────────╮
│ 🔴 CRITICAL: 2 issue(s)                                              │
│   • Missing sender verification in admin function                    │
│     → contracts/payment_app.py:45                                    │
│     💡 Add: Assert(Txn.sender() == Global.creator_address())        │
│                                                                      │
│   • Cardholder data stored in global state (PCI-DSS 3.4)           │
│     → contracts/payment_app.py:78                                    │
│     💡 Use local state or encryption                                │
│                                                                      │
│ ⚠️  HIGH: 3 issue(s)                                                  │
│   • Payment amount not validated (PCI-DSS 6.5.1)                    │
│   • Missing transaction logging                                      │
│   • Potential integer overflow                                       │
│                                                                      │
│ Score: 62/100 - NON COMPLIANT ❌                                     │
╰──────────────────────────────────────────────────────────────────────╯

✅ 42 checks passed  ⚠️ 3 warnings  ❌ 2 critical
```

---

## 📋 Policy Packs

| Policy Pack | Status | Controls | Focus Area |
|-------------|--------|----------|------------|
| `algorand-baseline` | ✅ Available | 15+ | PyTeal/TEAL security |
| `pci-dss-algorand` | ✅ Available | 7 | Payment & DeFi |
| `soc2-algorand` | 🚧 v0.2.0 | 25+ | Trust Services |
| `fedramp-algorand` | 🚧 v0.3.0 | 50+ | Federal security |
| `iso-27001` | 🚧 v0.4.0 | 114 | InfoSec mgmt |

```bash
# Use specific policy
compliledger check contracts/ --policy pci-dss-algorand

# Use multiple policies
compliledger check contracts/ --policy algorand-baseline,pci-dss-algorand
```

---

## 🤖 CI/CD Integration

### GitHub Actions

```yaml
name: CompliLedger Security

on: [pull_request, push]

jobs:
  security-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install CompliLedger
        run: pip install compliledger-algorand
      
      - name: Run Security Analysis
        run: |
          compliledger check contracts/ \
            --fail-on-critical \
            --threshold 80
      
      - name: Anchor Proof (main branch only)
        if: github.ref == 'refs/heads/main'
        env:
          ALGORAND_MNEMONIC: ${{ secrets.ALGORAND_MNEMONIC }}
        run: |
          compliledger anchor \
            --framework SOC2 \
            --control CC6.1 \
            --status pass
```

### Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "🔍 Running CompliLedger security analysis..."

compliledger check contracts/ --threshold 75 --fail-on-critical

if [ $? -ne 0 ]; then
    echo "❌ Security check failed. Fix issues before committing."
    exit 1
fi

echo "✅ Security check passed!"
```

---

## 🔬 Python API

### Proof Anchoring API

```python
from compliledger_algorand import CompliLedgerClient

# Initialize
client = CompliLedgerClient(
    algod_url="https://testnet-api.algonode.cloud",
    algod_token="",
    sender_mnemonic="your mnemonic",
    network="testnet"
)

# Create and anchor
event = client.create_compliance_event(
    framework="SOC2",
    control_id="CC6.1",
    status="pass",
    resource="payment-service"
)

proof = client.mint_proof(event)

# Verify
is_valid = client.verify_proof(event, proof.txid)
assert is_valid

# Query history
proofs = client.query_proofs(
    framework="SOC2",
    from_date="2025-01-01"
)
```

### Smart Contract Analysis API

```python
from compliledger_algorand.analyzer import ComplianceChecker

# Initialize checker
checker = ComplianceChecker(
    policy_pack="algorand-baseline",
    threshold=80
)

# Check single file
result = checker.check_file("contracts/payment_app.py")

print(f"Score: {result.score}/100")
print(f"Violations: {len(result.violations)}")

for v in result.violations:
    print(f"{v.severity}: {v.message} at line {v.line_number}")

# Check directory
results = checker.check_directory("contracts/")

# Generate report
checker.generate_report(
    results,
    format="html",
    output_path="compliance_report.html"
)
```

---

## 🏗️ How It Works

### Proof Anchoring Flow

```
1. Developer creates compliance event
   ↓
2. SDK hashes event locally (SHA-256)
   ↓
3. Hash written to Algorand transaction note
   ↓
4. Blockchain provides immutable timestamp
   ↓
5. Anyone can verify proof on-chain
   ↓
6. Original data stays private
```

### Smart Contract Analysis Flow

```
1. Developer writes PyTeal/TEAL contract
   ↓
2. SDK parses code (AST extraction)
   ↓
3. Pattern matching against security rules
   ↓
4. Severity scoring (0-100)
   ↓
5. Generate actionable remediation suggestions
   ↓
6. Export reports or fail CI/CD
```

---

## 🎯 Use Cases

### Compliance Proof Anchoring
- **SOC 2** control checks in CI/CD
- **PCI DSS** evidence for Web3 payment systems
- **FedRAMP** audit trails
- SBOM verification
- Evidence immutability for legal workflows
- Regulator-ready reporting

### Smart Contract Security
- Pre-deployment security audits
- Continuous compliance monitoring
- Payment contract PCI-DSS validation
- DeFi protocol security checks
- NFT marketplace access control verification
- Automated security in CI/CD pipelines

---

## 🗺️ Roadmap

### v0.1.0 (Current)
- ✅ Basic proof anchoring on Algorand
- ✅ PyTeal/TEAL static analysis
- ✅ 15+ security rules
- ✅ PCI-DSS policy pack
- ✅ Interactive CLI
- ✅ CI/CD integration

### v0.2.0 (Q1 2025)
- 🚧 SOC 2 policy pack for dApps
- 🚧 Advanced reentrancy detection
- 🚧 Box storage security checks
- 🚧 State proof verification
- 🚧 GitHub App integration

### v0.3.0 (Q2 2025)
- 🚧 FedRAMP policy pack
- 🚧 Zero-knowledge proof support
- 🚧 Proof-of-Compliance NFTs
- 🚧 Multi-signature proof anchoring
- 🚧 VS Code extension

### v0.4.0 (Q3 2025)
- 🚧 ISO 27001 policy pack
- 🚧 AI-powered auto-fix suggestions
- 🚧 Compliance marketplace
- 🚧 Cross-chain proof verification
- 🚧 Enterprise API service

---

## 🔒 Why 100% Local?

Your smart contract code **never leaves your machine**:

- ✅ **No Data Leakage** – Code stays on your machine
- ✅ **Works Offline** – Zero network dependency for analysis
- ✅ **Deterministic** – Same code = same results always
- ✅ **Fast** – <100ms analysis vs 2-5s with cloud AI
- ✅ **Free Forever** – No per-check costs
- ✅ **Auditable** – Open source, verify everything

True privacy for blockchain development.

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 CompliLedger Algorand SDK                   │
├─────────────────────────────────────────────────────────────┤
│  CLI Tool           Python API         CI Integration       │
│  compliledger       CompliLedgerClient GitHub Actions       │
│  check/anchor       ComplianceChecker  GitLab CI            │
│  verify/report      mint_proof()       Pre-commit hooks     │
├─────────────────────────────────────────────────────────────┤
│              Proof Anchoring Engine                         │
│  Event Creator → Hasher → Algorand Txn → Verifier          │
├─────────────────────────────────────────────────────────────┤
│           Smart Contract Analysis Engine                    │
│  PyTeal/TEAL Parser → AST → Pattern Matcher → Scorer       │
├─────────────────────────────────────────────────────────────┤
│                  Policy Engine                              │
│  Rules | Severity | Evidence | Control Mapping             │
├─────────────────────────────────────────────────────────────┤
│                 Algorand Integration                        │
│  Algod Client | Transaction Builder | Explorer Links       │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
compliledger-algorand/
├── cli/                      # Command-line interface
├── client/                   # Proof anchoring client
│   ├── algorand.py          # Algorand integration
│   ├── events.py            # Event creation
│   └── verification.py      # Proof verification
├── analyzer/                # Smart contract analysis
│   ├── parser.py            # PyTeal/TEAL parser
│   ├── checker.py           # Pattern matcher
│   ├── scorer.py            # Severity scoring
│   └── reporter.py          # Report generation
├── policies/                # Compliance rules
│   ├── algorand_baseline.json
│   ├── pci_dss_algorand.json
│   ├── soc2_algorand.json
│   └── fedramp_algorand.json
├── integrations/            # CI/CD plugins
│   ├── github/
│   └── gitlab/
└── tests/                   # Test suite
```

---

## 💰 Pricing

| Tier | Checks/Month | Proofs/Month | Price | Features |
|------|--------------|--------------|-------|----------|
| **Freemium** | 100 | 100 | **Free** | Core policies, CLI |
| **Pro** | 1,000 | 1,000 | **$99/mo** | All policies, API access |
| **Enterprise** | Unlimited | Unlimited | **$999/mo** | Custom rules, SLA, support |

*Algorand transaction fees (≈0.001 ALGO per proof) paid separately*

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Areas we need help:**
- Additional policy packs (ISO 27001, HIPAA, GDPR)
- Advanced PyTeal patterns
- Performance optimizations
- Documentation improvements
- Testing coverage

---

## 📄 License

**MIT License** for core SDK (open-source)  
**Proprietary** for enterprise features

See [LICENSE](LICENSE) for details.

---

## 🌟 About CompliLedger

CompliLedger is building the **Proof-of-Compliance layer for Web3** — combining AI agents, blockchain attestations, and smart contract security.

**Algorand is our primary trust anchor.**

- 🌐 [Website](https://compliledger.com)
- 📧 [Email](mailto:hello@compliledger.com)
- 🐦 [Twitter](https://twitter.com/compliledger)
- 💬 [Discord](https://discord.gg/compliledger)

---

## 📚 Additional Resources

- [Full Documentation](https://docs.compliledger.com/algorand)
- [API Reference](https://docs.compliledger.com/algorand/api)
- [Security Best Practices](https://docs.compliledger.com/algorand/security)
- [PCI-DSS Guide](https://docs.compliledger.com/algorand/pci-dss)
- [Example Contracts](https://github.com/compliledger/algorand-examples)

---

**Built for the Algorand ecosystem** 🔷

*If you're building on Algorand and care about compliance, we'd love your help.*
