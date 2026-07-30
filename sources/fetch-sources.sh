#!/usr/bin/env bash
# Re-fetch the pinned public-domain sources and compare against SHA256SUMS.
# Never overwrites a pinned file. See ../PROVENANCE.md §1.
set -euo pipefail

cd "$(dirname "$0")"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36'

# name|url
SOURCES=(
  "DOE-STD-1029-92.pdf|https://www.osti.gov/servlets/purl/308015"
  "NASA-SP-7084.pdf|https://ntrs.nasa.gov/api/citations/19900017394/downloads/19900017394.pdf"
)

if command -v sha256sum >/dev/null 2>&1; then
  SHA() { sha256sum "$1" | awk '{print $1}'; }
else
  SHA() { shasum -a 256 "$1" | awk '{print $1}'; }
fi

drift=0
for entry in "${SOURCES[@]}"; do
  name="${entry%%|*}"
  url="${entry#*|}"
  printf '%-24s ' "$name"

  if ! curl -sfL -A "$UA" --max-time 120 "$url" -o "$TMP/$name"; then
    echo "FETCH FAILED — $url"
    drift=1
    continue
  fi

  if ! file "$TMP/$name" | grep -q 'PDF document'; then
    echo "NOT A PDF (server returned an error page)"
    drift=1
    continue
  fi

  want="$(awk -v n="$name" '$2 == n {print $1}' SHA256SUMS)"
  got="$(SHA "$TMP/$name")"

  if [ -z "$want" ]; then
    echo "UNPINNED — add to SHA256SUMS: $got"
    drift=1
  elif [ "$want" = "$got" ]; then
    echo "OK (matches pin)"
  else
    echo "DRIFT"
    echo "    pinned:  $want"
    echo "    fetched: $got"
    echo "    Upstream changed. Review it, update PROVENANCE.md, then repin."
    drift=1
  fi
done

if [ "$drift" -ne 0 ]; then
  echo
  echo "One or more sources drifted or failed. Nothing was overwritten."
  exit 1
fi

echo
echo "All pinned sources match."
