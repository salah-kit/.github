#!/usr/bin/env python3
"""Checks this repository's files. CI runs it on every pull request and push to main.

    python3 scripts/check.py

It checks that:
- every issue form parses and has the shape GitHub expects, and uses only labels from labels.json;
- the issue template chooser's config.yml parses;
- labels.json has exactly the labels STANDARD.md lists, each with a valid color;
- .swift-format is byte-identical to templates/.swift-format;
- every relative link in the Markdown files points to a file or folder that exists.

It needs PyYAML (pip install pyyaml==6.0.3) and nothing else outside the standard library.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

try:
    import yaml
except ImportError:
    sys.exit("check.py needs PyYAML: python3 -m pip install pyyaml==6.0.3")

ROOT = Path(__file__).resolve().parent.parent
ISSUE_TEMPLATES = ROOT / ".github" / "ISSUE_TEMPLATE"

# The body element types GitHub's issue forms accept.
ELEMENT_TYPES = {"markdown", "textarea", "input", "dropdown", "checkboxes"}
ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")
HEX_COLOR = re.compile(r"^[0-9A-Fa-f]{6}$")

# Folders whose Markdown is meant to be copied elsewhere, so its relative links resolve only
# in the repository that copies it.
LINK_CHECK_EXCLUDED = {"templates"}

problems: list[str] = []


def problem(path: Path, message: str) -> None:
    problems.append(f"{path.relative_to(ROOT)}: {message}")


def load_yaml(path: Path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        problem(path, f"isn't valid YAML: {error}")
        return None


def load_labels() -> list[dict]:
    path = ROOT / "labels.json"
    try:
        labels = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        problem(path, f"can't be read as JSON: {error}")
        return []
    if not isinstance(labels, list):
        problem(path, "must be a JSON array of labels")
        return []
    return labels


def standard_labels() -> list[str]:
    """The label names in STANDARD.md's "Labels" section, in order."""
    path = ROOT / "STANDARD.md"
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^## Labels\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    if not match:
        problem(path, 'has no "## Labels" section')
        return []
    names = re.findall(r"`([^`]+)`", match.group(1))
    if not names:
        problem(path, 'lists no labels in its "Labels" section')
    return names


def check_labels(labels: list[dict]) -> set[str]:
    path = ROOT / "labels.json"
    names: list[str] = []
    for index, label in enumerate(labels):
        if not isinstance(label, dict):
            problem(path, f"entry {index} isn't an object")
            continue
        name = label.get("name")
        if not isinstance(name, str) or not name:
            problem(path, f"entry {index} has no name")
            continue
        names.append(name)
        color = label.get("color")
        if not isinstance(color, str) or not HEX_COLOR.match(color):
            problem(path, f"{name!r} has color {color!r}; use 6 hex digits without '#'")
        description = label.get("description")
        if not isinstance(description, str) or not description:
            problem(path, f"{name!r} has no description")
        elif len(description) > 100:
            problem(path, f"{name!r} has a description over GitHub's 100-character limit")
        extra = set(label) - {"name", "color", "description"}
        if extra:
            problem(path, f"{name!r} has unknown keys: {', '.join(sorted(extra))}")

    lowered = [name.lower() for name in names]
    duplicates = sorted({name for name in lowered if lowered.count(name) > 1})
    if duplicates:
        problem(path, f"lists these labels more than once: {', '.join(duplicates)}")

    expected = standard_labels()
    if expected and sorted(names) != sorted(expected):
        missing = sorted(set(expected) - set(names))
        unexpected = sorted(set(names) - set(expected))
        detail = []
        if missing:
            detail.append(f"missing {', '.join(missing)}")
        if unexpected:
            detail.append(f"not in STANDARD.md: {', '.join(unexpected)}")
        problem(path, "doesn't match STANDARD.md's labels (" + "; ".join(detail) + ")")
    return set(names)


