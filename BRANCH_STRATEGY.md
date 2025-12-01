# CompALGO Branch Strategy

**Branch Management for Internal Development vs Public PyPI Releases**

---

## 📋 Overview

CompALGO uses a **two-branch strategy** to separate internal development documentation from public-facing documentation on PyPI.

| Branch | Purpose | Documentation | PyPI Publishing |
|--------|---------|---------------|-----------------|
| **`main`** | Development & Internal | ALL docs (dev plans, test reports, etc.) | ❌ Never |
| **`publish`** | Public Releases | User-facing docs only | ✅ Always |

---

## 🌿 Branch Descriptions

### `main` Branch
**Purpose:** Internal development, complete documentation

**Contains:**
- ✅ All source code
- ✅ User-facing documentation
- ✅ Internal dev plans
- ✅ Testing reports
- ✅ Manager summaries
- ✅ Implementation details
- ✅ CI/CD documentation
- ✅ All markdown files

**Who uses it:** Developers, QA, internal team

**PyPI Publishing:** ❌ **NEVER publish from main**

---

### `publish` Branch
**Purpose:** Clean public releases for PyPI

**Contains:**
- ✅ All source code (same as main)
- ✅ User-facing documentation ONLY:
  - `README.md`
  - `QUICKSTART.md`
  - `CLI_USER_FLOWS.md`
  - `SECURITY_RULES.md`
  - `POLICY_GUIDE.md`
- ✅ LICENSE
- ✅ pyproject.toml

**Excluded (internal docs):**
- ❌ DEV_10_DAY_PLAN.md
- ❌ TESTING_REPORT.md
- ❌ MANAGER_SUMMARY.md
- ❌ P0_P1_COMPLETE.md
- ❌ CI_STATUS.md
- ❌ TESTNET_SETUP.md (too detailed)
- ❌ All other internal docs

**Who sees it:** PyPI users, public

**PyPI Publishing:** ✅ **ALWAYS publish from publish branch**

---

## 🔄 Workflow

### For Regular Development

```powershell
# Work on main branch
git checkout main
git pull origin main

# Make changes to code
# Update docs (both internal and user-facing)

# Commit and push
git add .
git commit -m "Your changes"
git push origin main
```

---

### For PyPI Publishing

**Step 1: Update main branch**
```powershell
# Ensure main is up to date
git checkout main
git pull origin main

# Update version in pyproject.toml
# Make any final changes
git add .
git commit -m "Prepare for release vX.X.X"
git push origin main
```

**Step 2: Merge to publish branch (code changes only)**
```powershell
# Switch to publish branch
git checkout publish
git pull origin publish

# Merge code changes from main
# This will try to merge everything, but we'll handle conflicts
git merge main

# If there are doc conflicts, keep publish branch versions
# (publish branch has fewer docs, that's intentional)

# OR better: Cherry-pick specific commits
git cherry-pick <commit-hash>  # Only code changes

# OR manually copy changed source files
# Keep publish branch docs as-is
```

**Step 3: Clean check (ensure no dev docs)**
```powershell
# Verify only user docs are present
Get-ChildItem -Filter *.md

# Should only see:
# - README.md
# - QUICKSTART.md
# - CLI_USER_FLOWS.md
# - SECURITY_RULES.md
# - POLICY_GUIDE.md
```

**Step 4: Build and publish**
```powershell
# Clean previous builds
if (Test-Path dist) { Remove-Item -Recurse -Force dist }

# Build package
python -m build

# Verify package contents
tar -tzf dist/compalgo-X.X.X.tar.gz | Select-String -Pattern "\.md$"

# Check for dev docs - should see NONE:
# ❌ No DEV_10_DAY_PLAN.md
# ❌ No TESTING_REPORT.md
# ❌ No MANAGER_SUMMARY.md
# etc.

# Upload to PyPI
twine check dist/*
twine upload dist/*
```

**Step 5: Tag and push**
```powershell
# Tag the release
git tag v0.1.1
git push origin publish
git push origin --tags

# Switch back to main for continued development
git checkout main
```

---

## 🔐 Security: What NOT to Include in Publish Branch

**Internal Documentation (REMOVE from publish):**
- `TESTING_REPORT.md`
- `MANAGER_SUMMARY.md`
- `P0_P1_COMPLETE.md`
- `CI_STATUS.md`
- `PYPI_PUBLISHING_GUIDE.md`
- `IMPLEMENTATION_SUMMARY.md`
- `DEV_10_DAY_PLAN.md`
- `TESTNET_SETUP.md`
- `YOU_ARE_HERE.md`
- `REPORTS_README.md`
- Any `P0_*.md` files
- Any `*_SUMMARY.md` files
- Any `*_COMPLETE.md` files

**User Documentation (KEEP in publish):**
- `README.md` (main package docs)
- `QUICKSTART.md` (getting started)
- `CLI_USER_FLOWS.md` (usage examples)
- `SECURITY_RULES.md` (security reference)
- `POLICY_GUIDE.md` (policy reference)
- `LICENSE` (required)
- `.github/workflows/README.md` (CI docs for contributors)
- `tests/README.md` (test docs for contributors)

---

## 📊 Current Status

**Branches:**
- ✅ `main` - Full development branch with all docs
- ✅ `publish` - Clean release branch (17 dev docs removed)

**Version:**
- Current: `0.1.1`
- Published from: `publish` branch

**Last Clean-up:**
- Date: December 2, 2025
- Files removed: 17 internal docs
- Files kept: 5 user-facing docs

---

## 🎯 Quick Reference

**When to use main:**
- Daily development
- Testing
- Internal documentation
- Code reviews

**When to use publish:**
- PyPI releases ONLY
- Public-facing documentation updates
- Version tagging

**Golden Rule:**
> 🚨 **NEVER publish to PyPI from `main` branch!**
> Always use `publish` branch for releases.

---

## 🔄 Version Update Checklist

Before publishing a new version:

**On main branch:**
- [ ] Update version in `pyproject.toml`
- [ ] Update CHANGELOG (if exists)
- [ ] Update internal docs
- [ ] Run tests
- [ ] Commit and push to main

**On publish branch:**
- [ ] Cherry-pick version update commit
- [ ] Verify no dev docs present
- [ ] Build package
- [ ] Verify package contents (no dev docs in tarball)
- [ ] Upload to PyPI
- [ ] Tag release
- [ ] Push tag

**After publishing:**
- [ ] Verify package on PyPI
- [ ] Test `pip install compalgo`
- [ ] Switch back to main for development

---

## 📝 Notes

**Why this strategy?**
- Keeps internal development docs private
- Shows only polished, user-facing docs on PyPI
- Maintains professional image
- Protects internal processes and planning

**How often to sync?**
- `main`: Continuous development (daily commits)
- `publish`: Only on releases (when publishing to PyPI)

**What if I accidentally publish from main?**
1. You can't unpublish from PyPI
2. Bump version immediately
3. Publish clean version from `publish` branch
4. Mark old version as yanked on PyPI (optional)

---

**Maintained by:** CompliLedger Team  
**Last Updated:** December 2, 2025
