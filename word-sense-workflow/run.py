#!/usr/bin/env python3
"""Run the three-step Word Sense content workflow."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - exercised only before dependencies install
    OpenAI = None  # type: ignore[assignment]

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - exercised only before dependencies install
    load_dotenv = None  # type: ignore[assignment]


BASE_DIR = Path(__file__).resolve().parent
PROMPTS_DIR = BASE_DIR / "prompts"
DEFAULT_OUTPUT_DIR = BASE_DIR / "output"

DEFAULT_WRITE_MODEL = "openai/gpt-5.4-mini"
DEFAULT_RESEARCH_MODEL = "openai/gpt-5.4"
DEFAULT_REWRITE_MODEL = "openai/gpt-5.4"


def load_prompt(name: str) -> str:
    """Load only the prompt body from prompts/[name].md."""
    path = PROMPTS_DIR / f"{name}.md"
    content = path.read_text(encoding="utf-8")

    marker = "## PROMPT 内容"
    if marker not in content:
        return content.strip()

    after_marker = content.split(marker, 1)[1]
    if "---" not in after_marker:
        return after_marker.strip()

    return after_marker.split("---", 1)[1].strip()


def response_text(response: object) -> str:
    """Extract text from an OpenAI Responses API response."""
    output_text = getattr(response, "output_text", None)
    if output_text:
        return str(output_text).strip()
    return str(response).strip()


def safe_word_dir(word: str) -> str:
    """Make a readable output directory name for a word or phrase."""
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", word.strip()).strip("-._")
    return safe or "word"


def build_step_1_user_message(word: str, source: str = "", sentence: str = "") -> str:
    lines = [f"词:{word}"]
    if source:
        lines.append(f"出处:{source}")
    if sentence:
        lines.append(f"原句:{sentence}")
    return "\n".join(lines)


def build_step_2_user_message(word: str, draft: str) -> str:
    return f"""请查证以下这篇关于英文词 "{word}" 的解读初稿。

---

{draft}

---

按你的工作流执行,输出查证报告。
"""


def build_step_3_user_message(word: str, draft: str, research_report: str) -> str:
    return f"""请改写以下关于英文词 "{word}" 的解读初稿。

# Step 1 初稿

---

{draft}

---

# Step 2 查证报告

---

{research_report}

---

