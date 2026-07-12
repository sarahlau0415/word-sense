#!/usr/bin/env python3
"""Build the static front-end content bundle from workflow outputs."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = Path(__file__).resolve().parent / "output"
CONTENT_JS = ROOT / "word-sense-content.js"

ENTRY_META = {
    "lowkey": {"displayWord": "lowkey", "meta": ["社媒 · L2", "本周词条"]},
    "agentic": {"displayWord": "agentic", "meta": ["AI · L3", "本周词条"]},
    "reframe": {"displayWord": "reframe", "meta": ["学术 · L3", "本周词条"]},
    "sentiment": {"displayWord": "sentiment", "meta": ["新闻 · L2", "本周词条"]},
    "backdrop": {"displayWord": "backdrop", "meta": ["新闻 · L2", "本周词条"]},
    "it's giving": {
        "displayWord": "it's giving",
        "meta": ["社媒 · L2", "本周词条"],
        "dir": "it-s-giving",
    },
}


def extract_final(markdown: str) -> str:
    markdown = markdown.strip()
    if markdown.startswith("# 改写终稿"):
        markdown = markdown.split("\n", 1)[1].strip()
    if "\n---\n\n# 改动说明" in markdown:
        markdown = markdown.split("\n---\n\n# 改动说明", 1)[0].strip()
    elif "\n# 改动说明" in markdown:
        markdown = markdown.split("\n# 改动说明", 1)[0].strip()
    return markdown.strip()


def section(text: str, heading: str) -> str:
    pattern = rf"## {re.escape(heading)}\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, text, flags=re.S)
    return match.group(1).strip() if match else ""


def count_claims(research: str) -> int:
    facts = section(research, "待查事实清单")
    return len(re.findall(r"^\d+\.", facts, flags=re.M))


def count_result_items(research: str, heading: str) -> int:
    pattern = rf"### {re.escape(heading)}[^\n]*\n(.*?)(?=\n### |\n## |\Z)"
    match = re.search(pattern, research, flags=re.S)
    if not match:
        return 0
    return len(re.findall(r"^- \*\*", match.group(1), flags=re.M))


def extract_checked_topics(research: str) -> list[str]:
    process = section(research, "查证过程")
    candidates: list[str] = []

    for line in process.splitlines():
        stripped = line.strip()
        if stripped.startswith("- ") and not re.search(r"https?://", stripped):
            item = re.sub(r"^- ", "", stripped)
            item = item.rstrip("；;。")
            if item and len(item) <= 45:
                candidates.append(item)

    if candidates:
        return candidates[:5]

    # Fallback: use fact list snippets when the process section has no compact bullets.
    facts = section(research, "待查事实清单")
    for line in facts.splitlines():
        stripped = re.sub(r"^\d+\.\s*", "", line.strip()).strip("“”")
        if stripped:
            candidates.append(stripped[:42] + ("…" if len(stripped) > 42 else ""))
    return candidates[:5]


def clean_url(url: str) -> str:
    return url.rstrip(").,，。；;")


def normalize_display_word(word: str) -> str:
    raw = str(word or "").strip()
    if not raw:
        return raw
    fixed_forms = {"AI", "API", "US", "UK", "Gen Z", "TikTok", "Instagram", "Slack", "X"}
    if raw in fixed_forms:
        return raw
    if re.match(r"^[A-Z]{2,}(?:[-\s][A-Z0-9]{2,})*$", raw):
        return raw
    if re.search(r"\b(?:AI|API|Gen Z|TikTok|Instagram|Slack|X)\b", raw):
        return raw
    return raw.lower()


def extract_sources(research: str) -> list[dict[str, str]]:
    visible_sources = section(research, "用户可见来源")
    if visible_sources:
        parsed_sources: list[dict[str, str]] = []
        for line in visible_sources.splitlines():
            match = re.match(r"^-\s*(.*?):\s*(https?://\S+)", line.strip())
            if not match:
                continue
            label = match.group(1).strip("[] ")
            url = clean_url(match.group(2))
            if url and all(source["url"] != url for source in parsed_sources):
                parsed_sources.append({"label": label, "url": url})
        if parsed_sources:
            return parsed_sources[:8]

    urls: list[str] = []
    for url in re.findall(r"https?://[^\s\])）>]+", research):
        cleaned = clean_url(url)
        if cleaned not in urls:
            urls.append(cleaned)

    sources = []
    for url in urls[:8]:
        host = urlparse(url).netloc.replace("www.", "")
        sources.append({"label": host, "url": url})
    return sources


def build_verification(research: str) -> dict[str, object]:
    return {
        "claimCount": count_claims(research),
        "confirmedCount": count_result_items(research, "✅ 证实"),
        "softenedCount": count_result_items(research, "⚠️ 部分证实"),
        "uncertainCount": count_result_items(research, "❓ 无法确认"),
        "rejectedCount": count_result_items(research, "❌ 证伪"),
        "checked": extract_checked_topics(research),
        "sources": extract_sources(research),
    }


def discover_entries() -> dict[str, dict[str, object]]:
    entries: dict[str, dict[str, object]] = {}

    for key, meta in ENTRY_META.items():
        entries[key] = dict(meta)

    for entry_dir in sorted(OUTPUT_DIR.iterdir()):
        if not entry_dir.is_dir():
            continue
        if not (entry_dir / "step-3-final.md").exists():
            continue
        if not (entry_dir / "step-2-research.md").exists():
            continue

        meta_path = entry_dir / "entry-meta.json"
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                meta = {}
            key = str(meta.get("key") or entry_dir.name).strip().lower()
            entries[key] = {
                "displayWord": normalize_display_word(meta.get("displayWord") or key),
                "meta": meta.get("meta") or ["用户搜索", "WordSense"],
                "dir": entry_dir.name,
            }
            if meta.get("surface"):
                entries[key]["surface"] = str(meta["surface"]).strip()

    return entries


def main() -> None:
    content: dict[str, object] = {}
    entries = discover_entries()

    for key, meta in entries.items():
        dirname = meta.get("dir", key)
        entry_dir = OUTPUT_DIR / dirname
        final_path = entry_dir / "step-3-final.md"
        research_path = entry_dir / "step-2-research.md"
        if not final_path.exists() or not research_path.exists():
            continue

        markdown = extract_final(final_path.read_text(encoding="utf-8"))
        research = research_path.read_text(encoding="utf-8")
        content[key] = {
            "displayWord": normalize_display_word(meta["displayWord"]),
            "meta": meta["meta"],
            "markdown": markdown,
            "verification": build_verification(research),
        }
        if meta.get("surface"):
            content[key]["surface"] = meta["surface"]

    bundle = "window.WORD_SENSE_ENTRIES = "
    bundle += json.dumps(content, ensure_ascii=False, indent=2)
    bundle += ";\n"
    CONTENT_JS.write_text(bundle, encoding="utf-8")
    print(f"wrote {CONTENT_JS} with {len(content)} entries")


if __name__ == "__main__":
    main()
