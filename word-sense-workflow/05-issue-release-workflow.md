# Word Sense 整期发布工作流

三阶段工作流只负责把文章写好。正式 Issue 只有完成本文件中的元数据、页面、缓存、视觉和公网验收，才算“已上线”。

## 1. 正式期刊输入

每个词至少提供：

- `word`：查询键，通常为规范小写。
- `displayWord`：需要特殊大小写时填写。
- `surface`：卡片正面的简短中文释义。
- `meta`：主题、等级，以及唯一的 `Issue NNN` 标签。
- 首页卡片信息：`meaning`、`trail`、`clue`。

`surface` 规范：

- 只写 2–4 个简短义项，例如 `条纹；痕迹；连续纪录`。
- 不解释，不写完整段落，不复制正文的“字面含义”。
- 建议 4–30 个中文字符，机器硬限制不超过 40 字。
- 多义词要覆盖正文实际展开的主要义项。

## 2. 三阶段内容生产

每个词依次保存：

1. `step-1-draft.md`
2. `step-2-research.md`
3. `step-3-final.md`
4. `entry-meta.json`

Step 2 必须使用搜索工具。Step 3 必须处理 sense coverage 中标记为“必须补”的项目。

## 3. 构建内容包

本期批处理脚本即使跳过已有正文，也必须重写最新的 `entry-meta.json`，然后运行 `build_content_js.py`。

`word-sense-content.js` 必须保留：

- `displayWord`
- `surface`
- `meta`
- `markdown`
- `verification`

展示规则：

- “正面写着”只读取 `surface`。
- “01 / 字面”读取终稿中的 `字面含义`。
- 正式期刊缺少 `surface` 时必须阻止上线，不能静默截取正文兜底。
- 摘要兜底只允许用于用户即时生成的新词或兼容旧档案。

## 4. 首页、归档与阅读页

首页必须完成：

- 顶部期数更新为本期。
- `ISSUE NNN WORD CARDS / N FILES` 与清单数量一致。
- 本期词卡完整且排序正确。
- 上一期完整移入归档抽屉。
- 不残留上一期标题、词数或专属主题。

独立阅读页从内容包的 `Issue NNN` 元数据读取身份：

- 内容包中的最高期数为当前期。
- 当前期显示 `CURRENT ISSUE / HANDLE WITH CARE`。
- 更早期显示 `ARCHIVE COPY / HANDLE WITH CARE`。
- 顶部徽章显示该词自己的期数，不能写死。

## 5. 缓存

修改首页、阅读页、内容包或静态资源后，必须更新 `service-worker.js` 的 `CACHE_NAME`。缓存名应包含可辨认的发布说明，例如 `wordsense-v18-archive-label`。

## 6. 自动审计

```bash
python3 word-sense-workflow/audit_content.py --issue "Issue 006" --expected-count 18
```

必须检查：

- 本期存在词条。
- Issue 006 及后续每个正式期刊词条都有 `surface`，且不超过 40 字；旧归档保留兼容兜底。
- 固定正文章节齐全。
- 无占位文案。
- 有用户可见来源。
- 本期词数与清单一致（发布脚本另行核对）。

## 7. 语法与视觉验收

检查 `index.html`、`word-sense-entry.html` 的内联脚本，以及 `service-worker.js`。

必须实际渲染桌面版和移动版截图，并至少打开：本期首词、一个短语、一个长词和末词。检查：

- 正面短释义与“字面含义”不重复。
- 期数徽章和当前期/归档印章正确。
- 归档袋提示文字完整，不被词卡遮挡，不溢出。
- 移动端无错位、裁切或异常换行。

视觉层级、定位和溢出问题不能只靠代码审查判断。

## 8. Git 与生产发布

发布提交只能包含本期相关文件，不得夹带用户的其他未提交内容。

1. 提交并推送 `main`。
2. VPS 拉取；若生产目录不是 Git 工作副本，则上传到 `/tmp`。
3. 在 VPS 校验期数、词数、`surface` 和缓存版本。
4. 备份旧生产文件。
5. 替换文件并重启 `wordsense`。
6. 确认服务状态为 `active`。

## 9. 公网验收

使用无缓存请求验证：

- `/index.html`
- `/word-sense-content.js`
- `/word-sense-entry.html?word=[本期首词]`
- 一个短语词条
- `/service-worker.js`

确认 HTTP 200、本期词数、短释义、Issue 身份和最新缓存版本。

## 完成定义

只有内容与查证完成、展示元数据完整、首页和归档正确、缓存更新、自动审计与截图通过、生产服务正常且公网验证通过，才能对外说“本期已上线”。
