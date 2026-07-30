#!/usr/bin/env bash
# Publish a sanitized single-commit release to GitHub.
#
# A GitHub Action cannot do this job. By the time a workflow runs, the push has
# already happened and anything internal is in the remote's history. Stripping
# must happen here, before the push. The workflow is the backstop.
#
# What this does:
#   1. refuses to run unless the working tree is clean and checks pass
#   2. builds an orphan branch from the current tree (no history carried over)
#   3. repoints REPO_URL at the public repository
#   4. rebuilds the deliverable so every generated link follows
#   5. refuses to continue if anything internal survives
#   6. commits as the configured identity, with no agent trailers
#   7. pushes only after all of the above passed
#
# Usage:
#   tools/release-github.sh [--dry-run] [--repo NAME] [--visibility private|public]
#
# Exit: 0 released (or dry run clean), 1 refused
set -uo pipefail

cd "$(dirname "$0")/.."

OWNER="AdamPippert"
REPO="AgentStyleGuide"
VISIBILITY="private"
DRY_RUN=0
BRANCH="github-release"
AUTHOR_NAME="Adam Pippert"
AUTHOR_EMAIL="adam.pippert@gmail.com"
SOURCE_BRANCH="main"

while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run)    DRY_RUN=1 ;;
    --repo)       REPO="$2"; shift ;;
    --visibility) VISIBILITY="$2"; shift ;;
    --owner)      OWNER="$2"; shift ;;
    -h|--help)    sed -n '2,28p' "$0"; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 1 ;;
  esac
  shift
done

PUBLIC_URL="https://github.com/${OWNER}/${REPO}"

say()  { printf '\n== %s\n' "$1"; }
ok()   { printf '   OK    %s\n' "$1"; }
die()  { printf '   REFUSED  %s\n' "$1" >&2; cleanup; exit 1; }

start_branch=$(git rev-parse --abbrev-ref HEAD)
start_sha=$(git rev-parse HEAD 2>/dev/null)
switched=0   # set to 1 only once the orphan branch is actually checked out

# Return to the starting branch WITHOUT discarding anything.
#
# Two earlier versions of this function destroyed uncommitted work: one ran
# "git checkout -- .", the other "git checkout --force". Both wiped edits that
# were still in the tree when the script refused at the precondition step,
# before it had switched branches at all. The guard below is the fix: if we
# never left the starting branch, cleanup does nothing whatsoever.
cleanup() {
  [ "$switched" -eq 1 ] || return 0
  cur=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
  [ "$cur" = "$start_branch" ] && return 0
  if ! git checkout -q "$start_branch" 2>/dev/null; then
    printf '   NOTE  could not return to %s; you are on %s and nothing was\n' \
      "$start_branch" "$cur" >&2
    printf '         discarded. Resolve by hand.\n' >&2
    return 0
  fi
  now=$(git rev-parse HEAD 2>/dev/null)
  if [ "$now" != "$start_sha" ]; then
    printf '   NOTE  %s is no longer at %s; check before continuing\n' \
      "$start_branch" "${start_sha:0:7}" >&2
  fi
}
trap cleanup EXIT

say "1. Preconditions"
[ "$start_branch" = "$SOURCE_BRANCH" ] || die "run from $SOURCE_BRANCH, not $start_branch"
[ -z "$(git status --porcelain)" ] || die "working tree is dirty; commit or stash first"
command -v gh >/dev/null || die "gh is not installed"
gh auth status >/dev/null 2>&1 || die "gh is not authenticated"
active=$(gh api user --jq .login 2>/dev/null)
[ "$active" = "$OWNER" ] || die "gh is authenticated as '$active', expected '$OWNER'"
ok "on $SOURCE_BRANCH, tree clean, gh authenticated as $OWNER"

say "2. Source checks"
./tools/check.sh >/dev/null 2>&1 || die "tools/check.sh fails on $SOURCE_BRANCH"
ok "self-check passes"

say "3. Building orphan branch '$BRANCH'"
git branch -D "$BRANCH" >/dev/null 2>&1
git checkout -q --orphan "$BRANCH" || die "could not create orphan branch"
switched=1
ok "orphan branch created from current tree"

say "4. Repointing REPO_URL at $PUBLIC_URL"
before=$(grep -c '^REPO_URL' tools/build-deliverable.py)
[ "$before" -eq 1 ] || die "expected exactly one REPO_URL line, found $before"
python3 - "$PUBLIC_URL" <<'PY'
import pathlib, re, sys
url = sys.argv[1]
p = pathlib.Path("tools/build-deliverable.py")
s = p.read_text()
s2 = re.sub(r'^REPO_URL = ".*"$', f'REPO_URL = "{url}"', s, count=1, flags=re.M)
if s == s2:
    sys.exit("REPO_URL substitution did not change anything")
p.write_text(s2)
PY
[ $? -eq 0 ] || die "could not rewrite REPO_URL"
grep -q "^REPO_URL = \"${PUBLIC_URL}\"$" tools/build-deliverable.py || die "REPO_URL rewrite did not take"
ok "REPO_URL now $PUBLIC_URL"

say "5. Rebuilding deliverable so generated links follow"
python3 tools/build-deliverable.py >/dev/null 2>&1
# A dirty tree here is expected: inputs changed and nothing is committed yet.
grep -q "$PUBLIC_URL" dist/WRITING-STANDARD.md || die "deliverable did not pick up the public URL"
ok "deliverable rebuilt"

