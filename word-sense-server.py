#!/usr/bin/env python3
"""Local WordSense web server with workflow job API."""

from __future__ import annotations

import importlib.util
import json
import mimetypes
import os
import re
import sys
import threading
import time
from datetime import datetime, timezone
from difflib import SequenceMatcher
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlparse


ROOT = Path(__file__).resolve().parent
WORKFLOW_DIR = ROOT / "word-sense-workflow"
JOBS_DIR = WORKFLOW_DIR / "jobs"
RUN_PY = WORKFLOW_DIR / "run.py"
BUILD_CONTENT = WORKFLOW_DIR / "build_content_js.py"
SUBSCRIBERS_FILE = ROOT / "mailing-list.jsonl"
EVENTS_FILE = ROOT / "events.jsonl"
WORDLIST_FILE = ROOT / "word-sense-wordlist.txt"
DICTIONARY_CACHE_FILE = WORKFLOW_DIR / "dictionary-cache.json"

HOST = "127.0.0.1"
PORT = 8787

JOB_LOCK = threading.Lock()
DICTIONARY_LOCK = threading.Lock()
EVENT_LOCK = threading.Lock()
JOBS: dict[str, dict[str, object]] = {}
JOB_SECRETS: dict[str, dict[str, str]] = {}
WORDLIST: set[str] | None = None

KNOWN_PHRASES = {
    "it's giving",
    "its giving",
    "inflection point",
    "accountability gap",
    "brain rot",
    "main character energy",
    "side eye",
    "low-key",
    "high-key",
}

COMMON_SPELLING_SUGGESTIONS = {
    "dawm": ["dawn", "damn"],
    "litelly": ["literally"],
    "helo": ["hello"],
    "recieve": ["receive"],
    "langauge": ["language"],
    "definately": ["definitely"],
    "wierd": ["weird"],
}

DICTIONARY_MEANINGS = {
    "resilience": "恢复力；韧性；复原能力。",
    "unfold": "展开；逐渐显露；逐步发生。",
    "brace": "支撑；使做好准备；绷紧以应对冲击。",
    "surge": "激增；猛涨；涌动。",
    "verify": "核实；查证；确认。",
    "cringe": "畏缩；尴尬得不适；感到难为情。",
    "probe": "调查；探查；深入追问。",
    "fallout": "后果；余波；附带影响。",
    "hallucination": "幻觉；幻视；AI 语境中指无依据但像真的生成内容。",
    "grounding": "基础；接地；AI 语境中指把回答锚定到来源和上下文。",
    "delulu": "网络俚语，指带自嘲意味的“不切实际”或“上头”。",
    "brain rot": "网络俚语，指被低质量内容占据后的精神状态。",
    "deprecate": "不赞成；反对；技术语境中指弃用、不推荐继续使用。",
    "orchestrate": "编排；协调；像指挥一样组织多个部分。",
    "inflection point": "拐点；转折点；趋势开始改变方向的关键点。",
    "accountability gap": "责任缺口；责任链断裂、难以追责的状态。",
    "clanker": "俚语，对机器人或 AI 的贬称。",
    "unhinged": "失控的；离谱的；不受正常边界约束的。",
    "sense": "感觉；意义；判断力；感官。",
    "overhead": "头顶上方；经常性开销；技术语境中指额外系统开销。",
    "render": "使成为；呈现；计算机语境中指渲染、生成画面或界面。",
    "inference": "推断；推论；机器学习语境中指模型推理阶段。",
}


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


workflow_mod = load_module(RUN_PY, "wordsense_workflow_run")
builder_mod = load_module(BUILD_CONTENT, "wordsense_build_content")


def now() -> float:
    return time.time()


def event_day(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp, timezone.utc).astimezone().strftime("%Y-%m-%d")


def parse_date_to_timestamp(value: str, end_of_day: bool = False) -> float | None:
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return None
    if end_of_day:
        parsed = parsed.replace(hour=23, minute=59, second=59)
    return parsed.timestamp()


def append_event(record: dict[str, object]) -> None:
    record.setdefault("createdAt", now())
    with EVENT_LOCK:
        with EVENTS_FILE.open("a", encoding="utf-8") as file:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")


