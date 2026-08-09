#!/usr/bin/env python3
"""Run the curated 18-word WordSense Issue 007 batch."""

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


ISSUE_007_WORDS = [
    {"word": "aristocratic", "surface": "贵族的；贵族气派的；高雅而疏离的", "meta": ["阶层气质 · 身份风格 · B2-C1", "Issue 007"]},
    {"word": "juxtapose", "surface": "并置；并列对照", "meta": ["视觉关系 · 对照表达 · B2-C1", "Issue 007"]},
    {"word": "wince", "surface": "畏缩；皱眉；因痛退缩", "meta": ["身体反应 · 尴尬痛感 · B2", "Issue 007"]},
    {"word": "myriad", "surface": "无数；大量；多种多样", "meta": ["数量表达 · 丰富繁多 · B2-C1", "Issue 007"]},
    {"word": "disembody", "surface": "使脱离身体；使失去实体", "meta": ["身体隐喻 · 抽象分离 · C1", "Issue 007"]},
    {"word": "propensity", "surface": "倾向；习性；偏好", "meta": ["行为倾向 · 预测判断 · C1", "Issue 007"]},
    {"word": "divinity", "surface": "神性；神；神学", "meta": ["宗教概念 · 超越属性 · C1", "Issue 007"]},
    {"word": "ensemble", "surface": "整体；合奏团；全套服装", "meta": ["整体关系 · 艺术组合 · B2-C1", "Issue 007"]},
    {"word": "perturb", "surface": "使不安；扰乱；使偏离", "meta": ["心理扰动 · 系统偏离 · C1", "Issue 007"]},
    {"word": "pasture", "surface": "牧场；草地；放牧", "meta": ["土地场景 · 放牧动作 · B2", "Issue 007"]},
    {"word": "elapse", "surface": "流逝；过去", "meta": ["时间流动 · 书面表达 · B2", "Issue 007"]},
    {"word": "ostracise", "surface": "排斥；排挤；放逐", "meta": ["群体边界 · 社会排斥 · B2-C1", "Issue 007"]},
    {"word": "taunt", "surface": "嘲弄；奚落；挑衅", "meta": ["攻击言语 · 挑衅动作 · B2", "Issue 007"]},
    {"word": "averse", "surface": "反感的；不愿意的", "meta": ["态度倾向 · 风险回避 · B2-C1", "Issue 007"]},
    {"word": "incur", "surface": "招致；承担；蒙受", "meta": ["后果成本 · 正式表达 · B2-C1", "Issue 007"]},
    {"word": "supposition", "surface": "假设；推测；设想", "meta": ["推理基础 · 未证判断 · C1", "Issue 007"]},
    {"word": "despondency", "surface": "沮丧；消沉；绝望", "meta": ["情绪低谷 · 希望流失 · C1", "Issue 007"]},
    {"word": "vicinity", "surface": "附近；邻近地区；接近", "meta": ["空间范围 · 模糊邻近 · B2-C1", "Issue 007"]},
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
    parser = argparse.ArgumentParser(description="Run Word Sense Issue 007 words.")
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
        for item in ISSUE_007_WORDS
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
