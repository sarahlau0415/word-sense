#!/usr/bin/env python3
"""Run the curated 16-word WordSense Issue 005 batch."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import build_content_js
from run import (
    DEFAULT_OUTPUT_DIR,
    DEFAULT_RESEARCH_MODEL,
    DEFAULT_REWRITE_MODEL,
    DEFAULT_WRITE_MODEL,
    WordSenseWorkflow,
    safe_word_dir,
)


ISSUE_005_WORDS = [
    {"word": "What's cooking", "displayWord": "What's cooking", "meta": ["日常口语 · 情境寒暄 · A2-B1", "Issue 005"]},
    {"word": "Revelation", "displayWord": "revelation", "meta": ["抽象名词 · 发现时刻 · B1-B2", "Issue 005"]},
    {"word": "copy", "meta": ["内容与复制 · 基础高频 · A2-B1", "Issue 005"]},
    {"word": "stew", "meta": ["情绪与烹煮 · 画面动词 · B1-B2", "Issue 005"]},
    {"word": "fend", "meta": ["防御动作 · 短语动词 · B1-B2", "Issue 005"]},
    {"word": "cast", "meta": ["投掷与塑形 · 多义核心 · B1-B2", "Issue 005"]},
    {"word": "hygiene", "meta": ["制度与习惯 · 现代用法 · B1-B2", "Issue 005"]},
    {"word": "reference", "meta": ["指向与参照 · 学术职场 · B1-B2", "Issue 005"]},
    {"word": "float", "meta": ["漂浮与试探 · 动作隐喻 · B1-B2", "Issue 005"]},
    {"word": "fare", "meta": ["进展与费用 · 老词新读 · B1-B2", "Issue 005"]},
    {"word": "come off", "meta": ["结果与观感 · 口语短语 · B1-B2", "Issue 005"]},
    {"word": "affairs", "meta": ["公共事务 · 关系边界 · B1-B2", "Issue 005"]},
    {"word": "peg", "meta": ["固定与判断 · 具体物件 · B1-B2", "Issue 005"]},
    {"word": "legacy", "meta": ["遗留与影响 · 技术文化 · B2-C1", "Issue 005"]},
    {"word": "business", "meta": ["事情与边界 · 高频小词 · A2-B1", "Issue 005"]},
    {"word": "Sandbox", "displayWord": "sandbox", "meta": ["技术隐喻 · 安全空间 · B1-B2", "Issue 005"]},
]


def write_meta(output_dir: Path, item: dict[str, object]) -> None:
    word = str(item["word"])
    display_word = str(item.get("displayWord") or word)
    entry_dir = output_dir / safe_word_dir(word)
    entry_dir.mkdir(parents=True, exist_ok=True)
    meta = {
        "key": word.lower(),
        "displayWord": display_word,
        "meta": item["meta"],
    }
    (entry_dir / "entry-meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Word Sense Issue 005 words.")
    parser.add_argument("--force", action="store_true", help="重新生成已有词条")
    parser.add_argument("--only", nargs="*", default=[], help="只运行指定词")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(os.getenv("WORD_SENSE_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)),
    )
    parser.add_argument("--model", default=os.getenv("OPENAI_MODEL", DEFAULT_WRITE_MODEL))
    parser.add_argument(
        "--research-model",
        default=os.getenv("OPENAI_RESEARCH_MODEL", DEFAULT_RESEARCH_MODEL),
    )
    parser.add_argument(
        "--rewrite-model",
        default=os.getenv("OPENAI_REWRITE_MODEL", DEFAULT_REWRITE_MODEL),
    )
    parser.add_argument(
        "--search-context-size",
        choices=["low", "medium", "high"],
        default=os.getenv("OPENAI_SEARCH_CONTEXT_SIZE", "medium"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    requested = {word.lower() for word in args.only}
    items = [
        item
        for item in ISSUE_005_WORDS
        if not requested or str(item["word"]).lower() in requested
    ]

    workflow = WordSenseWorkflow(
        write_model=args.model,
        research_model=args.research_model,
        rewrite_model=args.rewrite_model,
        output_dir=args.output_dir,
        search_context_size=args.search_context_size,
    )

    for index, item in enumerate(items, start=1):
        word = str(item["word"])
        entry_dir = args.output_dir / safe_word_dir(word)
        final_path = entry_dir / "step-3-final.md"
        research_path = entry_dir / "step-2-research.md"

        if final_path.exists() and research_path.exists() and not args.force:
            print(f"[{index}/{len(items)}] skip {word}: already generated")
            write_meta(args.output_dir, item)
            continue

        print(f"[{index}/{len(items)}] run {word}")
        workflow.run(word)
        write_meta(args.output_dir, item)

    build_content_js.main()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