def check_issue_form(path: Path, label_names: set[str]) -> None:
    form = load_yaml(path)
    if form is None:
        return
    if not isinstance(form, dict):
        problem(path, "must be a YAML mapping")
        return
    for key in ("name", "description"):
        if not isinstance(form.get(key), str) or not form[key].strip():
            problem(path, f"needs a non-empty {key!r}")

    labels = form.get("labels", [])
    if isinstance(labels, str):
        labels = [part.strip() for part in labels.split(",")]
    if not isinstance(labels, list):
        problem(path, "'labels' must be a list")
        labels = []
    for label in labels:
        if label not in label_names:
            problem(path, f"uses label {label!r}, which isn't in labels.json")

    body = form.get("body")
    if not isinstance(body, list) or not body:
        problem(path, "needs a non-empty 'body' list")
        return

    ids: set[str] = set()
    labels_seen: set[str] = set()
    has_input = False
    for index, element in enumerate(body):
        where = f"body[{index}]"
        if not isinstance(element, dict):
            problem(path, f"{where} must be a mapping")
            continue
        kind = element.get("type")
        if kind not in ELEMENT_TYPES:
            problem(path, f"{where} has type {kind!r}; use one of {', '.join(sorted(ELEMENT_TYPES))}")
            continue
        attributes = element.get("attributes")
        if not isinstance(attributes, dict):
            problem(path, f"{where} ({kind}) needs 'attributes'")
            continue

        element_id = element.get("id")
        if element_id is not None:
            if not isinstance(element_id, str) or not ID_PATTERN.match(element_id):
                problem(path, f"{where} has id {element_id!r}; use letters, digits, '-' and '_'")
            elif element_id in ids:
                problem(path, f"{where} repeats the id {element_id!r}")
            else:
                ids.add(element_id)

        if kind == "markdown":
            if not isinstance(attributes.get("value"), str) or not attributes["value"].strip():
                problem(path, f"{where} (markdown) needs a non-empty 'value'")
            continue

        has_input = True
        label = attributes.get("label")
        if not isinstance(label, str) or not label.strip():
            problem(path, f"{where} ({kind}) needs a non-empty 'label'")
        elif label in labels_seen:
            problem(path, f"{where} repeats the label {label!r}")
        else:
            labels_seen.add(label)

        if kind in ("dropdown", "checkboxes"):
            options = attributes.get("options")
            if not isinstance(options, list) or not options:
                problem(path, f"{where} ({kind}) needs a non-empty 'options' list")
                continue
            if kind == "dropdown":
                if not all(isinstance(option, str) and option for option in options):
                    problem(path, f"{where} (dropdown) options must be non-empty strings")
                elif len(set(options)) != len(options):
                    problem(path, f"{where} (dropdown) repeats an option")
                elif "None" in options:
                    problem(path, f"{where} (dropdown) can't use the reserved option 'None'")
                default = attributes.get("default")
                if default is not None and (
                    not isinstance(default, int) or not 0 <= default < len(options)
                ):
                    problem(path, f"{where} (dropdown) default {default!r} isn't an option index")
            else:
                for option in options:
                    if not isinstance(option, dict) or not option.get("label"):
                        problem(path, f"{where} (checkboxes) every option needs a 'label'")
                        break

        validations = element.get("validations")
        if validations is not None and not isinstance(validations, dict):
            problem(path, f"{where} 'validations' must be a mapping")

    if not has_input:
        problem(path, "needs at least one element besides markdown")


