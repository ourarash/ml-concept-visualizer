#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from collections import Counter
from dataclasses import dataclass
from difflib import SequenceMatcher
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "index.html"

# This script checks repo/catalog consistency, not educational quality.
# A page can pass this check and still need content review, or fail it because
# of fixable integration issues such as a missing index entry or filename style.
FILENAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.html$")
TITLE_PATTERN = re.compile(r"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)
H1_PATTERN = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.IGNORECASE | re.DOTALL)
TAG_PATTERN = re.compile(r"<[^>]+>")
WORD_PATTERN = re.compile(r"[a-z0-9]+")
CANVAS_TAG_PATTERN = re.compile(r"<canvas\b[^>]*>", re.IGNORECASE)
CANVAS_DIMENSION_PATTERN = re.compile(r"<canvas\b[^>]*(?:width|height)\s*=\s*[\"'][0-9]+[\"'][^>]*>", re.IGNORECASE)
RESIZE_HANDLER_PATTERNS = (
    "addEventListener(\"resize\"",
    "addEventListener('resize'",
    "window.onresize",
    "ResizeObserver",
    ".onresize =",
)
DESKTOP_LAYOUT_PATTERN = re.compile(
    r"style\s*=\s*['\"][^'\"]*(?:width|min-width)\s*:\s*(?P<width>[9-9][0-9]{2,}|[1-9][0-9]{3,})px[^'\"]*(?:height|min-height)\s*:\s*(?P<height>[5-9][0-9]{2,}|[1-9][0-9]{3,})px[^'\"]*['\"]",
    re.IGNORECASE,
)
STOPWORDS = {
    "a",
    "an",
    "and",
    "by",
    "for",
    "in",
    "of",
    "on",
    "the",
    "to",
    "visualization",
    "visualizer",
    "interactive",
    "explorer",
    "simulator",
    "overview",
    "lab",
    "guide",
}


@dataclass(frozen=True)
class CatalogEntry:
    href: str
    title: str
    description: str


class CatalogParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.entries: list[CatalogEntry] = []
        self._current_href: str | None = None
        self._text_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return

        attr_map = {key: value or "" for key, value in attrs}
        classes = set(attr_map.get("class", "").split())
        if "viz-link" not in classes:
            return

        self._current_href = attr_map.get("href", "")
        self._text_parts = []

    def handle_data(self, data: str) -> None:
        if self._current_href is None:
            return

        text = " ".join(data.split())
        if text:
            self._text_parts.append(text)

    def handle_endtag(self, tag: str) -> None:
        if tag != "a" or self._current_href is None:
            return

        title = self._text_parts[0] if self._text_parts else ""
        description = " ".join(self._text_parts[1:]).strip()
        self.entries.append(
            CatalogEntry(
                href=self._current_href,
                title=title,
                description=description,
            )
        )
        self._current_href = None
        self._text_parts = []


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def strip_tags(text: str) -> str:
    text = text.replace("&amp;", "and")
    text = TAG_PATTERN.sub(" ", text)
    return " ".join(text.split())


def extract_title(text: str) -> str:
    match = TITLE_PATTERN.search(text)
    return strip_tags(match.group(1)) if match else ""


def extract_h1(text: str) -> str:
    match = H1_PATTERN.search(text)
    return strip_tags(match.group(1)) if match else ""


def is_redirect_stub(text: str) -> bool:
    return "<!-- redirect-stub -->" in text


def normalize_text(text: str) -> str:
    words = WORD_PATTERN.findall(text.lower())
    return " ".join(words)


def meaningful_tokens(text: str) -> set[str]:
    return {word for word in WORD_PATTERN.findall(text.lower()) if word not in STOPWORDS}


def is_metadata_divergent(label: str, other: str) -> bool:
    """Return True when catalog text and page metadata appear unrelated."""
    if not label or not other:
        return True

    label_norm = normalize_text(label)
    other_norm = normalize_text(other)
    if not label_norm or not other_norm:
        return True

    if label_norm in other_norm or other_norm in label_norm:
        return False

    ratio = SequenceMatcher(None, label_norm, other_norm).ratio()
    overlap = meaningful_tokens(label) & meaningful_tokens(other)
    return ratio < 0.55 and not overlap


def local_href(href: str) -> bool:
    parts = urlsplit(href)
    return not parts.scheme and not parts.netloc and not href.startswith("#")


