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
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlparse


ROOT = Path(__file__).resolve().parent
WORKFLOW_DIR = ROOT / "word-sense-workflow"
JOBS_DIR = WORKFLOW_DIR / "jobs"
RUN_PY = WORKFLOW_DIR / "run.py"
BUILD_CONTENT = WORKFLOW_DIR / "build_content_js.py"
SUBSCRIBERS_FILE = ROOT / "mailing-list.jsonl"
DICTIONARY_CACHE_FILE = WORKFLOW_DIR / "dictionary-cache.json"

HOST = "127.0.0.1"
PORT = 8787

JOB_LOCK = threading.Lock()
DICTIONARY_LOCK = threading.Lock()
JOBS: dict[str, dict[str, object]] = {}
JOB_SECRETS: dict[str, dict[str, str]] = {}

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