def check_issue_templates(label_names: set[str]) -> None:
    if not ISSUE_TEMPLATES.is_dir():
        problems.append(".github/ISSUE_TEMPLATE: missing")
        return
    forms = sorted(
        path
        for path in ISSUE_TEMPLATES.iterdir()
        if path.suffix in (".yml", ".yaml") and path.stem != "config"
    )
    if not forms:
        problems.append(".github/ISSUE_TEMPLATE: has no issue forms")
    for path in forms:
        check_issue_form(path, label_names)

    config_path = ISSUE_TEMPLATES / "config.yml"
    if not config_path.is_file():
        problems.append(".github/ISSUE_TEMPLATE/config.yml: missing")
        return
    config = load_yaml(config_path)
    if config is None:
        return
    if not isinstance(config, dict):
        problem(config_path, "must be a YAML mapping")
        return
    if not isinstance(config.get("blank_issues_enabled"), bool):
        problem(config_path, "'blank_issues_enabled' must be true or false")
    for index, link in enumerate(config.get("contact_links") or []):
        if not isinstance(link, dict) or not all(
            isinstance(link.get(key), str) and link[key] for key in ("name", "url", "about")
        ):
            problem(config_path, f"contact_links[{index}] needs 'name', 'url' and 'about'")
        elif not link["url"].startswith("https://"):
            problem(config_path, f"contact_links[{index}] url must be an https:// URL")


def check_swift_format() -> None:
    root_copy = ROOT / ".swift-format"
    template = ROOT / "templates" / ".swift-format"
    for path in (root_copy, template):
        if not path.is_file():
            problems.append(f"{path.relative_to(ROOT)}: missing")
            return
    if root_copy.read_bytes() != template.read_bytes():
        problem(root_copy, "differs from templates/.swift-format; the two must be identical")


FENCE = re.compile(r"^(\s*)(```|~~~)")
INLINE_CODE = re.compile(r"`[^`]*`")
PROFILE = ROOT / "profile" / "README.md"
INLINE_LINK = re.compile(r"!?\[(?:[^\]\\]|\\.)*\]\(\s*(<[^>]*>|[^)\s]+)(?:\s+[\"'(][^)]*)?\)")
REFERENCE = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*(<[^>]*>|\S+)")
HTML_LINK = re.compile(r"<(?:a|img)\b[^>]*?\b(?:href|src)=[\"']([^\"']+)[\"']", re.IGNORECASE)
SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


def markdown_files() -> list[Path]:
    files = []
    for path in sorted(ROOT.rglob("*.md")):
        parts = path.relative_to(ROOT).parts
        if any(part.startswith(".") and part != ".github" for part in parts[:-1]):
            continue
        if parts[0] in LINK_CHECK_EXCLUDED:
            continue
        files.append(path)
    return files


def links_in(text: str):
    """Yields (line number, target) for each link outside code."""
    in_fence = None
    for number, line in enumerate(text.splitlines(), start=1):
        fence = FENCE.match(line)
        if fence:
            if in_fence is None:
                in_fence = fence.group(2)
            elif fence.group(2) == in_fence:
                in_fence = None
            continue
        if in_fence:
            continue
        line = INLINE_CODE.sub("", line)
        for pattern in (INLINE_LINK, REFERENCE, HTML_LINK):
            for match in pattern.finditer(line):
                yield number, match.group(1).strip("<>")


def check_relative_links() -> None:
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        for number, target in links_in(text):
            if target.startswith("#") or SCHEME.match(target):
                continue  # An anchor in this file, or http(s), mailto and other schemes.
            if path == PROFILE:
                # The org page shows this file at github.com/salah-kit, where a relative link
                # doesn't resolve against this repository.
                problem(path, f"line {number}: link target {target!r} must be an absolute URL")
                continue
            relative = unquote(target.split("#", 1)[0].split("?", 1)[0])
            if not relative:
                continue
            base = ROOT if relative.startswith("/") else path.parent
            resolved = (base / relative.lstrip("/")).resolve()
            if not resolved.exists():
                problem(path, f"line {number}: link target {target!r} doesn't exist")
            elif ROOT not in resolved.parents and resolved != ROOT:
                problem(path, f"line {number}: link target {target!r} is outside the repository")


def main() -> int:
    label_names = check_labels(load_labels())
    check_issue_templates(label_names)
    check_swift_format()
    check_relative_links()

    if problems:
        for line in problems:
            print(f"error: {line}")
        print(f"\n{len(problems)} problem(s) found.")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