def collect_catalog_entries(index_text: str) -> list[CatalogEntry]:
    # The catalog is the set of local <a class="viz-link"> entries in index.html.
    # External links and hash-only anchors are ignored because they are not repo pages.
    parser = CatalogParser()
    parser.feed(index_text)
    return [entry for entry in parser.entries if local_href(entry.href)]


def has_fixed_canvas_dimensions(text: str) -> bool:
    return CANVAS_DIMENSION_PATTERN.search(text) is not None


def has_resize_handler(text: str) -> bool:
    lowered = text.lower()
    return any(pattern.lower() in lowered for pattern in RESIZE_HANDLER_PATTERNS)


def has_fixed_desktop_layout(text: str) -> bool:
    return DESKTOP_LAYOUT_PATTERN.search(text) is not None


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    index_text = load_text(INDEX_PATH)
    catalog_entries = collect_catalog_entries(index_text)
    catalog_by_href = {entry.href: entry for entry in catalog_entries}

    # Catalog entries should be unique. Duplicate hrefs are errors because they
    # make the landing page ambiguous; duplicate titles are warnings because two
    # related visualizations may legitimately use similar names.
    href_counts = Counter(entry.href for entry in catalog_entries)
    for href, count in sorted(href_counts.items()):
        if count > 1:
            errors.append(f"Duplicate index entry: {href} appears {count} times")

    title_counts = Counter(entry.title for entry in catalog_entries if entry.title)
    for title, count in sorted(title_counts.items()):
        if count > 1:
            warnings.append(f"Duplicate catalog title: '{title}' appears {count} times")

    for entry in sorted(catalog_entries, key=lambda item: item.href):
        target = ROOT / entry.href
        if not target.exists():
            errors.append(f"Broken index link: {entry.href}")
            continue

        # Redirect stubs preserve old URLs, but the public catalog should point
        # directly to the canonical visualization page.
        target_text = load_text(target)
        if is_redirect_stub(target_text):
            errors.append(f"Catalog points to redirect stub instead of canonical page: {entry.href}")

        if not entry.description:
            warnings.append(f"Missing catalog description: {entry.href}")

    html_files = sorted(path for path in ROOT.rglob("*.html") if ".git" not in path.parts)

    for path in html_files:
        rel_path = path.relative_to(ROOT).as_posix()
        if rel_path == "index.html":
            continue

        text = load_text(path)
        redirect_stub = is_redirect_stub(text)

        # Kebab-case filenames keep URLs predictable and match the existing
        # visualization naming convention, e.g. "flash-attention.html".
        if not redirect_stub and not FILENAME_PATTERN.match(path.name):
            errors.append(f"Non-kebab-case filename: {rel_path}")

        if redirect_stub:
            continue

        # Every real visualization page should be discoverable from index.html.
        # This is the most common failure for student PRs that add a standalone
        # HTML file but do not add it to the catalog.
        if rel_path not in catalog_by_href:
            errors.append(f"Page missing from index catalog: {rel_path}")

        title = extract_title(text)
        h1 = extract_h1(text)
        entry = catalog_by_href.get(rel_path)

        if not title:
            warnings.append(f"Missing title: {rel_path}")
        if not h1:
            warnings.append(f"Missing H1: {rel_path}")

        # The catalog label, <title>, and <h1> do not need to be identical, but
        # they should describe the same visualization so browser tabs, search,
        # and the landing page do not drift apart.
        if entry and title and is_metadata_divergent(entry.title, title):
            warnings.append(
                f"Catalog/title drift: {rel_path} | catalog='{entry.title}' | title='{title}'"
            )
        if entry and h1 and is_metadata_divergent(entry.title, h1):
            warnings.append(
                f"Catalog/H1 drift: {rel_path} | catalog='{entry.title}' | h1='{h1}'"
            )

        # Canvas pages with hard-coded dimensions often look broken on phones
        # unless the script also resizes or redraws them.
        if CANVAS_TAG_PATTERN.search(text) and has_fixed_canvas_dimensions(text) and not has_resize_handler(text):
            warnings.append(f"Canvas page may be missing resize handling: {rel_path}")

        # Flag obvious desktop-only inline layouts. This is intentionally a
        # heuristic warning, not an error, because visual pages vary a lot.
        if has_fixed_desktop_layout(text):
            warnings.append(f"Page may use a fixed desktop-only layout: {rel_path}")

    if errors:
        print("Consistency check failed:\n")
        for error in errors:
            print(f"ERROR: {error}")
        if warnings:
            print("\nWarnings:")
            for warning in warnings:
                print(f"WARN: {warning}")
        return 1

    print("Consistency check passed.")
    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"WARN: {warning}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
