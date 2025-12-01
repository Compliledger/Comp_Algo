# CompALGO TestNet Setup Guide (Windows/PowerShell)

**Complete setup guide for running CompALGO with .env configuration on Windows**

---

## 📋 Prerequisites

- ✅ Windows 10/11 with PowerShell
- ✅ Python 3.10+ installed
- ✅ Pera Wallet TestNet account with test ALGO
- ✅ Git (for cloning the repo)

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies

Open PowerShell in the project directory and run:

```powershell
# Install the package in development mode
pip install -e .

# This installs all dependencies including python-dotenv
```

**Expected output:**
```
Successfully installed compalgo-0.1.0 py-algorand-sdk-2.6.0 python-dotenv-1.0.0 ...
```

---

### Step 2: Create Your .env File

Copy the example file and edit it with your credentials:

```powershell
# Copy the example file
copy .env.example .env

# Open in your default text editor
notepad .env
```

**Edit the .env file** and replace the placeholder with your actual 25-word mnemonic:

```bash
# Before:
ALGO_MNEMONIC=your 25 word mnemonic phrase here

# After (example - use YOUR mnemonic):
ALGO_MNEMONIC=word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 word12 word13 word14 word15 word16 word17 word18 word19 word20 word21 word22 word23 word24 word25
```

**Keep the other settings as-is for TestNet:**
```bash
ALGO_NETWORK=testnet
ALGOD_URL=https://testnet-api.algonode.cloud
INDEXER_URL=https://testnet-idx.algonode.cloud
```

**⚠️ SECURITY NOTES:**
- ✅ `.env` is already in `.gitignore` - it will NOT be committed to git
- ✅ Your mnemonic NEVER leaves your local machine
- ✅ Transactions are signed locally before being sent
- ❌ NEVER share your .env file or commit it to version control

---

### Step 3: Get TestNet ALGO

Your Pera wallet needs a small amount of TestNet ALGO (~0.1 ALGO minimum).

**Get free TestNet ALGO:**

1. Open your Pera Wallet app
2. Copy your TestNet wallet address
3. Visit: https://bank.testnet.algorand.network/
4. Paste your address and request ALGO
5. Wait ~5 seconds for confirmation

**Verify you have ALGO:**
- Open Pera Wallet → Select TestNet → Check balance shows > 0 ALGO

---

### Step 4: Run the End-to-End Demo

Now run the complete anchor and verify flow:

```powershell
# Run the demo script
python examples/anchor_and_verify.py
```

**Expected output:**

```
================================================================================
  CompALGO - Algorand Compliance Proof Anchoring Demo
================================================================================
P0 Flow: Scan → Verdict → Anchor → Verify

[Step 0] Loading configuration from .env file
--------------------------------------------------------------------------------
✅ Config loaded: AlgoConfig(network=testnet, algod_url=https://testnet-api.algonode.cloud, ...)

[Step 1] Scanning vulnerable smart contract
--------------------------------------------------------------------------------
📄 Contract: examples/vulnerable_escrow.py
📊 Score: 20/100
✅ Passed: No
⚠️  Violations: 7

Detected Violations:
  1. [CRITICAL] DELETE_WITHOUT_ADMIN_CHECK: DeleteApplication not restricted
  2. [HIGH] REKEY_NOT_ZERO: RekeyTo field not validated
  ...

[Step 2] Building Compliance Verdict
--------------------------------------------------------------------------------
🏛️  Framework: SOC2:CC6.1
📋 Status: FAIL
⚠️  Severity: CRITICAL
📜 Rules Triggered: DELETE_WITHOUT_ADMIN_CHECK, REKEY_NOT_ZERO, ...

🔐 Verdict Hash (SHA-256):
   a7f3c9e8b2d1f4a5e6c7d8b9f0a1c2e3d4b5a6c7d8e9f0a1b2c3d4e5f6a7b8c9

💾 Verdict saved to: examples/output/verdict_demo.json

[Step 3] Anchoring verdict hash on Algorand TestNet
--------------------------------------------------------------------------------
🌐 Network: TESTNET
🔗 Algod URL: https://testnet-api.algonode.cloud
📍 Indexer URL: https://testnet-idx.algonode.cloud

⏳ Sending transaction to Algorand... (this may take 3-5 seconds)

✅ Anchored successfully!
📝 Transaction ID: CTOE5M6ZZD3XAMPLE1234567890
🔍 Explorer URL:
   https://testnet.algoexplorer.io/tx/CTOE5M6ZZD3XAMPLE1234567890

💡 Your proof is now permanently on the Algorand blockchain!
   Cost: ~0.001 ALGO

[Step 4] Verifying verdict against blockchain
--------------------------------------------------------------------------------
🔎 Fetching transaction from Algorand...
   TXID: CTOE5M6ZZD3XAMPLE1234567890

✅ VERIFICATION SUCCESSFUL!
   The on-chain hash matches the verdict hash.
   This verdict is cryptographically proven on Algorand.

================================================================================
  Demo Complete! 🎉
================================================================================

📊 Summary:
   Contract: examples/vulnerable_escrow.py
   Score: 20/100
   Status: FAIL
   Violations: 7
   Verdict Hash: a7f3c9e8b2d1f4a5e6c7d8b9f0a1...
   TXID: CTOE5M6ZZD3XAMPLE1234567890

🔗 Blockchain Proof:
   https://testnet.algoexplorer.io/tx/CTOE5M6ZZD3XAMPLE1234567890

💾 Verdict File:
   examples/output/verdict_demo.json

================================================================================
Your compliance proof is now permanently anchored on Algorand! 🚀
================================================================================

📖 Next Steps:
   1. View your transaction on AlgoExplorer (link above)
   2. Verify anytime with:
      compalgo verify --verdict examples/output/verdict_demo.json --txid CTOE5M6ZZD3XAMPLE1234567890
   3. Share the TXID and verdict file for audit verification
```

