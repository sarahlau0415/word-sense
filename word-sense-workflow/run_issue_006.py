#!/usr/bin/env python3
"""Run the curated 19-word WordSense Issue 006 batch."""

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


ISSUE_006_WORDS = [
    {"word": "gimmick", "meta": ["营销表达 · 吸睛手法 · B2", "Issue 006"]},
    {"word": "gross", "meta": ["感官评价 · 数量总额 · B1-B2", "Issue 006"]},
    {"word": "royalty", "meta": ["王室身份 · 版权收入 · B2", "Issue 006"]},
    {"word": "cannibalize", "meta": ["商业竞争 · 自我蚕食 · B2-C1", "Issue 006"]},
    {"word": "tap into", "meta": ["资源调用 · 潜力利用 · B1-B2", "Issue 006"]},
    {"word": "feature", "meta": ["产品特性 · 重点呈现 · B1-B2", "Issue 006"]},
    {"word": "guerrilla", "meta": ["游击策略 · 非常规行动 · B2", "Issue 006"]},
    {"word": "epitome", "meta": ["典型代表 · 高度概括 · C1", "Issue 006"]},
    {"word": "maiden", "meta": ["首次亮相 · 历史用语 · B2-C1", "Issue 006"]},
    {"word": "blunt", "meta": ["直接表达 · 钝化触感 · B1-B2", "Issue 006"]},
    {"word": "flex", "meta": ["弯曲动作 · 展示实力 · B1-B2", "Issue 006"]},
    {"word": "obliterate", "meta": ["彻底摧毁 · 抹除痕迹 · C1", "Issue 006"]},
    {"word": "derogatory", "meta": ["贬损表达 · 语用边界 · C1", "Issue 006"]},
    {"word": "streak", "meta": ["连续纪录 · 条纹痕迹 · B2", "Issue 006"]},
    {"word": "tender", "meta": ["温柔触感 · 正式投标 · B1-B2", "Issue 006"]},
    {"word": "pledge", "meta": ["郑重承诺 · 抵押捐赠 · B2", "Issue 006"]},
    {"word": "demeanor", "meta": ["外在举止 · 人际观感 · C1", "Issue 006"]},
    {"word": "spiral", "meta": ["螺旋轨迹 · 连锁恶化 · B2", "Issue 006"]},
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
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Word Sense Issue 006 words.")
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
        for item in ISSUE_006_WORDS
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
