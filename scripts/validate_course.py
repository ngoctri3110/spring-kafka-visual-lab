#!/usr/bin/env python3
"""Validate the static Kafka Visual Lab before publishing."""

from __future__ import annotations

import html.parser
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
LESSONS = DOCS / "visual-guides" / "html"
EXPECTED = [
    "kafka-visual-lab-module-01-02.html",
    "kafka-visual-lab-module-03-consumer-group.html",
    "kafka-visual-lab-module-04-producer-reliability.html",
    "kafka-visual-lab-module-05-partition-key-ordering.html",
    "kafka-visual-lab-module-06-serialization-schema-evolution.html",
    "kafka-visual-lab-module-07-consumer-offset-commit.html",
    "kafka-visual-lab-module-08-retry-backoff-dlt.html",
    "kafka-visual-lab-module-09-kafka-transactions-eos.html",
    "kafka-visual-lab-module-10-outbox-idempotent-consumer.html",
    "kafka-visual-lab-module-11-testing-spring-kafka.html",
    "kafka-visual-lab-module-12-observability-performance-tuning.html",
    "kafka-visual-lab-module-13-capstone-order-platform.html",
]
FORBIDDEN = (
    "notebook.google.com",
    "notebooklm",
    "74f0faf5-ec3d-480c-aa12-52cdf9fa9e89",
)
SKIP_SCHEMES = {"http", "https", "mailto", "tel", "javascript", "data"}


class PageParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.links: list[tuple[str, str]] = []
        self.home_link = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"] or "")
        for attr in ("href", "src"):
            if values.get(attr):
                self.links.append((attr, values[attr] or ""))
        classes = set((values.get("class") or "").split())
        if tag == "a" and "course-home" in classes and values.get("href") == "../../index.html":
            self.home_link = True


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def main() -> int:
    errors: list[str] = []
    if not (DOCS / "index.html").is_file():
        errors.append("missing docs/index.html")
    if not (DOCS / ".nojekyll").is_file():
        errors.append("missing docs/.nojekyll")
    for name in EXPECTED:
        if not (LESSONS / name).is_file():
            errors.append(f"missing lesson: {name}")

    html_files = sorted(DOCS.rglob("*.html")) if DOCS.is_dir() else []
    for path in html_files:
        rel = path.relative_to(ROOT)
        raw = path.read_text(encoding="utf-8")
        lowered = raw.lower()
        for token in FORBIDDEN:
            if token in lowered:
                errors.append(f"{rel}: forbidden private-source token: {token}")

        parser = parse_page(path)
        duplicates = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
        for duplicate in duplicates:
            errors.append(f"{rel}: duplicate id #{duplicate}")

        if path.parent == LESSONS and path.name in EXPECTED and not parser.home_link:
            errors.append(f"{rel}: missing course-home link to ../../index.html")

        known_ids = set(parser.ids)
        for attr, raw_target in parser.links:
            target = raw_target.strip()
            parsed = urlsplit(target)
            if parsed.scheme.lower() in SKIP_SCHEMES or target.startswith("//"):
                continue
            if not parsed.path:
                if parsed.fragment and unquote(parsed.fragment) not in known_ids:
                    errors.append(f"{rel}: missing fragment target #{parsed.fragment}")
                continue
            local_path = (path.parent / unquote(parsed.path)).resolve()
            try:
                local_path.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"{rel}: {attr} escapes repository: {target}")
                continue
            if not local_path.exists():
                errors.append(f"{rel}: broken local {attr}: {target}")
                continue
            if parsed.fragment and local_path.suffix.lower() == ".html":
                target_ids = set(parse_page(local_path).ids)
                if unquote(parsed.fragment) not in target_ids:
                    errors.append(f"{rel}: missing target {target}")

    if len(html_files) != len(EXPECTED) + 1:
        errors.append(f"expected {len(EXPECTED) + 1} HTML pages, found {len(html_files)}")

    if errors:
        print("COURSE VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("COURSE VALIDATION PASSED")
    print(f"- HTML pages: {len(html_files)}")
    print(f"- Lesson pages: {len(EXPECTED)}")
    print("- Internal links, fragments, IDs and public-source rules: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
