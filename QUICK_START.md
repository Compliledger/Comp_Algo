# CompALGO Quick Start - .env Configuration

**3-step setup for Windows PowerShell + TestNet**

---

## ⚡ Quick Commands

### 1️⃣ Install Dependencies
```powershell
pip install -e .
```

### 2️⃣ Create .env File
```powershell
copy .env.example .env
notepad .env
```

**Edit .env** - Replace with your 25-word Pera TestNet mnemonic:
```bash
ALGO_MNEMONIC=word1 word2 word3 ... word25
```

### 3️⃣ Run End-to-End Demo
```powershell
python examples/anchor_and_verify.py
```

**That's it!** ✅

---

## 📋 What You'll See

The script will:
1. ✅ Scan `examples/vulnerable_escrow.py` for violations
2. ✅ Build a Compliance Verdict (SOC2:CC6.1)
3. ✅ Anchor the verdict hash on Algorand TestNet
4. ✅ Print TXID + AlgoExplorer URL
5. ✅ Verify the proof back from the chain

**Output includes:**
- Transaction ID (TXID)
- AlgoExplorer URL (click to view on-chain)
- Verdict file: `examples/output/verdict_demo.json`
- Cost: ~0.001 ALGO

---

## 🎯 CLI Usage

```powershell
# Create verdict
compalgo check examples/vulnerable_escrow.py --verdict-out verdict.json

# Anchor (uses .env automatically)
compalgo anchor --verdict verdict.json

# Verify (no mnemonic needed)
compalgo verify --verdict verdict.json --txid YOUR_TXID_HERE
```

---

## 🔧 Prerequisites

- ✅ Python 3.10+
- ✅ Pera Wallet with TestNet account
- ✅ Test ALGO: https://bank.testnet.algorand.network/

---

## 🔐 Security

- ✅ `.env` is gitignored (never committed)
- ✅ Your mnemonic stays local
- ✅ No system environment variables needed

---

## 📖 Full Documentation

See **TESTNET_SETUP.md** for detailed instructions and troubleshooting.

---

**Ready? Run this:**
```powershell
python examples/anchor_and_verify.py
```
