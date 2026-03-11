#!/usr/bin/env bash
# ==============================================================================
# Phase 114 – Autonomous Compliance Certification: Git Push Script
# ==============================================================================
# Commits all Phase 114 changes (code + documentation) and pushes to GitHub.
#
# Usage:
#   bash push_phase114.sh
#
# Prerequisites:
#   - Git installed and on PATH
#   - Remote 'origin' pointing to github.com/ckr-rai73/guardrail-ai
#   - SSH key or credential helper configured for push access
# ==============================================================================

set -euo pipefail

COMMIT_MSG="Phase 114 complete – Autonomous Compliance Certification + doc updates"
REMOTE="origin"
BRANCH="main"

# ---------- 1. Verify we are inside a Git repository --------------------------
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
  echo "❌  ERROR: Not inside a Git repository. Run this script from the repo root."
  exit 1
fi

echo "✅  Inside Git repository: $(git rev-parse --show-toplevel)"

# ---------- 2. Verify the remote is set correctly -----------------------------
REMOTE_URL=$(git remote get-url "$REMOTE" 2>/dev/null || true)
if [[ -z "$REMOTE_URL" ]]; then
  echo "❌  ERROR: Remote '$REMOTE' is not configured."
  echo "   Run: git remote add origin https://github.com/ckr-rai73/guardrail-ai.git"
  exit 1
fi

echo "✅  Remote '$REMOTE' → $REMOTE_URL"

# ---------- 3. Stage all Phase 114 files (new + modified) ---------------------
echo ""
echo "📂  Staging Phase 114 files..."

# Code modules
git add backend/app/compliance/control_mapper.py          2>/dev/null || true
git add backend/app/compliance/evidence_collector.py       2>/dev/null || true
git add backend/app/compliance/certificate_builder.py      2>/dev/null || true
git add backend/app/compliance/auditor_portal.py           2>/dev/null || true
git add backend/app/compliance/continuous_compliance_dashboard.py 2>/dev/null || true
git add backend/app/compliance/zk_prover.py                2>/dev/null || true
git add backend/app/compliance/__init__.py                 2>/dev/null || true

# Config update
git add backend/app/core/config.py                         2>/dev/null || true

# Adversarial test suite
git add backend/adversarial_test_phase114_compliance.py    2>/dev/null || true

# Framework definitions
git add backend/frameworks/iso42001.yaml                   2>/dev/null || true
git add backend/frameworks/soc2.yaml                       2>/dev/null || true
git add backend/frameworks/fedramp.yaml                    2>/dev/null || true
git add backend/frameworks/eu_ai_act.yaml                  2>/dev/null || true
git add backend/frameworks/nist_ai_rmf.yaml                2>/dev/null || true

# Documentation updates
git add MASTER_WALKTHROUGH.md                              2>/dev/null || true
git add architecture_review.md                             2>/dev/null || true
git add hard_roi_report.md                                 2>/dev/null || true
git add MASTER_MANIFEST_AUDIT.md                           2>/dev/null || true

# ---------- 4. Check if there are staged changes ------------------------------
if git diff --cached --quiet; then
  echo ""
  echo "ℹ️   No changes to commit — everything is already up to date."
  echo "   Latest commit: $(git log -1 --oneline)"
  exit 0
fi

echo ""
echo "📋  Staged files:"
git diff --cached --name-status

# ---------- 5. Commit with descriptive message --------------------------------
echo ""
echo "💾  Committing..."
git commit -m "$COMMIT_MSG"

# ---------- 6. Push to remote -------------------------------------------------
echo ""
echo "🚀  Pushing to $REMOTE/$BRANCH..."
git push "$REMOTE" "$BRANCH"

# ---------- 7. Confirmation ---------------------------------------------------
COMMIT_HASH=$(git rev-parse HEAD)
SHORT_HASH=$(git rev-parse --short HEAD)

echo ""
echo "══════════════════════════════════════════════════════════════"
echo "  ✅  Phase 114 pushed successfully!"
echo ""
echo "  Commit  : $SHORT_HASH ($COMMIT_HASH)"
echo "  Branch  : $BRANCH"
echo "  Remote  : $REMOTE_URL"
echo "  Message : $COMMIT_MSG"
echo "══════════════════════════════════════════════════════════════"
echo ""
echo "🧪  To verify tests: pytest backend/adversarial_test_phase114_compliance.py -v"