---

## 🎯 Single Command Summary

**Once .env is configured, just run:**

```powershell
python examples/anchor_and_verify.py
```

This single command:
- ✅ Scans `examples/vulnerable_escrow.py`
- ✅ Builds a Compliance Verdict
- ✅ Anchors the verdict hash on Algorand TestNet
- ✅ Prints the TXID and AlgoExplorer URL
- ✅ Verifies the proof back from the chain

---

## 🔧 Troubleshooting

### Error: "ALGO_MNEMONIC is required but not set"

**Solution:**
1. Make sure you created `.env` file (copy from `.env.example`)
2. Edit `.env` and set your 25-word mnemonic
3. Verify `.env` is in the project root directory

### Error: "insufficient balance"

**Solution:**
- Get more TestNet ALGO from: https://bank.testnet.algorand.network/
- You need at least 0.001 ALGO per transaction

### Error: "ModuleNotFoundError: No module named 'dotenv'"

**Solution:**
```powershell
pip install python-dotenv
# Or reinstall the package:
pip install -e .
```

### Error: "File not found: examples/vulnerable_escrow.py"

**Solution:**
- Make sure you're running the command from the project root directory
- Check that the file exists: `ls examples/vulnerable_escrow.py`

---

## 📖 Using the CLI

The CLI also supports .env configuration:

### Anchor a Verdict

```powershell
# Create a verdict
compalgo check examples/vulnerable_escrow.py --verdict-out verdict.json

# Anchor it (uses .env config automatically)
compalgo anchor --verdict verdict.json

# Output:
# ✅ Anchored! TXID: CTOE5M6ZZD...
# Explorer: https://testnet.algoexplorer.io/tx/CTOE5M6ZZD...
```

### Verify a Verdict

```powershell
# Verify (uses .env config, no mnemonic needed)
compalgo verify --verdict verdict.json --txid CTOE5M6ZZD...

# Output:
# ✅ VALID
```

### Override .env with CLI Options

```powershell
# Use MainNet instead of .env setting
compalgo anchor --verdict verdict.json --network mainnet

# Use different Algod URL
compalgo anchor --verdict verdict.json --algod-url https://mainnet-api.algonode.cloud
```

---

## 🔐 Security Best Practices

### ✅ DO:
- ✅ Keep your `.env` file in the project root (it's gitignored)
- ✅ Use TestNet for testing (free ALGO, no risk)
- ✅ Verify `.env` is NOT committed: `git status` should not show it
- ✅ Each developer can have their own `.env` with their own wallet

### ❌ DON'T:
- ❌ NEVER commit `.env` to version control
- ❌ NEVER share your `.env` file
- ❌ NEVER hardcode mnemonics in Python scripts
- ❌ NEVER set system-level environment variables (use .env instead)

---

## 🌐 Switching to MainNet

When ready for production:

1. **Edit .env:**
```bash
ALGO_NETWORK=mainnet
ALGOD_URL=https://mainnet-api.algonode.cloud
INDEXER_URL=https://mainnet-idx.algonode.cloud
```

2. **Update mnemonic to MainNet wallet:**
```bash
ALGO_MNEMONIC=your mainnet wallet 25 word mnemonic here
```

3. **Run the same commands:**
```powershell
python examples/anchor_and_verify.py
```

**MainNet Notes:**
- ⚠️ Costs real ALGO (~0.001 ALGO per anchor)
- ⚠️ Transactions are PERMANENT and irreversible
- ⚠️ Use a dedicated compliance wallet, not your main wallet

---

## 📚 Additional Resources

- **AlgoExplorer TestNet:** https://testnet.algoexplorer.io/
- **AlgoExplorer MainNet:** https://algoexplorer.io/
- **Algorand Faucet (TestNet):** https://bank.testnet.algorand.network/
- **Pera Wallet:** https://perawallet.app/
- **CompALGO Documentation:** See `README.md`, `CLI_USER_FLOWS.md`

---

## 💡 What's Happening Under the Hood?

1. **Scan:** Analyzes PyTeal/TEAL code for violations using P0 rules
2. **Verdict:** Creates a structured JSON object with results
3. **Hash:** Computes deterministic SHA-256 hash of the verdict
4. **Anchor:** Sends a 0-ALGO payment transaction to yourself with note: `CLG1|sha256:<hash>`
5. **Verify:** Fetches the transaction, decodes the note, compares hashes

**Result:** Cryptographic proof that a specific contract was analyzed with a specific result at a specific time.

---

## ✅ Success Checklist

After running the demo, you should have:

- ✅ `.env` file with your mnemonic (not committed to git)
- ✅ `examples/output/verdict_demo.json` - the verdict file
- ✅ A transaction ID (TXID) printed to console
- ✅ An AlgoExplorer URL showing your transaction
- ✅ "VERIFICATION SUCCESSFUL" message
- ✅ ~0.001 ALGO deducted from your TestNet wallet

---

**🎉 You're all set! CompALGO is now configured and ready to use.**

For questions or issues, see `README.md` or file an issue on GitHub.
