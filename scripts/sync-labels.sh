#!/usr/bin/env bash
# Makes each repository's labels match labels.json.
#
#   scripts/sync-labels.sh [--dry-run] [--prune] <owner/repo>...
#
# Creates every label in labels.json that a repository lacks, and updates the color and
# description of those that differ. Running it again changes nothing.
#
#   --prune    also deletes labels that aren't in labels.json, but only when no issue or
#              pull request uses them; it reports the ones it keeps.
#   --dry-run  prints what it would do, and makes only read-only calls.
#
# Needs gh, authenticated with permission to manage the repositories' labels, and python3.

set -euo pipefail

usage() {
  echo "usage: $0 [--dry-run] [--prune] <owner/repo>..." >&2
  exit 2
}

dry_run=0
prune=0
repos=()
for arg in "$@"; do
  case "$arg" in
    --dry-run) dry_run=1 ;;
    --prune) prune=1 ;;
    -h | --help) usage ;;
    -*)
      echo "unknown option: $arg" >&2
      usage
      ;;
    */*) repos+=("$arg") ;;
    *)
      echo "not an owner/repo: $arg" >&2
      usage
      ;;
  esac
done
[ "${#repos[@]}" -gt 0 ] || usage

labels_file="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/labels.json"
sep=$'\x1f' # The unit separator: never in a label, and not whitespace, so empty fields survive.

# One line per wanted label: name, color, description.
wanted="$(
  python3 - "$labels_file" <<'PY'
import json, re, sys
labels = json.load(open(sys.argv[1], encoding="utf-8"))
for label in labels:
    name, color, description = label["name"], label["color"], label.get("description", "")
    if not re.fullmatch(r"[0-9a-fA-F]{6}", color):
        sys.exit(f"labels.json: {name!r} has color {color!r}, not 6 hex digits")
    print("\x1f".join([name, color.lower(), description]))
PY
)"

lower() { printf '%s' "$1" | tr '[:upper:]' '[:lower:]'; }

# Number of issues and pull requests, in any state, that carry the label.
usage_count() {
  local repo="$1" name="$2" issues prs
  issues="$(gh issue list -R "$repo" --label "$name" --state all --limit 1 \
    --json number --jq length </dev/null)"
  prs="$(gh pr list -R "$repo" --label "$name" --state all --limit 1 \
    --json number --jq length </dev/null)"
  echo $((issues + prs))
}

act() {
  if [ "$dry_run" -eq 1 ]; then
    echo "  would $1"
  else
    echo "  $1"
  fi
}

for repo in "${repos[@]}"; do
  echo "$repo"
  existing="$(gh label list -R "$repo" --limit 1000 --json name,color,description \
    --jq '.[] | [.name, (.color | ascii_downcase), (.description // "")] | join("\u001f")' \
    </dev/null)"

  while IFS="$sep" read -r name color description; do
    [ -n "$name" ] || continue
    current=""
    current_name=""
    while IFS="$sep" read -r ename ecolor edescription; do
      if [ "$(lower "$ename")" = "$(lower "$name")" ]; then
        current="$ename$sep$ecolor$sep$edescription"
        current_name="$ename"
        break
      fi
    done <<<"$existing"

    if [ "$current" = "$name$sep$color$sep$description" ]; then
      echo "  unchanged: $name"
      continue
    elif [ -z "$current" ]; then
      act "create: $name ($color, \"$description\")"
    else
      act "update: $name ($color, \"$description\")"
    fi
    if [ "$dry_run" -eq 1 ]; then
      :
    elif [ -n "$current_name" ] && [ "$current_name" != "$name" ]; then
      # Label names are case-insensitive on GitHub; only an edit changes a name's case.
      gh label edit "$current_name" -R "$repo" --name "$name" --color "$color" \
        --description "$description" </dev/null >/dev/null
    else
      gh label create "$name" -R "$repo" --color "$color" --description "$description" --force \
        </dev/null >/dev/null
    fi
  done <<<"$wanted"

  [ "$prune" -eq 1 ] || continue
  while IFS="$sep" read -r ename _ _; do
    [ -n "$ename" ] || continue
    keep=0
    while IFS="$sep" read -r name _ _; do
      if [ "$(lower "$ename")" = "$(lower "$name")" ]; then
        keep=1
        break
      fi
    done <<<"$wanted"
    [ "$keep" -eq 0 ] || continue

    count="$(usage_count "$repo" "$ename")"
    if [ "$count" -gt 0 ]; then
      echo "  kept, in use: $ename"
      continue
    fi
    act "delete: $ename"
    if [ "$dry_run" -eq 0 ]; then
      gh label delete "$ename" -R "$repo" --yes </dev/null >/dev/null
    fi
  done <<<"$existing"
done
