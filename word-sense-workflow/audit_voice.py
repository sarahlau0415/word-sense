#!/usr/bin/env python3
"""Audit visible Word Sense copy for templated AI-writing patterns."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

from audit_content import CONTENT_JS, load_entries


HARD_PATTERNS = {
    "internal review text": re.compile(r"改动说明|声音审校记录|查证报告|软化\s*\d+|整合\s*\d+"),
    "native-speaker mind claim": re.compile(r"(?:英语)?母语者.{0,16}(?:脑子里|心里|会自然想到|第一反应)"),
    "ASCII comma between Chinese text": re.compile(r"[\u4e00-\u9fff],[\u4e00-\u9fff]"),
    "unnecessary English register adjective": re.compile(r"\b(?:dramatic|plain|formal|everyday)\b(?=\s*的|\s*语境)"),
}

SOFT_PATTERNS = {
    "不是": (re.compile(r"不是"), 5),
    "而是": (re.compile(r"而是"), 4),
    "不只是": (re.compile(r"不只是"), 3),
    "更像": (re.compile(r"更像"), 4),
    "真正要记住/值得": (re.compile(r"真正(?:要记住|值得|抓住|有意思|好用)"), 1),
    "以后再遇到": (re.compile(r"以后再(?:遇到|见到)|下次(?:看到|遇到)"), 1),
}


def audit(entries: dict, issue: str | None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    endings: Counter[str] = Counter()
    checked = 0
    for key, entry in entries.items():
        if issue and issue not in entry.get("meta", []):
            continue
        checked += 1
        markdown = str(entry.get("markdown") or "")
        # Usage notes often need explicit A/B contrasts to teach sense boundaries.
        # Measure template density on the editorial spine instead of penalizing
        # every necessary contrast beneath an example.
        editorial_markdown = re.sub(
            r"\*\*各路用法\*\*\s*·[\s\S]*?(?=\*\*(?:原生思维|英汉分野|悟道时刻)\*\*\s*·)",
            "",
            markdown,
        )
        for label, pattern in HARD_PATTERNS.items():
            count = len(pattern.findall(markdown))
            if count:
                errors.append(f"{key}: {label} ({count})")
        for label, (pattern, limit) in SOFT_PATTERNS.items():
            count = len(pattern.findall(editorial_markdown))
            if count > limit:
                warnings.append(f"{key}: {label} appears {count} times (limit {limit})")
        insight = re.search(r"\*\*悟道时刻\*\*\s*·\s*(.+)", markdown, re.S)
        if insight:
            first_sentence = re.split(r"[。！？\n]", insight.group(1).strip(), maxsplit=1)[0]
            signature = re.sub(r"\b[A-Za-z][A-Za-z -]*\b", "[word]", first_sentence)
            endings[signature[:48]] += 1
    if not checked:
        errors.append(f"No entries matched issue filter: {issue}")
    for signature, count in endings.items():
        if count >= 3:
            warnings.append(f"repeated insight opening across {count} entries: {signature}")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Word Sense voice quality.")
    parser.add_argument("--issue", help="Only audit one Issue NNN")
    parser.add_argument("--content", type=Path, default=CONTENT_JS)
    parser.add_argument("--strict", action="store_true", help="Treat soft warnings as failures")
    args = parser.parse_args()
    errors, warnings = audit(load_entries(args.content), args.issue)
    if warnings:
        print("Voice audit warnings:")
        for warning in warnings:
            print(f"- {warning}")
    if errors:
        print("Voice audit failed:")
        for error in errors:
            print(f"- {error}")
    if errors or (args.strict and warnings):
        return 1
    print(f"Voice audit passed for {args.issue or 'all entries'}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
