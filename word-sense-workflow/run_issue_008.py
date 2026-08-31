#!/usr/bin/env python3
"""Run the curated 16-word WordSense Issue 008 batch."""

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


ISSUE_008_WORDS = [
    {"word": "attenuate", "surface": "减弱；稀释；使变细", "meta": ["强度变化 · 正式表达 · C1", "Issue 008"]},
    {"word": "prime", "surface": "首要的；鼎盛期；预先激活", "meta": ["优先程度 · 联想启动 · B2-C1", "Issue 008"]},
    {"word": "logistics", "surface": "物流；后勤；统筹安排", "meta": ["组织运作 · 资源调度 · B2-C1", "Issue 008"]},
    {"word": "shack", "surface": "简陋小屋；棚屋", "meta": ["居住空间 · 简陋质感 · B2", "Issue 008"]},
    {"word": "clearance", "surface": "许可；清仓；净空", "meta": ["许可边界 · 空间余量 · B2-C1", "Issue 008"]},
    {"word": "groom", "surface": "梳理；培养；诱骗接近", "meta": ["照料培养 · 风险语义 · B2-C1", "Issue 008"]},
    {"word": "level", "surface": "水平；层级；坦诚相告", "meta": ["尺度层级 · 影视口语 · B1-B2", "Issue 008"]},
    {"word": "traffic", "surface": "交通；流量；非法交易", "meta": ["流动交换 · 网络指标 · B1-C1", "Issue 008"]},
    {"word": "field", "surface": "田地；领域；实地", "meta": ["空间范围 · 专业领域 · B1-B2", "Issue 008"]},
    {"word": "proposition", "surface": "主张；提议；价值命题", "meta": ["论证提案 · 商业表达 · B2-C1", "Issue 008"]},
    {"word": "crisp", "surface": "酥脆的；清晰利落的", "meta": ["感官质地 · 表达风格 · B2", "Issue 008"]},
    {"word": "crop", "surface": "作物；一批；裁剪", "meta": ["生长收成 · 图像动作 · B1-B2", "Issue 008"]},
    {"word": "prod", "surface": "戳；催促；推动", "meta": ["身体动作 · 行动催促 · B2", "Issue 008"]},
    {"word": "cherry", "surface": "樱桃；樱桃红；精选之物", "meta": ["果实意象 · 价值延伸 · B1-B2", "Issue 008"]},
    {"word": "subtract", "surface": "减去；扣除；削减", "meta": ["数量运算 · 移除减少 · B1-B2", "Issue 008"]},
    {"word": "retrieve", "surface": "取回；找回；检索", "meta": ["恢复取回 · 信息检索 · B2", "Issue 008"]},
]


def write_meta(output_dir: Path, item: dict[str, object]) -> None:
    word = str(item["word"])
    display_word = str(item.get("displayWord") or word)
    entry_dir = output_dir / safe_word_dir(word)
    entry_dir.mkdir(parents=True, exist_ok=True)
    meta = {
        "key": word.lower(),
        "displayWord": display_word,
        "surface": item.get("surface", ""),
        "meta": item["meta"],
    }
    (entry_dir / "entry-meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Word Sense Issue 008 words.")
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
        for item in ISSUE_008_WORDS
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
        voice_path = entry_dir / "step-4-final.md"
        research_path = entry_dir / "step-2-research.md"
        if final_path.exists() and voice_path.exists() and research_path.exists() and not args.force:
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
