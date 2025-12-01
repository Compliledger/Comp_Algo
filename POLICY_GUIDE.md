# CompALGO Policy Pack Guide

## Policy Pack Overview

CompALGO includes **9 policy packs** organized into three categories:

---

## 🎯 Algorand-Specific Policies (Recommended)

### 1. **algorand-baseline** ⭐ MOST POPULAR

**Purpose**: Core security rules specifically for Algorand PyTeal and TEAL smart contracts

| Attribute | Value |
|-----------|-------|
| **Rules** | 9 |
| **Threshold** | 80% |
| **Target** | All Algorand contracts |
| **Severity** | 4 CRITICAL, 4 HIGH, 1 MEDIUM |

**Detects:**
- ❌ DeleteApplication without admin check
- ❌ UpdateApplication without admin check  
- ❌ Missing rekey_to == zero_address assertion
- ❌ Missing close_remainder_to == zero_address assertion
- ❌ Unprotected state mutations
- ❌ Unvalidated application arguments
- ❌ Missing inner transaction guards
- ❌ Unbounded transaction fees

**Use When:**
- Building any Algorand smart contract
- General purpose PyTeal/TEAL development
- Starting a new project (baseline security)

**Example:**
```bash
compalgo check contract.py --policy algorand-baseline
```

---

### 2. **pci-dss-algorand**

**Purpose**: PCI-DSS compliance subset optimized for Algorand payment contracts

| Attribute | Value |
|-----------|-------|
| **Rules** | 3 |
| **Threshold** | 80% |
| **Target** | Payment/financial Algorand contracts |
| **Severity** | 2 HIGH, 1 MEDIUM |

**Detects:**
- ❌ Missing input validation (PCI REQ 6.5.1)
- ❌ Unsafe inner transactions
- ❌ Unbounded fees

**Use When:**
- Building payment protocols
- Processing financial transactions
- DeFi applications on Algorand

---

## 🔒 General Security Policy

### 3. **security-baseline** ⭐ RECOMMENDED

**Purpose**: Blockchain-agnostic security patterns based on NIST, ISO-27001, OWASP

| Attribute | Value |
|-----------|-------|
| **Rules** | 10 |
| **Threshold** | 75% |
| **Target** | Any smart contract platform |
| **Severity** | 3 CRITICAL, 4 HIGH, 3 MEDIUM |

**Detects:**
- ❌ Missing input validation
- ❌ Unprotected state mutations
- ❌ Insufficient logging
- ❌ Access control issues
- ❌ Integer overflow risks
- ❌ Forbidden data storage
- ❌ Weak cryptography
- ❌ Reentrancy vulnerabilities

**Use When:**
- Cross-platform security review
- Following NIST/ISO standards
- General best practices audit
- Comparative analysis with other chains

**Example:**
```bash
compalgo check contract.py --policy security-baseline
```

---

## 💳 PCI-DSS Compliance Policies

### 4. **pci-dss-basic**

**Purpose**: Essential PCI-DSS v4.0 requirements for payment applications

| Attribute | Value |
|-----------|-------|
| **Rules** | 7 |
| **Threshold** | 85% |
| **Target** | Payment apps, DeFi, token swaps |
| **Coverage** | ~40% of PCI-DSS |

**Use When:**
- Payment processing
- Cryptocurrency exchanges
- DeFi lending/borrowing
- Quick PCI compliance check

---

### 5. **pci-dss-standard**

**Purpose**: Comprehensive PCI-DSS v4.0 compliance for production payment systems

| Attribute | Value |
|-----------|-------|
| **Rules** | 15 |
| **Threshold** | 90% |
| **Target** | Production payment applications |
| **Coverage** | ~75% of PCI-DSS |

**Use When:**
- Production payment systems
- Enterprise financial applications
- Full PCI-DSS compliance required
- Preparing for PCI audit

**Example:**
```bash
compalgo check payment_contract.py --policy pci-dss-standard --threshold 90
```

---

### 6. **pci-secure-software**

**Purpose**: PCI Secure Software Standard v1.2.1 for software vendors

| Attribute | Value |
|-----------|-------|
| **Rules** | 7 |
| **Threshold** | 90% |
| **Target** | Software vendors, solution providers |
| **Covers** | REQ-1.x through REQ-10.x |

**Use When:**
- Building payment software products
- Vendor certification required
- Software-as-a-Service payment platforms

---

### 7. **pci-tokenization**

**Purpose**: PCI Tokenization and Token Service Provider (TSP) requirements

| Attribute | Value |
|-----------|-------|
| **Rules** | 4 |
| **Threshold** | 90% |
| **Target** | Token service providers, tokenized assets |

**Use When:**
- Building tokenization services
- Payment token handling
- DeFi tokenized asset platforms

---

## 📚 Reference Policies

### 8. **aleo-baseline**

**Purpose**: Security patterns from Aleo/Leo blockchain (cross-chain reference)

