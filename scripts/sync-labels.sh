#!/usr/bin/env bash
# Makes each repository's labels match labels.json.
#
#   scripts/sync-labels.sh [--dry-run] [--prune] <owner/repo>...
#
# Creates every label in labels.json that a repository lacks, and updates the color and
# description of those that differ. Running it again changes nothing.
#
#   --prune    also deletes labels that aren't in labels.json, but only when no issue, pull
#              request or discussion uses them; it reports the ones it keeps, and stops
#              without deleting if it can't tell.
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

# Number of issues, pull requests and discussions, in any state, that carry the label. It looks
# the label up by its exact name, and prints nothing and fails when GitHub can't say.
usage_count() {
  python3 - "$1" "$2" <<'PY'
import json, subprocess, sys

repo, label = sys.argv[1], sys.argv[2]
owner, name = repo.split("/", 1)
query = """
query($owner: String!, $name: String!, $label: String!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    label(name: $label) { issues { totalCount } pullRequests { totalCount } }
    discussions(first: 100, after: $cursor) {
      pageInfo { hasNextPage endCursor }
      nodes { labels(first: 100) { nodes { name } } }
    }
  }
}
"""
count, cursor = None, None
while True:
    args = ["gh", "api", "graphql", "-f", f"query={query}", "-f", f"owner={owner}",
            "-f", f"name={name}", "-f", f"label={label}"]
    if cursor:
        args += ["-f", f"cursor={cursor}"]
    result = subprocess.run(args, capture_output=True, text=True, stdin=subprocess.DEVNULL)
    if result.returncode != 0:
        sys.exit(result.stderr.strip() or f"gh exited with {result.returncode}")
    try:
        response = json.loads(result.stdout)
    except json.JSONDecodeError:
        sys.exit(f"gh returned something other than JSON: {result.stdout[:200]!r}")
    if response.get("errors"):
        sys.exit("; ".join(error.get("message", "") for error in response["errors"]))
    repository = response["data"]["repository"]
    if count is None:
        if repository["label"] is None:
            sys.exit(f"no label named {label!r}")
        count = (repository["label"]["issues"]["totalCount"]
                 + repository["label"]["pullRequests"]["totalCount"])
    discussions = repository["discussions"]
    for discussion in discussions["nodes"]:
        names = [node["name"].lower() for node in discussion["labels"]["nodes"]]
        count += names.count(label.lower())
    if not discussions["pageInfo"]["hasNextPage"]:
        break
    cursor = discussions["pageInfo"]["endCursor"]
print(count)
PY
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

    # A command substitution ignores errexit, so check the count before trusting it.
    if ! count="$(usage_count "$repo" "$ename")" || ! [[ "$count" =~ ^[0-9]+$ ]]; then
      echo "$repo: can't tell whether \"$ename\" is in use, so it stays; stopping" >&2
      exit 1
    fi
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
