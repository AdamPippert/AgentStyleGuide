#!/usr/bin/env bash
# Self-check. The repository must obey the standard it publishes.
#
# Discovers every tracked markdown file rather than naming them, so a new
# document cannot silently escape the checks.
#
# Usage: tools/check.sh
# Exit:  0 all checks pass, 1 a check failed
set -uo pipefail

cd "$(dirname "$0")/.."

# Deliberately non-conforming; it proves the linter still fires.
FIXTURE="tools/testdata/bad.md"

fail=0
step() { printf '\n== %s\n' "$1"; }
ok()   { printf '   PASS  %s\n' "$1"; }
bad()  { printf '   FAIL  %s\n' "$1"; fail=1; }

step "1. Every tracked markdown file obeys the standard"
governed=$(git ls-files '*.md' | grep -v "^${FIXTURE}$")
if [ -z "$governed" ]; then
  bad "no markdown files found; is this a git checkout?"
else
  # shellcheck disable=SC2086
  if python3 tools/lint.py $governed; then
    ok "$(echo "$governed" | wc -l | tr -d ' ') file(s) conform"
  else
    bad "see findings above"
  fi
fi

step "2. The linter still detects violations"
if python3 tools/lint.py "$FIXTURE" >/dev/null 2>&1; then
  bad "$FIXTURE passed; the linter has stopped working"
else
  ok "fixture still fails as designed"
fi

step "2b. Every fixture case came from a real violation"
# A synthetic fixture drifts from reality. Each case must name where it was
# actually observed, so the suite tracks failures that happened rather than
# failures someone imagined.
if python3 - "$FIXTURE" <<'PY'
import re, sys
text = open(sys.argv[1], encoding="utf-8").read()
# Content after the preamble; a case is a text block, optionally preceded by
# an "observed:" comment on the immediately preceding lines.
body = text.split("still fails.", 1)[-1]
blocks = [b.strip() for b in body.split("\n\n") if b.strip()]
cases, undocumented = 0, []
for b in blocks:
    prose = re.sub(r"<!--.*?-->", "", b, flags=re.S).strip()
    if not prose or prose.startswith("#"):
        continue
    cases += 1
    if "<!-- observed:" not in b:
        undocumented.append(prose.splitlines()[0][:60])
if not cases:
    sys.exit("no fixture cases found; the parser or the file is wrong")
if undocumented:
    sys.exit("cases without provenance: " + "; ".join(undocumented))
print(f"{cases} case(s), all with provenance")
PY
then
  ok "every case names where it was observed"
else
  bad "see above"
fi

step "3. The deliverable is current and self-consistent"
before=$(git status --porcelain dist/ 2>/dev/null)
if python3 tools/build-deliverable.py; then
  after=$(git status --porcelain dist/ 2>/dev/null)
  if [ "$before" = "$after" ]; then
    ok "deliverable already up to date"
  else
    bad "deliverable was stale; it has been rebuilt, commit the result"
  fi
else
  bad "build failed or the deliverable breaks its own standard"
fi

step "4. Pinned sources match their checksums"
if (cd sources && { sha256sum -c SHA256SUMS >/dev/null 2>&1 \
    || shasum -a 256 -c SHA256SUMS >/dev/null 2>&1; }); then
  ok "source checksums match"
else
  bad "a pinned source does not match SHA256SUMS"
fi

step "5. No unpinned material in sources/"
# PROVENANCE.md section 3 forbids committing ASD-STE100 in any form. Grepping
# prose cannot tell a prohibition from a violation, so check the invariant
# that actually matters: every binary in sources/ is pinned in SHA256SUMS.
unpinned=""
for f in $(git ls-files 'sources/*'); do
  base="${f#sources/}"
  case "$base" in
    *.md|*.sh|SHA256SUMS) continue ;;
  esac
  grep -q " ${base}\$" sources/SHA256SUMS || unpinned="$unpinned $base"
done
if [ -z "$unpinned" ]; then
  ok "every vendored source is pinned"
else
  bad "unpinned file(s) in sources/:$unpinned — pin them or remove them"
fi

step "6. Readability gates"
# Only the gating metrics fail the build. The proxies are printed for trend.
if python3 tools/evaluate.py >/tmp/asg-eval.$$ 2>&1; then
  ok "$(grep -cE 'advisory$' /tmp/asg-eval.$$) advisory, all gates within threshold"
else
  sed 's/^/   /' /tmp/asg-eval.$$
  bad "a gating metric is below its floor"
fi
rm -f /tmp/asg-eval.$$

printf '\n'
if [ "$fail" -eq 0 ]; then
  echo "All checks passed."
else
  echo "One or more checks failed."
fi
exit "$fail"
