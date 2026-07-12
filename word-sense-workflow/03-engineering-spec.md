# 工程实现规格

## 推荐技术栈

当前实现使用 **Python + OpenAI SDK**。

接口按 OpenAI-compatible 方式调用,可以通过 `OPENAI_BASE_URL` 指向兼容服务。第一版已经落在 `run.py` 上,目标是简单可靠:输入一个英文词,跑完三步,输出三份 markdown 文件。

## 依赖

```
openai>=1.99.0
python-dotenv
```

## 项目结构

```
word-sense-workflow/
├── prompts/
│   ├── v3-write.md
│   ├── v3-research.md
│   └── v3-rewrite.md
├── output/
│   └── [word]/
│       ├── step-1-draft.md
│       ├── step-2-research.md
│       ├── step-3-final.md
│       └── entry-meta.json
├── run.py
├── requirements.txt
├── .env.example
└── .env
```

正式 Issue 的 `entry-meta.json` 至少包含：

```json
{
  "key": "streak",
  "displayWord": "streak",
  "surface": "条纹；痕迹；连续纪录",
  "meta": ["连续纪录 · 条纹痕迹 · B2", "Issue 006"]
}
```

`build_content_js.py` 必须把 `surface` 原样写入 `word-sense-content.js`。正式期刊条目缺少该字段应在发布审计阶段失败，不能让前端用正文第一段静默代替。

## 配置

`.env` 文件:

```
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://zenmux.ai/api/v1

# Optional model overrides:
# OPENAI_MODEL=openai/gpt-5.4-mini
# OPENAI_RESEARCH_MODEL=openai/gpt-5.4
# OPENAI_REWRITE_MODEL=openai/gpt-5.4
# OPENAI_SEARCH_CONTEXT_SIZE=medium
```

不要把 API key 写进代码或提交到 git。

## 主流程

`run.py` 用 OpenAI Responses API 跑三步:

1. **Step 1 写作**
   - prompt:`prompts/v3-write.md`
   - model:`OPENAI_MODEL` 或默认 `openai/gpt-5.4-mini`
   - 输出:`step-1-draft.md`

2. **Step 2 查证**
   - prompt:`prompts/v3-research.md`
   - model:`OPENAI_RESEARCH_MODEL` 或默认 `openai/gpt-5.4`
   - 启用 `web_search`
   - 输出:`step-2-research.md`

3. **Step 3 改写**
   - prompt:`prompts/v3-rewrite.md`
   - model:`OPENAI_REWRITE_MODEL` 或默认 `openai/gpt-5.4`
   - 输入 Step 1 初稿 + Step 2 查证报告
   - 输出:`step-3-final.md`

## 命令

安装依赖:

```bash
pip install -r requirements.txt
```

检查 prompt 和输出路径,不调用 API:

```bash
python run.py brainrot --dry-run
```

简单跑:

```bash
python run.py brainrot
```

带出处和原句:

```bash
python run.py concerning --source "周会后老板的邮件" --sentence "My manager said some of these numbers are concerning."
```

指定模型或输出目录:

```bash
python run.py backdrop \
  --model openai/gpt-5.4-mini \
  --research-model openai/gpt-5.4 \
  --rewrite-model openai/gpt-5.4 \
  --output-dir output
```

## 错误处理

- **缺少依赖**:提示安装 `requirements.txt`。
- **缺少密钥**:提示配置 `OPENAI_API_KEY`。
- **Step 1 失败**:停止工作流,不生成后续文件。
- **Step 2 失败**:停止工作流,保留 Step 1 输出,用户可重试。
- **Step 3 失败**:保留 Step 1 和 Step 2 输出,用户可手动改写或重试。
- **查证找不到**:不要假装查到了;在 Step 2 报告里标注无法验证。

## 后续可以加的功能

- 批量跑多个词
- 搜索结果缓存
- Web UI
- 用统一 `issue-XXX.json` 同时生成批处理输入、首页词卡、归档和宣传物料，彻底移除重复的手工词表
- 生成 Notion/个人笔记版本

单词级生成仍以三份 Markdown 为核心；正式 Issue 发布必须继续执行 `05-issue-release-workflow.md`。
