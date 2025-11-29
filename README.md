# 🔒 CompliLedger SDK – Algorand Edition

**Proof-of-Compliance & Smart Contract Security for Algorand**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Algorand](https://img.shields.io/badge/Algorand-Ready-00D4AA.svg)](https://algorand.com)

**SOC 2** • **PCI DSS** • **FedRAMP** • **Smart Contract Security**

---

## 🎯 Dual-Purpose Compliance SDK

CompliLedger for Algorand provides **two powerful capabilities**:

### 1. 🔐 Compliance Proof Anchoring
Create cryptographically verifiable attestations anchored immutably on Algorand blockchain.

### 2. 🛡️ Smart Contract Security Analysis
Analyze PyTeal and TEAL contracts for vulnerabilities and compliance issues during development.

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
pip install compliledger-algorand

# With interactive menu mode
pip install compliledger-algorand[interactive]

# With file watching (auto-check on save)
pip install compliledger-algorand[watch]

# Full install
pip install compliledger-algorand[all]
```

---

## 🎬 Quickstart

### Part 1: Anchor Compliance Proofs

```python
from compliledger_algorand import CompliLedgerClient

client = CompliLedgerClient(
    algod_url="https://testnet-api.algonode.cloud",
    algod_token="",
    sender_mnemonic="your 25-word mnemonic",
    network="testnet"
)

# Create compliance event
event = client.create_compliance_event(
    framework="SOC2",
    control_id="CC6.1",
    status="pass",
    resource="auth-service",
    details={"checked_by": "ci-pipeline"}
)

# Mint proof on Algorand
proof = client.mint_proof(event)

print(f"✅ Proof anchored!")
print(f"📍 TXID: {proof.txid}")
print(f"🔗 Explorer: {proof.explorer_url}")
print(f"🔐 Hash: {proof.event_hash}")

# Verify proof
assert client.verify_proof(event, proof.txid)
```

### Part 2: Analyze Smart Contract Security

```bash
# Interactive mode (recommended)
compliledger analyze --interactive

# Quick check
compliledger check contracts/payment.py

# Check directory with threshold
compliledger check contracts/ --threshold 80 --fail-on-critical

# Generate HTML report
compliledger report contracts/ --format html -o report.html
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

## 💻 CLI Commands

### Proof Anchoring

```bash
# Anchor compliance event
compliledger anchor --framework SOC2 --control CC6.1 --status pass

# Verify proof
compliledger verify --txid <TRANSACTION_ID>

# Query proofs
compliledger query --framework SOC2 --from-date 2025-01-01

# Export history
compliledger export --format csv -o compliance_history.csv
```

### Smart Contract Analysis

```bash
# Interactive menu
compliledger analyze --interactive

# Check file/directory
compliledger check contracts/payment.py
compliledger check contracts/ --fail-on-high

# Generate reports
compliledger report contracts/ --format html -o report.html
compliledger report contracts/ --format markdown -o SECURITY.md

# CI/CD integration
compliledger init-ci

# Watch mode
compliledger watch contracts/

# List policies
compliledger list-policies
```

---

## 🎨 Interactive Mode

```bash
compliledger analyze --interactive
```

**Features:**
- 🔍 Auto-scans for PyTeal (.py) and TEAL (.teal) files
- 📋 Quick access to recent files
- ⌨️ Navigate with arrow keys
- 🔄 Rescan on demand
- 📊 Detailed violation reports
- 💾 Export to multiple formats

---

## 🔐 Framework Examples

### SOC 2 Compliance

```python
event = client.create_compliance_event(
    framework="SOC2",
    control_id="CC6.1",  # Logical Access Controls
    status="pass",
    resource="auth-service",
    details={"mfa_enabled": True}
)
proof = client.mint_proof(event)
```

### PCI DSS Payment Security

```python
# Anchor compliance event
event = client.create_compliance_event(
    framework="PCI",
    control_id="REQ_10",  # Track and Monitor Access
    status="pass",
    resource="payment-api"
)

# Check smart contract for PCI compliance
from compliledger_algorand.analyzer import ComplianceChecker

checker = ComplianceChecker(policy_pack="pci-dss-algorand")
result = checker.check_file("contracts/payment_app.py")

if result.score >= 85:
    proof = client.mint_proof(event)
```

### FedRAMP Cloud Security

```python
event = client.create_compliance_event(
    framework="FedRAMP",
    control_id="AC-2",  # Account Management
    status="pass",
    resource="cloud-console"
)
proof = client.mint_proof(event)
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