def read_jsonl(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    records: list[dict[str, object]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            records.append(value)
    return records


def read_events() -> list[dict[str, object]]:
    events = read_jsonl(EVENTS_FILE)

    for record in read_jsonl(SUBSCRIBERS_FILE):
        events.append({
            "event": "subscribe_success",
            "createdAt": record.get("createdAt"),
            "page": record.get("page") or "/",
            "source": "subscriber_file",
        })

    if JOBS_DIR.exists():
        for path in JOBS_DIR.glob("*.json"):
            try:
                job = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            word = str(job.get("word") or "")
            job_id = str(job.get("id") or path.stem)
            created = job.get("createdAt")
            updated = job.get("updatedAt") or created
            if created:
                events.append({
                    "event": "review_start",
                    "createdAt": created,
                    "word": word,
                    "jobId": job_id,
                    "source": "job_file",
                })
            if job.get("status") == "complete" and updated:
                events.append({
                    "event": "generation_success",
                    "createdAt": updated,
                    "word": word,
                    "jobId": job_id,
                    "source": "job_file",
                })
            if job.get("status") == "failed" and updated:
                events.append({
                    "event": "generation_fail",
                    "createdAt": updated,
                    "word": word,
                    "jobId": job_id,
                    "errorType": job.get("errorType"),
                    "source": "job_file",
                })
    return [event for event in events if isinstance(event.get("createdAt"), (int, float))]


def unique_count(events: list[dict[str, object]], names: set[str]) -> int:
    identities: set[str] = set()
    for event in events:
        if str(event.get("event")) not in names:
            continue
        identity = event.get("sessionId") or event.get("jobId")
        if identity:
            identities.add(str(identity))
        else:
            identities.add(f"{event.get('event')}:{event.get('createdAt')}:{event.get('word', '')}")
    return len(identities)


def build_metrics(days: int = 7, start: float | None = None, end: float | None = None) -> dict[str, object]:
    end_ts = end or now()
    start_ts = start if start is not None else end_ts - max(1, days) * 86400
    events = [
        event for event in read_events()
        if start_ts <= float(event.get("createdAt") or 0) <= end_ts
    ]

    trend_names = [
        "home_view",
        "word_click",
        "result_view",
        "search_submit",
        "review_start",
        "generation_success",
        "generation_fail",
        "save_click",
        "share_click",
        "subscribe_submit",
        "subscribe_success",
        "install_click",
    ]
    trend: dict[str, dict[str, int]] = {}
    for event in events:
        name = str(event.get("event") or "")
        if name not in trend_names:
            continue
        day = event_day(float(event.get("createdAt") or 0))
        trend.setdefault(day, {item: 0 for item in trend_names})
        trend[day][name] += 1

    funnel_steps = [
        ("访问首页", {"home_view"}),
        ("点击精选词条", {"word_click", "preview_continue_click"}),
        ("阅读词条页", {"result_view"}),
        ("提交搜索", {"search_submit"}),
        ("进入审校流程", {"review_start"}),
        ("生成成功", {"generation_success"}),
        ("保存/分享/订阅/安装", {"save_click", "share_click", "subscribe_success", "install_click"}),
    ]
    funnel = []
    previous = None
    for label, names in funnel_steps:
        count = unique_count(events, names)
        funnel.append({
            "step": label,
            "count": count,
            "rateFromPrevious": None if previous in (None, 0) else round(count / previous * 100, 1),
        })
        previous = count

    def event_total(names: set[str]) -> int:
        return sum(1 for event in events if str(event.get("event")) in names)

    checkpoints = [
        ("首页到精选词条", event_total({"home_view"}), event_total({"word_click", "preview_continue_click"}), "首页展示、选词吸引力"),
        ("词条页到保存/分享", event_total({"result_view"}), event_total({"save_click", "share_click"}), "结果页获得感和分享动机"),
        ("搜索到审校", event_total({"search_submit"}), event_total({"review_start"}), "搜索成本提示、API key、网络"),
        ("审校到生成成功", event_total({"review_start"}), event_total({"generation_success"}), "生成时间、模型/API 错误"),
        ("订阅表单到成功", event_total({"subscribe_submit"}), event_total({"subscribe_success"}), "邮箱表单、保存接口"),
    ]
    blockers = []
    for label, start_count, done_count, area in checkpoints:
        drop = max(0, start_count - done_count)
        blockers.append({
            "path": label,
            "start": start_count,
            "done": done_count,
            "drop": drop,
            "conversionRate": None if start_count == 0 else round(done_count / start_count * 100, 1),
            "watchArea": area,
        })

    word_counts: dict[str, int] = {}
    for event in events:
        if str(event.get("event")) in {"word_click", "result_view", "search_submit", "review_start", "generation_success"}:
            word = str(event.get("word") or "").strip()
            if word:
                word_counts[word] = word_counts.get(word, 0) + 1

    return {
        "window": {
            "start": start_ts,
            "end": end_ts,
            "days": days,
        },
        "totals": {
            "events": len(events),
            "uniqueSessions": unique_count(events, set(trend_names)),
        },
        "funnel": funnel,
        "trend": [
            {"date": day, **counts}
            for day, counts in sorted(trend.items())
        ],
        "blockers": blockers,
        "topWords": [
            {"word": word, "count": count}
            for word, count in sorted(word_counts.items(), key=lambda item: item[1], reverse=True)[:12]
        ],
    }


def read_dictionary_cache() -> dict[str, str]:
    with DICTIONARY_LOCK:
        if not DICTIONARY_CACHE_FILE.exists():
            return {}
        try:
            data = json.loads(DICTIONARY_CACHE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
        return {str(key): str(value) for key, value in data.items() if value}


def write_dictionary_cache(cache: dict[str, str]) -> None:
    with DICTIONARY_LOCK:
        DICTIONARY_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        DICTIONARY_CACHE_FILE.write_text(
            json.dumps(cache, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


def clean_dictionary_meaning(text: str) -> str:
    cleaned = re.sub(r"\s+", " ", text).strip().strip('"“”')
    cleaned = re.sub(r"^(释义|中文释义|常见中文释义)\s*[:：]\s*", "", cleaned)
    if len(cleaned) > 180:
        cleaned = cleaned[:180].rstrip("；，,、 ") + "。"
    return cleaned


def generate_dictionary_meaning(word: str, api_key: str | None = None) -> str | None:
    OpenAI = getattr(workflow_mod, "OpenAI", None)
    if OpenAI is None:
        return None

    load_dotenv = getattr(workflow_mod, "load_dotenv", None)
    if load_dotenv is not None:
        load_dotenv(WORKFLOW_DIR / ".env")

    resolved_api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not resolved_api_key:
        return None

    client_kwargs: dict[str, str] = {"api_key": resolved_api_key}
    resolved_base_url = os.getenv("OPENAI_BASE_URL")
    if resolved_base_url:
        client_kwargs["base_url"] = resolved_base_url

    client = OpenAI(**client_kwargs)
    model = os.getenv("OPENAI_DICTIONARY_MODEL") or os.getenv("OPENAI_MODEL") or workflow_mod.DEFAULT_WRITE_MODEL
    response = client.responses.create(
        model=model,
        max_output_tokens=120,
        instructions=(
            "你是一个简明英汉词典。用户给你一个英文单词或英文短语。"
            "请只输出常见中文释义,用分号分隔,必要时补充一个高频专业语境。"
            "不要写解释文章,不要写例句,不要使用 Markdown。"
        ),
        input=f"英文词或短语:{word}",
    )
    text = workflow_mod.response_text(response)
    return clean_dictionary_meaning(text) or None


def dictionary_meaning(word: str, api_key: str | None = None) -> str:
    key = word.strip().lower()
    if not key:
        return "常见中文释义正在整理中。"
    if key in DICTIONARY_MEANINGS:
        return DICTIONARY_MEANINGS[key]

    cache = read_dictionary_cache()
    if key in cache:
        return cache[key]

    try:
        generated = generate_dictionary_meaning(word, api_key=api_key)
    except Exception:
        generated = None

    if generated:
        cache[key] = generated
        write_dictionary_cache(cache)
        return generated

    return "常见中文释义正在整理中。"


def load_wordlist() -> set[str]:
    global WORDLIST
    if WORDLIST is not None:
        return WORDLIST

    words: set[str] = set(DICTIONARY_MEANINGS.keys())
    words.update(KNOWN_PHRASES)
    if WORDLIST_FILE.exists():
        for line in WORDLIST_FILE.read_text(encoding="utf-8").splitlines():
            item = line.strip().lower()
            if item:
                words.add(item)
    WORDLIST = words
    return WORDLIST


def normalized_spell_tokens(text: str) -> list[str]:
    lowered = text.lower().strip()
    lowered = lowered.replace("’", "'")
    lowered = lowered.replace("'s", "s")
    return re.findall(r"[a-z]+", lowered)


def levenshtein_distance(a: str, b: str, limit: int = 3) -> int:
    if abs(len(a) - len(b)) > limit:
        return limit + 1
    previous = list(range(len(b) + 1))
    for index_a, char_a in enumerate(a, start=1):
        current = [index_a]
        row_min = current[0]
        for index_b, char_b in enumerate(b, start=1):
            cost = 0 if char_a == char_b else 1
            value = min(previous[index_b] + 1, current[index_b - 1] + 1, previous[index_b - 1] + cost)
            current.append(value)
            row_min = min(row_min, value)
        if row_min > limit:
            return limit + 1
        previous = current
    return previous[-1]


def spelling_suggestions(token: str, limit: int = 5) -> list[str]:
    token = token.lower()
    if token in COMMON_SPELLING_SUGGESTIONS:
        return COMMON_SPELLING_SUGGESTIONS[token][:limit]

    if len(token) <= 2:
        return []

    candidates: list[tuple[int, float, str]] = []
    first = token[0]
    for word in load_wordlist():
        if " " in word or "-" in word or len(word) < 3:
            continue
        if word[0] != first:
            continue
        if abs(len(word) - len(token)) > 3:
            continue
        distance = levenshtein_distance(token, word, limit=3)
        if distance > 3:
            continue
        ratio = SequenceMatcher(None, token, word).ratio()
        if distance <= 2 or ratio >= 0.72:
            candidates.append((distance, -ratio, word))

    candidates.sort()
    suggestions: list[str] = []
    for _, _, word in candidates:
        if word not in suggestions and word != token:
            suggestions.append(word)
        if len(suggestions) >= limit:
            break
    return suggestions


def spellcheck_word(word: str) -> dict[str, object]:
    raw = word.strip()
    lowered = raw.lower().replace("’", "'")
    if not raw:
        return {"ok": False, "errorType": "empty", "suggestions": []}
    if contains_cjk(raw):
        return {
            "ok": False,
            "errorType": "invalid-word",
            "message": "目前 Word Sense 只支持英文词或英文短语。中文词条我们先不开放生成。",
            "suggestions": [],
        }
    if lowered in load_wordlist() or lowered in KNOWN_PHRASES:
        return {"ok": True, "suggestions": []}

    tokens = normalized_spell_tokens(raw)
    if not tokens:
        return {
            "ok": False,
            "errorType": "invalid-word",
            "message": "请输入英文词或英文短语。",
            "suggestions": [],
        }

    unknown = [token for token in tokens if token not in load_wordlist()]
    if not unknown:
        return {"ok": True, "suggestions": []}

    # Only block when there is a strong likely correction. Obscure but valid slang can still enter the workflow.
    suggestions = spelling_suggestions(unknown[0])
    if suggestions:
        return {
            "ok": False,
            "errorType": "misspelling",
            "message": "这个词看起来可能拼写有误。",
            "suggestions": suggestions,
            "unknownToken": unknown[0],
        }
    if not re.search(r"[aeiouy]", unknown[0]) or re.search(r"(qx|qz|zx|xq|zq)", unknown[0]):
        return {
            "ok": False,
            "errorType": "misspelling",
            "message": "这个词看起来不像有效英文拼写。请重新输入。",
            "suggestions": [],
            "unknownToken": unknown[0],
        }
    return {"ok": True, "suggestions": []}


def contains_cjk(text: str) -> bool:
    return bool(re.search(r"[\u3400-\u9FFF\uF900-\uFAFF]", text))


def normalize_display_word(word: str) -> str:
    raw = word.strip()
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


def job_path(job_id: str) -> Path:
    return JOBS_DIR / f"{job_id}.json"


def write_job(job_id: str) -> None:
    JOBS_DIR.mkdir(parents=True, exist_ok=True)
    with JOB_LOCK:
        data = dict(JOBS[job_id])
    job_path(job_id).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def update_job(job_id: str, **updates: object) -> None:
    with JOB_LOCK:
        if job_id not in JOBS:
            return
        JOBS[job_id].update(updates)
        JOBS[job_id]["updatedAt"] = now()
    write_job(job_id)


def start_stage_pacer(job_id: str, stop_event: threading.Event) -> threading.Thread:
    """Move the public review state forward while a long research call is running."""
    schedule = [
        (18, "对照真实使用场景", 2, "正在把词放回真实英语里。"),
        (45, "检查容易误读的地方", 3, "正在检查中文直译和真实语感之间哪里会错开。"),
        (75, "整理内容依据", 4, "正在收束主要来源和可展示给你的内容依据。"),
    ]

    def pace() -> None:
        started = now()
        for delay, stage, index, message in schedule:
            remaining = delay - (now() - started)
            if remaining > 0 and stop_event.wait(remaining):
                return
            if stop_event.is_set():
                return
            with JOB_LOCK:
                job = JOBS.get(job_id)
                if not job or job.get("status") != "running":
                    return
                current_index = int(job.get("stageIndex") or 0)
            if current_index < index:
                update_job(job_id, stage=stage, stageIndex=index, message=message)

    thread = threading.Thread(target=pace, daemon=True)
    thread.start()
    return thread


def public_job(job: dict[str, object]) -> dict[str, object]:
    allowed = {
        "id",
        "word",
        "source",
        "sentence",
        "status",
        "stage",
        "stageIndex",
        "message",
        "resultUrl",
        "error",
        "errorType",
        "createdAt",
        "updatedAt",
        "dictionaryMeaning",
    }
    return {key: value for key, value in job.items() if key in allowed}


def classify_workflow_error(exc: Exception) -> tuple[str, str]:
    """Turn provider exceptions into user-facing failure buckets."""
    text = str(exc)
    lowered = text.lower()

    if any(token in lowered for token in ["openai_api_key", ".env", "environment variable", "环境变量", "没有找到"]):
        return (
            "missing_key",
            "这次生成没有可用的 API key。请回到首页重新输入 key，或联系 Sarah 获取试用 key。",
        )

    if any(token in lowered for token in ["401", "403", "unauthorized", "forbidden", "access_denied", "no permission", "credentials", "invalid_api_key", "invalid api key", "incorrect api key", "authentication"]):
        return (
            "invalid_key",
            "这个 API key 没有通过验证，或没有权限访问当前服务/模型。请检查有没有复制完整，或者换一个 key 再试。",
        )

    if any(token in lowered for token in ["quota", "insufficient", "billing", "balance", "credit", "payment", "429"]):
        return (
            "quota",
            "这个 API key 可能余额不足、额度已用完，或触发了调用限制。请检查账户余额和限额后再试。",
        )

    if any(token in lowered for token in ["model", "not found", "does not exist", "not supported", "unsupported"]):
        return (
            "model",
            "当前 API key 或服务商可能不支持 WordSense 使用的模型。请换一个可用 key，或联系 Sarah 确认模型配置。",
        )

    if any(token in lowered for token in ["timeout", "timed out", "connection", "network", "tls", "ssl", "temporarily", "server disconnected"]):
        return (
            "network",
            "这次生成在网络连接或服务响应上中断了。你可以稍后重试，已经生成过的精选词条不受影响。",
        )

    return (
        "unknown",
        "这次词条处理没有完成。请稍后重试；如果连续失败，可以联系 Sarah 帮你看一下。",
    )


def run_job(job_id: str) -> None:
    with JOB_LOCK:
        job = dict(JOBS[job_id])
        secrets = dict(JOB_SECRETS.get(job_id, {}))

    word = str(job.get("word") or "").strip()
    source = str(job.get("source") or "").strip()
    sentence = str(job.get("sentence") or "").strip()
    output_dir = WORKFLOW_DIR / "output"
    safe_dir = output_dir / workflow_mod.safe_word_dir(word)

    try:
        workflow = workflow_mod.WordSenseWorkflow(
            write_model=str(job.get("writeModel") or workflow_mod.DEFAULT_WRITE_MODEL),
            research_model=str(job.get("researchModel") or workflow_mod.DEFAULT_RESEARCH_MODEL),
            rewrite_model=str(job.get("rewriteModel") or workflow_mod.DEFAULT_REWRITE_MODEL),
            output_dir=output_dir,
            search_context_size=str(job.get("searchContextSize") or "medium"),
            api_key=secrets.get("apiKey") or None,
        )

        update_job(
            job_id,
            status="running",
            stage="核对基础词义",
            stageIndex=0,
            message="WordSense 正在处理这个词条。",
        )
        draft = workflow.step_1_write(word, source, sentence)
        safe_dir.mkdir(parents=True, exist_ok=True)
        (safe_dir / "step-1-draft.md").write_text(draft, encoding="utf-8")

        update_job(
            job_id,
            stage="追溯词源和来路",
            stageIndex=1,
            message="正在核对词义、词源和来路。",
        )
        stop_pacer = threading.Event()
        pacer = start_stage_pacer(job_id, stop_pacer)
        research = workflow.step_2_research(word, draft)
        stop_pacer.set()
        pacer.join(timeout=0.2)
        (safe_dir / "step-2-research.md").write_text(research, encoding="utf-8")

        update_job(
            job_id,
            stage="写成最终词条",
            stageIndex=5,
            message="正在把审校后的内容写成最终词条。",
        )
        final = workflow.step_3_rewrite(word, draft, research)
        (safe_dir / "step-3-final.md").write_text(final, encoding="utf-8")

        meta = {
            "key": word.lower(),
            "displayWord": normalize_display_word(word),
            "meta": ["用户搜索", "WordSense"],
        }
        (safe_dir / "entry-meta.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        builder_mod.main()
        result_url = f"/word-sense-result_10.html?word={quote(word)}"
        update_job(
            job_id,
            status="complete",
            stage="审校完成",
            stageIndex=6,
            message="词条已经整理好，正在为你打开完整解读。",
            resultUrl=result_url,
        )
    except Exception as exc:
        error_type, public_error = classify_workflow_error(exc)
        update_job(
            job_id,
            status="failed",
            error=public_error,
            errorType=error_type,
            message=public_error,
        )
    finally:
        with JOB_LOCK:
            JOB_SECRETS.pop(job_id, None)


class Handler(BaseHTTPRequestHandler):
    server_version = "WordSenseServer/0.1"

    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.end_headers()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/events":
            self.handle_event()
            return

        if parsed.path == "/api/subscribe":
            self.handle_subscribe()
            return

        if parsed.path != "/api/jobs":
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length).decode("utf-8") if length else "{}"
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            self.send_json({"error": "invalid json"}, status=400)
            return

        word = str(payload.get("word") or "").strip()
        if not word:
            self.send_json({"error": "word is required"}, status=400)
            return
        if contains_cjk(word):
            self.send_json({
                "error": "目前 Word Sense 只支持英文词或英文短语。中文词条我们先不开放生成。",
                "errorType": "invalid-word",
            }, status=400)
            return
        spelling = spellcheck_word(word)
        if not spelling.get("ok"):
            self.send_json({
                "error": spelling.get("message") or "这个词看起来可能拼写有误。请重新输入。",
                "errorType": spelling.get("errorType") or "misspelling",
                "suggestions": spelling.get("suggestions") or [],
            }, status=400)
            return
        api_key = str(payload.get("apiKey") or "").strip()

        job_id = f"{int(now() * 1000)}-{workflow_mod.safe_word_dir(word).lower()}"
        job = {
            "id": job_id,
            "word": word,
            "source": str(payload.get("source") or ""),
            "sentence": str(payload.get("sentence") or ""),
            "status": "queued",
            "stage": "准备审校",
            "stageIndex": 0,
            "message": "词条已经进入审校队列。",
            "dictionaryMeaning": dictionary_meaning(word, api_key=api_key),
            "createdAt": now(),
            "updatedAt": now(),
        }

        with JOB_LOCK:
            JOBS[job_id] = job
            if api_key:
                JOB_SECRETS[job_id] = {"apiKey": api_key}
        write_job(job_id)

        thread = threading.Thread(target=run_job, args=(job_id,), daemon=True)
        thread.start()
        self.send_json(public_job(job), status=201)

    def handle_event(self) -> None:
        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length).decode("utf-8") if length else "{}"
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            self.send_json({"error": "invalid json"}, status=400)
            return

        event_name = str(payload.get("event") or "").strip()
        if not re.match(r"^[a-z][a-z0-9_]{1,48}$", event_name):
            self.send_json({"error": "invalid event"}, status=400)
            return

        properties = payload.get("properties") if isinstance(payload.get("properties"), dict) else {}
        record = {
            "event": event_name,
            "sessionId": str(payload.get("sessionId") or "")[:80],
            "page": str(payload.get("page") or "")[:240],
            "word": str(properties.get("word") or payload.get("word") or "")[:120],
            "properties": properties,
            "referer": self.headers.get("Referer", "")[:240],
            "userAgent": self.headers.get("User-Agent", "")[:240],
            "createdAt": now(),
        }
        append_event(record)
        self.send_json({"ok": True}, status=201)

    def handle_subscribe(self) -> None:
        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length).decode("utf-8") if length else "{}"
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            self.send_json({"error": "invalid json"}, status=400)
            return

        email = str(payload.get("email") or "").strip().lower()
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            self.send_json({"error": "请填写有效邮箱。"}, status=400)
            return

        record = {
            "email": email,
            "page": str(payload.get("page") or ""),
            "createdAt": now(),
        }
        with SUBSCRIBERS_FILE.open("a", encoding="utf-8") as file:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")

        self.send_json({"ok": True, "email": email}, status=201)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/metrics":
            query = parse_qs(parsed.query)
            try:
                days = int(str(query.get("days", ["7"])[0]) or "7")
            except ValueError:
                days = 7
            days = max(1, min(days, 365))
            start = query.get("start", [""])[0]
            end = query.get("end", [""])[0]
            start_ts = parse_date_to_timestamp(start) if start else None
            end_ts = parse_date_to_timestamp(end, end_of_day=True) if end else None
            self.send_json(build_metrics(days=days, start=start_ts, end=end_ts))
            return

        if parsed.path == "/api/dictionary":
            query = parse_qs(parsed.query)
            word = str(query.get("word", [""])[0]).strip()
            if not word:
                self.send_json({"error": "word is required"}, status=400)
                return
            if contains_cjk(word):
                self.send_json({
                    "error": "目前 Word Sense 只支持英文词或英文短语。中文词条我们先不开放生成。",
                    "errorType": "invalid-word",
                }, status=400)
                return
            self.send_json({"word": word, "dictionaryMeaning": dictionary_meaning(word)})
            return

        if parsed.path == "/api/spellcheck":
            query = parse_qs(parsed.query)
            word = str(query.get("word", [""])[0]).strip()
            result = spellcheck_word(word)
            self.send_json({"word": word, **result})
            return

        if parsed.path.startswith("/api/jobs/"):
            job_id = unquote(parsed.path.removeprefix("/api/jobs/"))
            with JOB_LOCK:
                job = JOBS.get(job_id)
            if job is None and job_path(job_id).exists():
                job = json.loads(job_path(job_id).read_text(encoding="utf-8"))
            if job is None:
                self.send_json({"error": "job not found"}, status=404)
                return
            self.send_json(public_job(job))
            return

        self.serve_static(parsed.path)

    def do_HEAD(self) -> None:
        parsed = urlparse(self.path)
        self.serve_static(parsed.path, head_only=True)

    def serve_static(self, request_path: str, head_only: bool = False) -> None:
        if request_path in ("", "/"):
            request_path = "/word-sense-home_9.html"
        relative = unquote(request_path).lstrip("/")
        path = (ROOT / relative).resolve()
        if not str(path).startswith(str(ROOT.resolve())) or not path.exists() or path.is_dir():
            self.send_error(404)
            return
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        if path.name == "manifest.webmanifest":
            content_type = "application/manifest+json"
        data = path.read_bytes()
        self.send_response(200)
        if content_type.startswith("text/") or content_type in {"application/javascript", "application/json", "image/svg+xml"}:
            content_type = f"{content_type}; charset=utf-8"
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        if not head_only:
            self.wfile.write(data)

    def send_json(self, payload: dict[str, object], status: int = 200) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format: str, *args: object) -> None:
        sys.stderr.write("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format % args))


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"WordSense server running at http://{HOST}:{PORT}/word-sense-home_9.html")
    server.serve_forever()


if __name__ == "__main__":
    main()
