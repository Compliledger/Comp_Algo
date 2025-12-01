# CompliLedger Algorand P0 Security Rules

This document describes the P0 baseline security and compliance rules implemented in the CompliLedger Algorand SDK v1.

## Rule Categories

### 1. Application Control
Rules that enforce proper authorization and access control for critical application lifecycle operations.

### 2. Account Control
Rules that prevent unauthorized account manipulation (rekey, close).

### 3. Fee Abuse
Rules that detect potentially dangerous fee handling patterns.

### 4. Asset Safety
Rules that protect asset transfers and asset management operations.

### 5. Logic Patterns
Rules that identify risky logic patterns or missing validations.

---

## P0 Rules Reference

### DELETE_WITHOUT_ADMIN_CHECK
- **Category**: Application Control
- **Severity**: CRITICAL
- **Control Mapping**: SOC2:CC6.1, PCI-DSS:6.5.10
- **Description**: Detects `DeleteApplication` without sender/admin validation
- **Detection (PyTeal)**: 
  - `OnComplete.DeleteApplication` branch exists
  - No `Txn.sender()` check in same block
- **Detection (TEAL)**:
  - `OnCompletion` == `DeleteApplication` (int DeleteApplication)
  - Missing `txn Sender` validation before `return 1`

### UPDATE_WITHOUT_ADMIN_CHECK
- **Category**: Application Control
- **Severity**: CRITICAL
- **Control Mapping**: SOC2:CC6.1, PCI-DSS:6.5.10
- **Description**: Detects `UpdateApplication` without sender/admin validation
- **Detection (PyTeal)**:
  - `OnComplete.UpdateApplication` branch exists
  - No `Txn.sender()` check
- **Detection (TEAL)**:
  - `OnCompletion` == `UpdateApplication`
  - Missing `txn Sender` validation

### MISSING_ADMIN_SENDER_CHECK
- **Category**: Application Control
- **Severity**: HIGH
- **Control Mapping**: SOC2:CC6.1
- **Description**: General missing admin/sender validation in critical paths
- **Detection (PyTeal)**:
  - Critical operations (globalPut, globalDel, InnerTxn) without `Txn.sender()` check
- **Detection (TEAL)**:
  - `app_global_put`, `app_global_del`, or `itxn_submit` without `txn Sender` validation

### REKEY_NOT_ZERO
- **Category**: Account Control
- **Severity**: CRITICAL
- **Control Mapping**: SOC2:CC6.6, PCI-DSS:6.5.10
- **Description**: Missing validation that `RekeyTo` is zero address
- **Detection (PyTeal)**:
  - No `Txn.rekey_to() == Global.zero_address()` check
- **Detection (TEAL)**:
  - No `txn RekeyTo` with `global ZeroAddress` comparison

### CLOSEREMAINDER_NOT_ZERO
- **Category**: Account Control
- **Severity**: CRITICAL
- **Control Mapping**: SOC2:CC6.6, PCI-DSS:6.5.10
- **Description**: Missing validation that `CloseRemainderTo` is zero address
- **Detection (PyTeal)**:
  - No `Txn.close_remainder_to() == Global.zero_address()` check
- **Detection (TEAL)**:
  - No `txn CloseRemainderTo` with `global ZeroAddress` comparison

### MISSING_ARG_VALIDATION
- **Category**: Logic Patterns
- **Severity**: HIGH
- **Control Mapping**: SOC2:CC7.2, PCI-DSS:6.5.1
- **Description**: Transaction arguments used without length/format validation
- **Detection (PyTeal)**:
  - `Txn.application_args[N]` used without `Txn.application_args.length()` check
- **Detection (TEAL)**:
  - `txn ApplicationArgs N` used without `txn NumAppArgs` validation

### STATE_MUTATION_UNGUARDED
- **Category**: Logic Patterns
- **Severity**: HIGH
- **Control Mapping**: SOC2:CC6.1, PCI-DSS:6.5.8
- **Description**: Global/local state mutations without authorization checks
- **Detection (PyTeal)**:
  - `App.globalPut` or `App.localPut` without preceding `Txn.sender()` or `Assert`
- **Detection (TEAL)**:
  - `app_global_put` or `app_local_put` without prior `txn Sender` check

### INNER_TXN_UNGUARDED
- **Category**: Logic Patterns
- **Severity**: HIGH
- **Control Mapping**: SOC2:CC6.1, PCI-DSS:6.5.1
- **Description**: Inner transactions submitted without proper validation
- **Detection (PyTeal)**:
  - `InnerTxnBuilder.Submit()` without authorization checks
- **Detection (TEAL)**:
  - `itxn_submit` without preceding validation logic

### EXCESSIVE_FEE_UNBOUNDED
- **Category**: Fee Abuse
- **Severity**: MEDIUM
- **Control Mapping**: SOC2:CC7.2, PCI-DSS:6.5.1
- **Description**: Transaction fee not bounded or validated
- **Detection (PyTeal)**:
  - `Txn.fee()` referenced but no upper bound check
- **Detection (TEAL)**:
  - `txn Fee` used without `<=` comparison to max value

---

## Compliance Score Calculation

The compliance score is computed as:

```
score = 100 - (critical_count * 20 + high_count * 10 + medium_count * 5 + low_count * 2)
score = max(0, min(100, score))
```

- **Critical**: -20 points each
- **High**: -10 points each
- **Medium**: -5 points each
- **Low**: -2 points each

A contract **passes** if its score meets or exceeds the threshold (default: 80).

---

## Compliance Verdict Object Schema

```json
{
  "framework": "SOC2",
  "control_id": "CC6.1",
  "status": "fail",
  "contract": "examples/vulnerable_escrow.py",
  "rules_triggered": ["DELETE_WITHOUT_ADMIN_CHECK", "REKEY_NOT_ZERO"],
  "severity": "critical",
  "timestamp": "2024-12-01T08:53:00Z",
  "metadata": {
    "policy": "algorand-baseline",
    "threshold": 80,
    "score": 60
  }
}
```

The verdict is serialized to canonical JSON, hashed with SHA-256, and anchored on Algorand as:
```
Note: CLG1|sha256:<hex_hash>
```

---

## Future Enhancements (v2+)

- **Asset transfer validation**: Ensure asset opt-in before transfers
- **Reentrancy detection**: Identify potential reentrancy patterns in stateful calls
- **Time-lock validation**: Verify proper use of `LatestTimestamp` and `FirstValid`/`LastValid`
- **ZK-proof integration**: Zero-knowledge proofs for private compliance attestations
- **Multi-sig enforcement**: Rules requiring multi-signature approvals for sensitive operations

---

## References

- [Algorand Developer Docs](https://developer.algorand.org/)
- [PyTeal Documentation](https://pyteal.readthedocs.io/)
- [TEAL Specification](https://developer.algorand.org/docs/get-details/dapps/avm/teal/)
- [SOC 2 Trust Services Criteria](https://www.aicpa.org/soc)
- [PCI-DSS Requirements](https://www.pcisecuritystandards.org/)
