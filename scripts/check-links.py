#!/usr/bin/env python3
"""Checks that the absolute links in this repository's Markdown files and issue forms resolve.

    python3 scripts/check-links.py

It requests every https:// URL once (HEAD, then GET when a server refuses HEAD), follows
redirects, retries a few times, and prints a table. It exits with 1 when any link fails.

External sites can be slow or down for a while, so CI runs this weekly and on demand, not on
pull requests. Uses only the standard library.
"""

from __future__ import annotations

import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Markdown meant to be copied elsewhere; its URLs contain placeholders such as <Repo>.
EXCLUDED = {"templates"}

TIMEOUT = 20
ATTEMPTS = 3
USER_AGENT = "salah-kit-link-check (+https://github.com/salah-kit/.github)"

FENCE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE = re.compile(r"`[^`]*`")
URL = re.compile(r"https://[^\s<>()\[\]\"'`]+")
TRAILING = ".,;:!?*_"


def source_files() -> list[Path]:
    files = []
    for path in sorted(ROOT.rglob("*")):
        relative = path.relative_to(ROOT)
        if not path.is_file() or relative.parts[0] in EXCLUDED or relative.parts[0] == ".git":
            continue
        is_form = relative.parts[:2] == (".github", "ISSUE_TEMPLATE") and path.suffix == ".yml"
        if path.suffix == ".md" or is_form:
            files.append(path)
    return files


def urls_in(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    found = []
    in_fence = False
    for line in text.splitlines():
        if path.suffix == ".md":
            if FENCE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            line = INLINE_CODE.sub("", line)
        for match in URL.finditer(line):
            found.append(match.group(0).rstrip(TRAILING))
    return found


def request(url: str, method: str) -> tuple[int, str]:
    req = urllib.request.Request(url, method=method, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
        return response.status, response.geturl()


def check(url: str) -> tuple[str, int | None, str]:
    """Returns (result, status, detail) for one URL."""
    last_error = ""
    status = None
    for attempt in range(ATTEMPTS):
        if attempt:
            time.sleep(2**attempt)
        for method in ("HEAD", "GET"):
            try:
                status, final = request(url, method)
                detail = "" if final == url else f"redirects to {final}"
                return "ok", status, detail
            except urllib.error.HTTPError as error:
                status = error.code
                last_error = f"HTTP {error.code} {error.reason}"
                if method == "HEAD" and error.code in (403, 404, 405, 501):
                    continue  # Some servers refuse HEAD; try GET.
                if error.code == 404:
                    return "FAIL", status, last_error
                break  # Retry other errors, such as 429 and 5xx.
            except (urllib.error.URLError, TimeoutError, OSError) as error:
                status = None
                last_error = str(getattr(error, "reason", error))
                break
    return "FAIL", status, last_error


def main() -> int:
    sources: dict[str, list[str]] = {}
    for path in source_files():
        for url in urls_in(path):
            sources.setdefault(url, [])
            name = str(path.relative_to(ROOT))
            if name not in sources[url]:
                sources[url].append(name)

    urls = sorted(sources)
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(check, urls))

    failures = 0
    print("| Result | Status | URL | Detail | Found in |")
    print("|---|---|---|---|---|")
    for url, (result, status, detail) in zip(urls, results):
        failures += result != "ok"
        found_in = ", ".join(sources[url])
        print(f"| {result} | {status or '-'} | {url} | {detail} | {found_in} |")
    print(f"\n{len(urls)} links checked, {failures} failed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
