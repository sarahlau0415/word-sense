#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit the built Word Sense content bundle before publishing an issue."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT_JS = ROOT / "word-sense-content.js"
REQUIRED_HEADINGS = ["字面含义", "本体质感", "寻根溯源", "各路用法", "悟道时刻"]
PLACEHOLDERS = [
    "正在查找这个用法从哪里长出来。",
    "正在审校",
    "TODO",
    "待补充",
]


def load_entries(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"window\.WORD_SENSE_ENTRIES\s*=\s*(\{.*\})\s*;\s*$", text, re.S)
    if not match:
        raise SystemExit(f"Cannot find WORD_SENSE_ENTRIES in {path}")
    return json.loads(match.group(1))


def audit(entries: dict, issue: str | None, expected_count: int | None = None) -> list[str]:
    errors: list[str] = []
    checked = 0
    heading_pattern = re.compile(r"\*\*([^*]+?)\*\*\s*·")

    for key, entry in entries.items():
        meta = entry.get("meta", [])
        if issue and not any(issue in item for item in meta):
            continue
        checked += 1
        markdown = entry.get("markdown", "")
        surface = str(entry.get("surface") or "").strip()
        issue_numbers = [
            int(match.group(1))
            for item in meta
            if (match := re.fullmatch(r"Issue (\d{3})", str(item)))
        ]
        requires_surface = any(number >= 6 for number in issue_numbers)
        if requires_surface:
            if not surface:
                errors.append(f"{key}: missing surface summary")
            elif len(surface) > 40:
                errors.append(f"{key}: surface summary is too long ({len(surface)} chars)")
        headings = [m.group(1).strip() for m in heading_pattern.finditer(markdown)]
        missing = [heading for heading in REQUIRED_HEADINGS if heading not in headings]
        if missing:
            errors.append(f"{key}: missing headings: {', '.join(missing)}")

        for placeholder in PLACEHOLDERS:
            if placeholder in markdown:
                errors.append(f"{key}: contains placeholder text: {placeholder}")

        sources = entry.get("verification", {}).get("sources", [])
        if not sources:
            errors.append(f"{key}: missing verification.sources")

    if checked == 0:
        errors.append(f"No entries matched issue filter: {issue}")
    if expected_count is not None and checked != expected_count:
        errors.append(f"Expected {expected_count} entries, found {checked}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit built Word Sense content.")
    parser.add_argument("--issue", help="Only audit entries whose meta contains this issue label, e.g. 'Issue 003'.")
    parser.add_argument("--expected-count", type=int, help="Fail unless the filtered issue contains exactly this many entries.")
    parser.add_argument("--content", type=Path, default=CONTENT_JS, help="Path to word-sense-content.js")
    args = parser.parse_args()

    entries = load_entries(args.content)
    errors = audit(entries, args.issue, args.expected_count)
    if errors:
        print("Content audit failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    scope = args.issue or "all entries"
    print(f"Content audit passed for {scope}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
