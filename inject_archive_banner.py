#!/usr/bin/env python3
"""Inject MkDocs Material announcement banner into archived docs-site HTML."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ARCHIVED_VERSIONS = [
    "25.3.0",
    "25.4.2",
    "25.6.2",
    "25.6.3",
    "25.9.0",
    "26.1.1",
    "26.1.2",
]

BANNER = """
<div class="md-banner" data-md-component="announce">
  <div class="md-banner__inner md-grid md-typeset">
    📦 <strong>Archived Documentation – Reference Only</strong> — This documentation is retained for customers using legacy product versions. It is no longer actively maintained, validated, or updated, and should not be relied upon for current product capabilities, security guidance, or operational decisions. For supported and up-to-date documentation, visit <a href="https://docs.nvidia.com/nemo/retriever/latest/">NVIDIA Docs Hub: NeMo Retriever</a>.
  </div>
</div>
""".strip()

ARCHIVE_MARKER = "Archived Documentation – Reference Only"
BODY_OPEN_RE = re.compile(r"(<body[^>]*>)", re.IGNORECASE)
EMPTY_ANNOUNCE_RE = re.compile(
    r"<div\s+data-md-component=\"announce\">\s*</div>",
    re.IGNORECASE | re.DOTALL,
)


def inject_banner(html: str) -> tuple[str, str]:
    if ARCHIVE_MARKER in html:
        return html, "skipped"

    empty_announce = EMPTY_ANNOUNCE_RE.search(html)
    if empty_announce:
        updated = html[: empty_announce.start()] + BANNER + html[empty_announce.end() :]
        return updated, "filled-announce"

    body_match = BODY_OPEN_RE.search(html)
    if not body_match:
        return html, "no-body"

    updated = html[: body_match.end()] + "\n" + BANNER + html[body_match.end() :]
    return updated, "injected-body"


def main() -> int:
    root = Path(__file__).resolve().parent
    totals: dict[str, int] = {}

    for version in ARCHIVED_VERSIONS:
        version_dir = root / version
        if not version_dir.is_dir():
            print(f"ERROR: missing version folder {version_dir}", file=sys.stderr)
            totals["errors"] = totals.get("errors", 0) + 1
            continue

        version_counts: dict[str, int] = {}
        for html_path in version_dir.rglob("*.html"):
            try:
                original = html_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                original = html_path.read_text(encoding="latin-1")

            updated, status = inject_banner(original)
            version_counts[status] = version_counts.get(status, 0) + 1
            totals[status] = totals.get(status, 0) + 1

            if status != "skipped" and updated != original:
                html_path.write_text(updated, encoding="utf-8", newline="\n")

        summary = " ".join(f"{k}={v}" for k, v in sorted(version_counts.items()))
        print(f"{version}: {summary}")

    summary = " ".join(f"{k}={v}" for k, v in sorted(totals.items()))
    print(f"TOTAL: {summary}")
    return 1 if totals.get("errors") else 0


if __name__ == "__main__":
    raise SystemExit(main())
