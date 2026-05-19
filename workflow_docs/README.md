# Word Sense 内容生产工作流

## 这是什么

这是一份给 AI 工程助手(Codex)的交付包,目的是实现一个**多步骤 AI 内容生产工作流**,服务于一个叫 Word Sense 的中文产品。

## 给 Codex 的简单说明

请按以下顺序读这些文件:

1. `01-product-context.md` — 先了解 Word Sense 是什么产品,你要服务什么样的内容生产
2. `02-workflow-overview.md` — 看懂三步骤工作流的整体逻辑
3. `prompts/v3-write.md` — 写作 prompt
4. `prompts/v3-research.md` — 查证 prompt(这是 agent 步骤,需要工具调用)
5. `prompts/v3-rewrite.md` — 改写 prompt
6. `03-engineering-spec.md` — 工程实现规格(技术栈、API 调用、输出格式)
7. `04-example-run.md` — 一个完整的"brainrot"跑过的实例,作为参照

## 你要交付的东西

一个能跑的 Python 脚本,使用 OpenAI-compatible API。输入一个英文词,输出三份文件:

```
output/
├── [词]/
│   ├── step-1-draft.md       # Step 1 的写作初稿
│   ├── step-2-research.md    # Step 2 的查证报告
│   └── step-3-final.md       # Step 3 的改写终稿
```

## 一些原则

- **优先简单和可靠,不追求花哨**。这是给一个独立产品创始人用的工具,不是企业级产品。
- **每一步都要保存中间结果**,方便调试和审查。
- **Step 2 必须有工具调用能力**(当前实现使用 `web_search`),不能纯靠 LLM 知识。
- **当前实现使用 OpenAI SDK Responses API**,通过 `OPENAI_API_KEY` 和可选的 `OPENAI_BASE_URL` 配置。
- **错误处理要明确**,不要静默失败。

## 联系方式

如果有任何 prompt 内容或工作流逻辑不清楚的地方,请明确指出,不要自己推测。这件事的细节由产品所有者(Leon)决定。
