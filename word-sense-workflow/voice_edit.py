#!/usr/bin/env python3
"""Run the independent Word Sense voice-editing stage."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

from run import BASE_DIR, DEFAULT_OUTPUT_DIR, DEFAULT_REWRITE_MODEL, OpenAI, load_dotenv, load_prompt, response_text, safe_word_dir


def extract_verified(markdown: str) -> tuple[str, str]:
    text = re.sub(r"^#\s*改写终稿\s*", "", markdown.strip(), count=1).strip()
    parts = re.split(r"\n---\s*\n#\s*改动说明\s*", text, maxsplit=1)
    if len(parts) == 1:
        parts = re.split(r"\n#\s*改动说明\s*", text, maxsplit=1)
    return parts[0].strip(), parts[1].strip() if len(parts) > 1 else ""


def split_voice_response(text: str) -> tuple[str, str]:
    cleaned = re.sub(r"^#\s*终稿\s*", "", text.strip(), count=1).strip()
    parts = re.split(r"\n---\s*\n#\s*声音审校记录\s*", cleaned, maxsplit=1)
    if len(parts) != 2:
        raise ValueError("声音编辑输出缺少独立的‘声音审校记录’部分")
    final, review = parts[0].strip(), parts[1].strip()
    if "改动说明" in final or "声音审校记录" in final:
        raise ValueError("用户终稿中混入了内部审校记录")
    return final, review


def edit_word(client: object, model: str, prompt: str, output_dir: Path, word: str) -> None:
    entry_dir = output_dir / safe_word_dir(word)
    verified_path = entry_dir / "step-3-final.md"
    if not verified_path.exists():
        raise FileNotFoundError(f"找不到 {verified_path}")
    verified, fact_review = extract_verified(verified_path.read_text(encoding="utf-8"))
    response = client.responses.create(
        model=model,
        max_output_tokens=6000,
        instructions=prompt,
        input=f"请审校以下关于英文词“{word}”的已查证终稿。\n\n---\n\n{verified}\n\n---\n\n严格保持事实不变，执行减法编辑，并按指定格式输出。",
    )
    final, voice_review = split_voice_response(response_text(response))
    (entry_dir / "step-4-final.md").write_text(final + "\n", encoding="utf-8")
    review_data = {"word": word, "source": "step-3-final.md", "factReview": fact_review, "voiceReview": voice_review}
    (entry_dir / "step-4-review.json").write_text(json.dumps(review_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"edited {word}: {len(verified)} -> {len(final)} chars")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Word Sense voice editing.")
    parser.add_argument("words", nargs="+", help="Words or phrases to edit")
    parser.add_argument("--force", action="store_true", help="Overwrite existing Step 4 files")
    parser.add_argument("--model", default=os.getenv("OPENAI_VOICE_MODEL", DEFAULT_REWRITE_MODEL))
    parser.add_argument("--output-dir", type=Path, default=Path(os.getenv("WORD_SENSE_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)))
    args = parser.parse_args()
    if OpenAI is None:
        raise RuntimeError("缺少依赖 openai")
    if load_dotenv is not None:
        load_dotenv(BASE_DIR / ".env")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("没有找到 OPENAI_API_KEY")
    kwargs: dict[str, str] = {"api_key": api_key}
    if os.getenv("OPENAI_BASE_URL"):
        kwargs["base_url"] = os.environ["OPENAI_BASE_URL"]
    client = OpenAI(**kwargs)
    prompt = load_prompt("v4-voice-edit")
    for word in args.words:
        final_path = args.output_dir / safe_word_dir(word) / "step-4-final.md"
        if final_path.exists() and not args.force:
            print(f"skip {word}: Step 4 already exists")
            continue
        edit_word(client, args.model, prompt, args.output_dir, word)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