| Attribute | Value |
|-----------|-------|
| **Rules** | 10 |
| **Threshold** | 75% |
| **Target** | Cross-chain comparison |

**Use When:**
- Comparing Algorand vs Aleo security
- Research and benchmarking
- Learning from other blockchain best practices

---

### 9. **controls_catalog**

**Purpose**: Reference catalog of all security controls across frameworks

**Use When:**
- Looking up control definitions
- Understanding control mappings
- Compliance documentation

---

## 🎯 Policy Selection Guide

### By Use Case

| Use Case | Recommended Policy | Why |
|----------|-------------------|-----|
| **General Algorand dApp** | `algorand-baseline` | Algorand-specific rules |
| **Payment Protocol** | `pci-dss-standard` | Comprehensive PCI compliance |
| **DeFi Application** | `pci-dss-basic` | Essential financial security |
| **Token Platform** | `pci-tokenization` | Tokenization-specific rules |
| **Software Product** | `pci-secure-software` | Vendor certification |
| **Security Research** | `security-baseline` | General best practices |
| **Pre-Audit Check** | `algorand-baseline` + `pci-dss-standard` | Multiple perspectives |

### By Project Stage

| Stage | Policy | Threshold |
|-------|--------|-----------|
| **Development** | `algorand-baseline` | 70-80% |
| **Testing** | `algorand-baseline` | 80-85% |
| **Pre-Production** | `pci-dss-standard` | 90%+ |
| **Production** | `pci-dss-standard` | 95%+ |

### By Risk Tolerance

| Risk Level | Policy | Approach |
|------------|--------|----------|
| **High Risk (payments)** | `pci-dss-standard` | Strictest rules |
| **Medium Risk (DeFi)** | `pci-dss-basic` | Balanced |
| **Low Risk (general)** | `algorand-baseline` | Essential only |

---

## 🔄 Multi-Policy Workflow

### Progressive Compliance

```bash
# Stage 1: Quick check (development)
compalgo check contract.py --policy algorand-baseline --threshold 75

# Stage 2: Security baseline (testing)
compalgo check contract.py --policy security-baseline --threshold 80

# Stage 3: PCI compliance (pre-production)
compalgo check contract.py --policy pci-dss-standard --threshold 90
```

### Comparative Analysis

```bash
# Compare across multiple policies
for policy in algorand-baseline security-baseline pci-dss-standard; do
    echo "Testing with $policy:"
    compalgo check contract.py --policy $policy
done
```

---

## 📊 Policy Comparison Matrix

| Policy | Algorand-Specific | PCI-DSS | SOC2 | NIST | Threshold | Best For |
|--------|-------------------|---------|------|------|-----------|----------|
| **algorand-baseline** | ✅ | ✅ | ✅ | ❌ | 80% | All Algorand projects |
| **security-baseline** | ❌ | ❌ | ✅ | ✅ | 75% | General security |
| **pci-dss-algorand** | ✅ | ✅ | ❌ | ❌ | 80% | Algorand payments |
| **pci-dss-basic** | ❌ | ✅ | ❌ | ❌ | 85% | Quick PCI check |
| **pci-dss-standard** | ❌ | ✅ | ❌ | ❌ | 90% | Full PCI compliance |
| **pci-secure-software** | ❌ | ✅ | ❌ | ❌ | 90% | Software vendors |
| **pci-tokenization** | ❌ | ✅ | ❌ | ❌ | 90% | Token platforms |

---

## 💡 Best Practices

### ✅ DO

- Start with `algorand-baseline` for all Algorand projects
- Use `pci-dss-standard` for production payment systems
- Run multiple policies for comprehensive coverage
- Increase threshold as project matures (70% → 80% → 90%)
- Generate verdicts for audit trails

### ❌ DON'T

- Use `aleo-baseline` as primary for Algorand (use `algorand-baseline` or `security-baseline`)
- Skip baseline checks before production
- Use low thresholds (<70%) for payment contracts
- Ignore CRITICAL severity violations
- Deploy without any compliance check

---

## 🚀 Quick Start Commands

```bash
# Check with recommended policy
compalgo check contract.py --policy algorand-baseline

# List all available policies
compalgo list-policies

# Payment contract with strict compliance
compalgo check payment.py --policy pci-dss-standard --threshold 90

# Generate compliance verdict
compalgo check contract.py --verdict-out verdict.json --policy algorand-baseline

# Compare multiple policies
compalgo check contract.py --policy security-baseline
compalgo check contract.py --policy algorand-baseline
compalgo check contract.py --policy pci-dss-standard
```

---

## 📖 Additional Resources

- **[CLI_USER_FLOWS.md](CLI_USER_FLOWS.md)** - Complete workflow examples
- **[SECURITY_RULES.md](SECURITY_RULES.md)** - Detailed rule documentation
- **[README.md](README.md)** - Main documentation
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute getting started

---

**Choose the right policy for your use case and build secure Algorand smart contracts!** 🔒
