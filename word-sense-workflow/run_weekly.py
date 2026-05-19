#!/usr/bin/env python3
"""Run the curated 18-word weekly WordSense batch."""

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


WEEKLY_WORDS = [
    {
        "word": "resilience",
        "meta": ["心理成长 · A2-B1 · 入门", "本周精选"],
    },
    {
        "word": "unfold",
        "meta": ["新闻叙事 · A2-B1 · 入门", "本周精选"],
    },
    {
        "word": "brace",
        "meta": ["新闻生活 · A2-B1 · 入门", "本周精选"],
    },
    {
        "word": "surge",
        "meta": ["新闻数据 · A2-B1 · 入门", "本周精选"],
    },
    {
        "word": "verify",
        "meta": ["AI 信息 · A2-B1 · 入门", "本周精选"],
    },
    {
        "word": "cringe",
        "meta": ["社媒口语 · A2-B1 · 入门", "本周精选"],
    },
    {
        "word": "probe",
        "meta": ["新闻调查 · B1-B2 · 进阶", "本周精选"],
    },
    {
        "word": "fallout",
        "meta": ["新闻政治 · B1-B2 · 进阶", "本周精选"],
    },
    {
        "word": "hallucination",
        "meta": ["AI 语境 · B1-B2 · 进阶", "本周精选"],
    },
    {
        "word": "grounding",
        "meta": ["AI 信息 · B1-B2 · 进阶", "本周精选"],
    },
    {
        "word": "delulu",
        "meta": ["社媒口语 · B1-B2 · 进阶", "本周精选"],
    },
    {
        "word": "brain rot",
        "meta": ["社媒文化 · B1-B2 · 进阶", "本周精选"],
    },
    {
        "word": "deprecate",
        "displayWord": "Deprecate",
        "meta": ["技术文档 · B2-C1 · 高阶", "本周精选"],
    },
    {
        "word": "orchestrate",
        "meta": ["AI 系统 · B2-C1 · 高阶", "本周精选"],
    },
    {
        "word": "inflection point",
        "meta": ["商业趋势 · B2-C1 · 高阶", "本周精选"],
    },
    {
        "word": "accountability gap",
        "meta": ["AI 治理 · B2-C1 · 高阶", "本周精选"],
    },
    {
        "word": "clanker",
        "displayWord": "Clanker",
        "meta": ["AI 俚语 · B2-C1 · 高阶", "本周精选"],
    },
    {
        "word": "unhinged",
        "meta": ["社媒评价 · B2-C1 · 高阶", "本周精选"],
    },
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
    parser = argparse.ArgumentParser(description="Run the curated weekly words.")
    parser.add_argument("--force", action="store_true", help="重新生成已有词条")
    parser.add_argument(
        "--only",
        nargs="*",
        default=[],
        help="只运行指定词，默认运行缺失的本周 18 词",
    )
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
        for item in WEEKLY_WORDS
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