say "6. Scanning for internal detail"
if ! ./tools/scan-internal.sh; then
  die "internal detail survived sanitization; nothing was pushed"
fi
ok "no internal references"

say "7. Re-running self-check after rewrite"
python3 tools/lint.py $(git ls-files '*.md' | grep -v '^tools/testdata/') >/dev/null 2>&1 \
  || die "markdown no longer conforms after the rewrite"
ok "all markdown still conforms"

say "8. Committing as $AUTHOR_NAME <$AUTHOR_EMAIL>"
git add -A
GIT_AUTHOR_NAME="$AUTHOR_NAME"   GIT_AUTHOR_EMAIL="$AUTHOR_EMAIL" \
GIT_COMMITTER_NAME="$AUTHOR_NAME" GIT_COMMITTER_EMAIL="$AUTHOR_EMAIL" \
git commit -q -F - <<MSG
AgentStyleGuide: a writing standard for specs and development documentation

A controlled language for specifications and development documentation,
written for human authors and agent authors alike.

Derived from ASD-STE100 Simplified Technical English, extended with
procedure and conditional-logic rules from DOE-STD-1029-92, and extended
again with rules addressing the failure modes of generated prose.

  STANDARD.md      the rules, sections 1-11 and appendices A-E
  PROVENANCE.md    source register, licenses, per-source derivation
  CHECKLIST.md     the checks no script can make
  tools/lint.py    mechanical checks, with a negative test fixture
  tools/check.sh   self-check: the repository obeys the standard it publishes
  dist/            the single-file deliverable and its pointer files
  sources/         pinned public-domain sources, with checksums

No ASD-STE100 text or dictionary content is reproduced. ASD-STE100 is a
copyright and trademark of ASD, Brussels; see PROVENANCE.md section 3 for
the boundary this project keeps.
MSG
[ $? -eq 0 ] || die "commit failed"
ok "committed $(git rev-parse --short HEAD)"

say "8b. Settling the deliverable stamp"
# The build before the commit had no commit to read, so it stamped
# "uncommitted". Rebuild now that one exists, amend, and confirm a second
# rebuild changes nothing. The digest is content-derived and the date is an
# author date, so this settles in one pass rather than chasing its own tail.
python3 tools/build-deliverable.py >/dev/null 2>&1
if [ -n "$(git status --porcelain)" ]; then
  git add -A
  GIT_AUTHOR_NAME="$AUTHOR_NAME"   GIT_AUTHOR_EMAIL="$AUTHOR_EMAIL" \
  GIT_COMMITTER_NAME="$AUTHOR_NAME" GIT_COMMITTER_EMAIL="$AUTHOR_EMAIL" \
  git commit -q --amend --no-edit || die "amend failed"
  python3 tools/build-deliverable.py >/dev/null 2>&1
  [ -z "$(git status --porcelain)" ] || die "deliverable stamp will not settle"
fi
grep -q "UNCOMMITTED" dist/WRITING-STANDARD.md && die "deliverable still marked UNCOMMITTED"
ok "stamp settled at $(git rev-parse --short HEAD)"

say "9. Verifying the commit"
[ -z "$(git log --format=%P -1)" ] || die "commit has a parent; expected an orphan"
[ "$(git log --format='%an <%ae>' -1)" = "$AUTHOR_NAME <$AUTHOR_EMAIL>" ] \
  || die "author is $(git log --format='%an <%ae>' -1)"
[ "$(git log --format='%cn <%ce>' -1)" = "$AUTHOR_NAME <$AUTHOR_EMAIL>" ] \
  || die "committer is $(git log --format='%cn <%ce>' -1)"
if git log --format=%B -1 | grep -qiE "co-authored-by|claude|anthropic|gpt|copilot"; then
  die "commit message names an agent"
fi
ok "single orphan commit, correct identity, no agent trailers"

say "10. Scanning the committed tree"
./tools/scan-internal.sh "$BRANCH" >/dev/null || die "committed tree contains internal detail"
ok "committed tree is clean"

if [ "$DRY_RUN" -eq 1 ]; then
  say "Dry run"
  echo "   Would push $BRANCH to ${PUBLIC_URL} as main (${VISIBILITY})."
  echo "   Branch '$BRANCH' is left in place for inspection."
  trap - EXIT
  git checkout -q "$start_branch"
  exit 0
fi

say "11. Publishing to $PUBLIC_URL"
if gh repo view "${OWNER}/${REPO}" >/dev/null 2>&1; then
  ok "repository exists"
else
  gh repo create "${OWNER}/${REPO}" --"${VISIBILITY}" \
    --description "A writing standard for specifications and development documentation." \
    >/dev/null || die "could not create repository"
  ok "repository created (${VISIBILITY})"
fi

git push -q --force "https://github.com/${OWNER}/${REPO}.git" "${BRANCH}:main" \
  || die "push failed"
ok "pushed ${BRANCH} to ${OWNER}/${REPO}:main"

say "12. Verifying what landed"
remote_sha=$(gh api "repos/${OWNER}/${REPO}/commits/main" --jq .sha 2>/dev/null | cut -c1-7)
local_sha=$(git rev-parse --short "$BRANCH")
[ "$remote_sha" = "$local_sha" ] || echo "   NOTE: remote $remote_sha, local $local_sha"
ok "remote main is $remote_sha"

trap - EXIT
git checkout -q "$start_branch"
printf '\nReleased. %s\n' "$PUBLIC_URL"
