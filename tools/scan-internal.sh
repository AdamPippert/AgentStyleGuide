#!/usr/bin/env bash
# Fail if internal infrastructure detail appears in tracked files.
#
# Runs in two places: locally before a GitHub release, and in CI on GitHub as
# a backstop for a push that skipped the release script.
#
# This file and the workflow that calls it are excluded from their own scan,
# because they necessarily contain the patterns they search for.
#
# EXPECTED TO FAIL on the internal branch. main is hosted on the tailnet and
# legitimately carries the Forgejo URL. Run this against the sanitized release
# branch, which is what tools/release-github.sh does. A failure here on main is
# the tool working, not a problem to fix.
#
# Usage: tools/scan-internal.sh [REF]     REF defaults to the working tree
# Exit:  0 clean, 1 something internal found
set -uo pipefail

cd "$(dirname "$0")/.."
REF="${1:-}"

SELF="tools/scan-internal.sh"
WORKFLOW=".github/workflows/release-guard.yml"

# name|regex  — keep descriptions specific so a hit explains itself
PATTERNS=(
  "tailnet MagicDNS name|[a-z0-9-]+\.tail[0-9a-f]+\.ts\.net"
  "any .ts.net host|[a-z0-9-]+\.ts\.net"
  "tailnet CGNAT address|\b100\.(6[4-9]|[7-9][0-9]|1[0-1][0-9]|12[0-7])\.[0-9]{1,3}\.[0-9]{1,3}\b"
  "RFC1918 address|\b(192\.168\.[0-9]{1,3}\.[0-9]{1,3}|10\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\b"
  "fleet hostname|\b(superrouter|jekyll|hyde|ns102375|coastaldigital|jumpbox|holstein|highland|jersey|glkvm|adams-mac-studio|adams-macbook-pro|apippert-mac)\b"
  "GitHub token|gh[pousr]_[A-Za-z0-9]{16,}"
  "private key block|BEGIN [A-Z ]*PRIVATE KEY"
  "AWS access key|\bAKIA[0-9A-Z]{16}\b"
  "vault path|kv/(secrets|ssh|llm-providers)/"
)

if [ -n "$REF" ]; then
  files=$(git ls-tree -r --name-only "$REF")
  read_file() { git show "$REF:$1" 2>/dev/null; }
  label="ref $REF"
else
  files=$(git ls-files)
  read_file() { cat "$1" 2>/dev/null; }
  label="working tree"
fi

echo "scanning $label"

# File-major so each offending line is reported once, with the most specific
# pattern that matched. Overlapping patterns are deliberate: a leak should be
# caught by more than one rule, but a reader wants one line per problem.
found=0
for f in $files; do
  case "$f" in
    "$SELF"|"$WORKFLOW") continue ;;
    *.pdf|sources/SHA256SUMS) continue ;;
  esac
  content=$(read_file "$f") || continue
  [ -n "$content" ] || continue

  file_hits=""
  for entry in "${PATTERNS[@]}"; do
    name="${entry%%|*}"
    rx="${entry#*|}"
    while IFS= read -r hit; do
      [ -n "$hit" ] || continue
      ln="${hit%%:*}"
      case "$file_hits" in
        *"|${ln}|"*) continue ;;   # already reported this line
      esac
      file_hits="${file_hits}|${ln}|"
      printf '%s\n' "    $f:$hit  <-- $name"
    done < <(printf '%s\n' "$content" | grep -nEI "$rx" 2>/dev/null | head -20)
  done

  if [ -n "$file_hits" ]; then
    found=1
  fi
done

echo
if [ "$found" -eq 0 ]; then
  echo "clean: no internal references"
  exit 0
fi
cat <<'EOF'
FAILED: internal detail must not reach a public repository.

Fix the source, rebuild, and rescan. Do not simply amend the commit that
carries it — if it has already been pushed, the value is in the remote's
history and must be treated as disclosed.
EOF
exit 1