按你的工作流执行,输出改写后的终稿 + 改动说明。
"""


class WordSenseWorkflow:
    def __init__(
        self,
        *,
        write_model: str,
        research_model: str,
        rewrite_model: str,
        output_dir: Path,
        search_context_size: str,
        api_key: str | None = None,
        base_url: str | None = None,
    ) -> None:
        if OpenAI is None:
            raise RuntimeError(
                "缺少依赖 openai。请先运行: pip install -r requirements.txt"
            )

        if load_dotenv is not None:
            load_dotenv(BASE_DIR / ".env")

        resolved_api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not resolved_api_key:
            raise RuntimeError(
                "没有找到 OPENAI_API_KEY。请在环境变量或 word-sense-workflow/.env 里配置。"
            )

        client_kwargs: dict[str, str] = {}
        client_kwargs["api_key"] = resolved_api_key
        resolved_base_url = base_url or os.getenv("OPENAI_BASE_URL")
        if resolved_base_url:
            client_kwargs["base_url"] = resolved_base_url

        self.client = OpenAI(**client_kwargs)
        self.write_model = write_model
        self.research_model = research_model
        self.rewrite_model = rewrite_model
        self.output_dir = output_dir
        self.search_context_size = search_context_size
        self.write_prompt = load_prompt("v3-write")
        self.research_prompt = load_prompt("v3-research")
        self.rewrite_prompt = load_prompt("v3-rewrite")

    def step_1_write(self, word: str, source: str = "", sentence: str = "") -> str:
        response = self.client.responses.create(
            model=self.write_model,
            max_output_tokens=4000,
            instructions=self.write_prompt,
            input=build_step_1_user_message(word, source, sentence),
        )
        return response_text(response)

    def step_2_research(self, word: str, draft: str) -> str:
        response = self.client.responses.create(
            model=self.research_model,
            max_output_tokens=8000,
            instructions=self.research_prompt,
            tools=[
                {
                    "type": "web_search",
                    "search_context_size": self.search_context_size,
                }
            ],
            tool_choice="auto",
            input=build_step_2_user_message(word, draft),
        )
        return response_text(response)

    def step_3_rewrite(self, word: str, draft: str, research_report: str) -> str:
        response = self.client.responses.create(
            model=self.rewrite_model,
            max_output_tokens=6000,
            instructions=self.rewrite_prompt,
            input=build_step_3_user_message(word, draft, research_report),
        )
        return response_text(response)

    def run(self, word: str, source: str = "", sentence: str = "") -> Path:
        word_output_dir = self.output_dir / safe_word_dir(word)
        word_output_dir.mkdir(parents=True, exist_ok=True)

        print(f"=== Step 1: 写作 {word!r} ===")
        draft = self.step_1_write(word, source, sentence)
        draft_path = word_output_dir / "step-1-draft.md"
        draft_path.write_text(draft, encoding="utf-8")
        print(f"  保存到 {draft_path}")
        print(f"  长度:{len(draft)} 字符")

        print("\n=== Step 2: 查证 ===")
        research = self.step_2_research(word, draft)
        research_path = word_output_dir / "step-2-research.md"
        research_path.write_text(research, encoding="utf-8")
        print(f"  保存到 {research_path}")
        print(f"  长度:{len(research)} 字符")

        print("\n=== Step 3: 改写 ===")
        final = self.step_3_rewrite(word, draft, research)
        final_path = word_output_dir / "step-3-final.md"
        final_path.write_text(final, encoding="utf-8")
        print(f"  保存到 {final_path}")
        print(f"  长度:{len(final)} 字符")

        print(f"\n完成。三份文件都在 {word_output_dir}")
        return word_output_dir


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the Word Sense three-step content workflow."
    )
    parser.add_argument("word", nargs="?", help="要生成内容的英文词")
    parser.add_argument("--source", default="", help="可选:词的出处")
    parser.add_argument("--sentence", default="", help="可选:词所在原句")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(os.getenv("WORD_SENSE_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)),
        help="输出目录,默认 word-sense-workflow/output",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("OPENAI_MODEL", DEFAULT_WRITE_MODEL),
        help="默认模型,未单独指定时用于 Step 1",
    )
    parser.add_argument(
        "--research-model",
        default=os.getenv("OPENAI_RESEARCH_MODEL", DEFAULT_RESEARCH_MODEL),
        help="Step 2 查证模型",
    )
    parser.add_argument(
        "--rewrite-model",
        default=os.getenv("OPENAI_REWRITE_MODEL", DEFAULT_REWRITE_MODEL),
        help="Step 3 改写模型",
    )
    parser.add_argument(
        "--search-context-size",
        choices=["low", "medium", "high"],
        default=os.getenv("OPENAI_SEARCH_CONTEXT_SIZE", "medium"),
        help="Step 2 web_search 使用的搜索上下文大小",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只检查 prompt 和输出路径,不调用 API",
    )
    return parser.parse_args(argv)


def dry_run(args: argparse.Namespace) -> None:
    prompts = {
        "v3-write": load_prompt("v3-write"),
        "v3-research": load_prompt("v3-research"),
        "v3-rewrite": load_prompt("v3-rewrite"),
    }
    output_path = args.output_dir / safe_word_dir(args.word or "example")

    print("Dry run OK.")
    print(f"  word: {args.word or '(未提供)'}")
    print(f"  output: {output_path}")
    for name, prompt in prompts.items():
        first_line = prompt.splitlines()[0] if prompt else ""
        print(f"  {name}: {len(prompt)} 字符, first line: {first_line}")


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.dry_run:
        dry_run(args)
        return 0

    if not args.word:
        print("错误:请提供一个英文词。用法: python run.py <word>", file=sys.stderr)
        return 2

    try:
        workflow = WordSenseWorkflow(
            write_model=args.model,
            research_model=args.research_model,
            rewrite_model=args.rewrite_model,
            output_dir=args.output_dir,
            search_context_size=args.search_context_size,
        )
        workflow.run(args.word, args.source, args.sentence)
    except Exception as exc:
        print(f"\n工作流停止:{exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
