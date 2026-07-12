# Word Sense Campaign Fast Workflow

这个文件是给下一期发刊时快速启动用的。目标是减少长上下文带来的摩擦：先把“期数、主题、词表、视觉规则、检查命令”放在一个固定位置。

## 新线程启动 brief

复制这一段到新的 Codex 线程即可：

```text
项目目录：/Users/sarah/projects/word-sense/frontend

我要做 Word Sense Issue 00X 的宣传物料。

词表：
[在这里贴 16 个词]

这一期主题：
[一句话说清楚，比如：熟词背面 / 机器术语 / 日常动词里的社会边界]

需要输出：
- X 单图 + 文案
- 小红书 8 张轮播 + 标题/正文/标签
- 如有需要，再加朋友圈方图

视觉规则：
- 强撞色、文字主导、卡片/档案线索感
- 图内文案必须落在色块里，不能溢出
- 首图要一眼看懂 Word Sense 的亮点
- 不继承上一期专属元素，比如“机器术语”章，除非本期明确需要
- 词条小写优先，中文用户要能一眼认出来

完成后请运行：
node campaigns/generate-campaign.js issue-00X
node campaigns/check-campaign.js issue-00X
```

## 本地命令

先进入项目目录：

```bash
cd /Users/sarah/projects/word-sense/frontend
```

生成某一期 SVG 和预览页：

```bash
node campaigns/generate-campaign.js issue-005
```

检查某一期物料：

```bash
node campaigns/check-campaign.js issue-005
```

预览：

```bash
python3 -m http.server 4173
# 打开 http://127.0.0.1:4173/campaigns/issue-005-images.html
```

## 发刊前检查

- 主站已通过 `word-sense-workflow/05-issue-release-workflow.md` 的整期发布门禁。
- 本期每个词都有独立 `surface`；宣传文案不截取“字面含义”正文代替。
- 首页期数、词数、当期卡片和上一期归档均正确。
- 独立阅读页的 Issue 徽章及 CURRENT / ARCHIVE 身份正确。
- Service Worker 缓存版本已更新。
- `issue-XXX-social-pack.md` 存在。
- `generate-issue-XXX-images.js` 存在且 `node -c` 通过。
- `issue-XXX-images.html` 能打开。
- 小红书 PNG 是 `1080x1440`。
- X PNG 是 `1600x900`。
- 没有残留上一期的期号、标签、专属章。
- 实际渲染完整截图，检查归档提示、标签、色块和长词没有互相遮挡。
- 首图文案足够直给，且没有长句溢出色块。
- X 图卡片里的英文短句没有横跨到隔壁卡片。

## 我需要参与的步骤

1. 给词表和本期主题。
2. 看首图方向，确认“是否有点击欲”。
3. 看一轮图内文案是否太晦涩。
4. 最后决定是否发布。

其余的生成、检查、修溢出、整理路径，都交给 Codex 做。
