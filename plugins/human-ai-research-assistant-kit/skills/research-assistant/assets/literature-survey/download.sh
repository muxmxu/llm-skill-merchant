#!/bin/bash
# Literature-survey helper — batch PDF download.
# Reads a "## Download list" fenced block from the manifest, where each line is
#   <url>|<filename>.pdf
# Downloads in parallel, validates each is a real PDF (HTTP 200 + size + %PDF
# magic), deletes failures, and is idempotent (skips files already present).
# Edit DEST and MANIFEST per survey.
set -u
DEST=/ABS/PATH/TO/reference/<topic>
MANIFEST=/ABS/PATH/TO/review-manifest.md
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
mkdir -p "$DEST"

# Extract the first fenced code block after "## Download list"
awk '/^## Download list/{f=1} f&&/^```/{c++; next} f&&c==1{print}' "$MANIFEST" > /tmp/survey_dl.txt

download_one() {
  line="$1"
  url="${line%%|*}"; fn="${line##*|}"
  [ -z "$url" ] && return
  if [ -s "$DEST/$fn" ]; then echo "SKIP $fn"; return; fi
  code=$(curl -sL --max-time 90 -A "$UA" -w "%{http_code}" -o "$DEST/$fn" "$url")
  sz=$(stat -f%z "$DEST/$fn" 2>/dev/null || echo 0)
  head=$(head -c 4 "$DEST/$fn" 2>/dev/null)
  if [ "$code" = "200" ] && [ "$sz" -gt 10000 ] && [ "$head" = "%PDF" ]; then
    echo "OK   $fn ($sz)"
  else
    echo "FAIL $fn http=$code sz=$sz head=$head"
    rm -f "$DEST/$fn"
  fi
}
export -f download_one; export DEST UA

xargs -P 6 -I {} bash -c 'download_one "$@"' _ {} < /tmp/survey_dl.txt | sort

echo "---"
echo "downloaded: $(ls -1 "$DEST"/*.pdf 2>/dev/null | wc -l | tr -d ' ') PDFs in $DEST"
