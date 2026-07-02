#!/bin/bash
# Literature-survey helper — resumable-progress check.
# Reports which expected review notes already exist. The checkpoint is the
# FILESYSTEM: every note that finished is on disk, independent of any session or
# workflow memory. Run this after a usage-limit interruption to see what is left,
# then re-run the (idempotent) deep-read workflow to fill only the gaps.
#
# Assumes the manifest has a numbered markdown table whose LAST column per
# numbered row is the Note filename. Edit MANIFEST and NOTEDIR per survey.

MANIFEST=/ABS/PATH/TO/review-manifest.md
NOTEDIR=/ABS/PATH/TO/ai-survey-notes/YYYY-MM

# expected note filenames = last non-empty cell of each numbered table row
awk -F'|' '/^\| *[0-9]+ /{n=$(NF-1); gsub(/^ +| +$/,"",n); print n}' "$MANIFEST" | sort > /tmp/survey_want.txt
ls -1 "$NOTEDIR" 2>/dev/null | grep '\.md$' | sort > /tmp/survey_have.txt

want=$(wc -l < /tmp/survey_want.txt | tr -d ' ')
done=$(comm -12 /tmp/survey_want.txt /tmp/survey_have.txt | wc -l | tr -d ' ')
miss=$(comm -23 /tmp/survey_want.txt /tmp/survey_have.txt | wc -l | tr -d ' ')

echo "expected notes : $want"
echo "written        : $done"
echo "MISSING        : $miss"
if [ "$miss" -gt 0 ]; then
  echo "--- missing note filenames ---"
  comm -23 /tmp/survey_want.txt /tmp/survey_have.txt
fi
