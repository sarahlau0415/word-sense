# Word Sense 社媒宣传 Workflow

这个 workflow 用来在每一期 Word Sense 上线后，生成小红书和 X 的图文物料。Issue 003 已经用这套流程跑通：小红书 8 张轮播、X 1 张横图、配套正文、图内文案检查、发布。

## 你在哪里能找到它

文件位置：

campaigns/social-campaign-workflow.md

第三期参考文件：

campaigns/generate-issue-003-images.js
campaigns/issue-003-images.html
campaigns/issue-003-social-pack.md
campaigns/issue-003-images/

## 你怎么调用它

以后你可以直接说：

“按 social campaign workflow 做第四期物料。”

或者：

“第四期上线了，跑一下小红书和 X 的宣传图文。”

我就会按这个流程执行，而不是重新发明一遍。

## 什么时候开始

主站内容已经基本确认之后开始。最好是在这一期已经能本地预览，或者已经上线之后。

开始宣传物料前，主站必须先通过 `word-sense-workflow/05-issue-release-workflow.md`。词条正文完成但首页、阅读页身份或缓存尚未更新时，不算“已经上线”。

需要输入：

1. 期数，比如 Issue 004。
2. 本期词表，一般 12 到 18 个词。
3. 你最想主推的 3 到 5 个词。
4. 本期核心感觉，比如“普通词的背面”“AI 词的身体感”“职场词里的权力关系”。
5. 默认链接：https://wordsense.sarahliu.fun/

如果你没有单独给这些信息，我会从 index.html 和 word-sense-content.js 里提取。

其中“每个词的表面意思”必须读取结构化 `surface` 字段。不要用正文 `字面含义` 的第一段代替，否则会造成宣传短句和阅读正文重复。

## 每期应该产出什么

### 小红书

默认 8 张轮播图，尺寸 1080 x 1440。

建议结构：

1. 封面：本期核心判断。
2. 主推词 1：用错位感抓人。
3. 主推词 2：展示真实语境里的动作或质感。
4. 一组普通词：说明为什么熟词最容易误解。
5. 一组概念词：职场、AI、制度、文化等。
6. 一组轻一点的词：社媒、生活、新词、怪词。
7. 结构性洞察：让用户感觉不是在背词。
8. 收尾：读完一张，再抽出下一张。

### X

默认 1 张横图，尺寸 1600 x 900。

内容要轻，通常只放：

- Issue 编号
- 4 个主推词
- 每个词一句短线索
- 链接或域名

### 文案包

每期生成一个文件：

campaigns/issue-XXX-social-pack.md

里面包括：

- X 英文单帖
- X 中文单帖
- X thread
- 小红书标题备选
- 小红书正文
- 小红书标签
- 每张小红书图的分镜说明
- 每张图片对应文件名

## 视觉规则

沿用新版 Word Sense 的视觉语言：

- 磁卡
- 旧纸张
- 档案袋
- 索引标签
- 报纸、笔记、纸片线索
- 独立出版物感

不要回到旧的 AI landing page 感。

避免：

- 大面积渐变
- 纯 UI mockup 感
- 只有效果图，没有图内文案
- 文案漂浮在背景上，没有承载色块
- 文字超出色块
- 英文词条全部大写

## 图内文案规则

这是最重要的检查点。

1. 文案必须放在明确的色块、纸片、卡片或档案元素里。
2. 长句必须手动换行。
3. 每一行都要待在自己的色块内。
4. 中文句子尽量短，不要一行塞太长。
5. 英文词条保持小写，除非它本来就是固定大写缩写。
6. 每张图只讲一个主感觉，不要像教材。

推荐句式：

- X 不是 A，而是 B。
- 它不是在说 A，而是在暗示 B。
- 中文容易先抓 A，英语里这里还有 B。
- 词形给你 A，语境给你 B。

## 执行步骤

### Step 1 读本期内容

从 index.html 和 word-sense-content.js 里提取：

- 本期词表
- 每个词的表面意思
- 每个词最适合传播的一句话线索
- 3 到 5 个最抓人的词
- 本期统一主题

### Step 2 写 social pack

先写文案包：

campaigns/issue-XXX-social-pack.md

文案先确认，再进图。

### Step 3 写图片生成器

参考上一期生成器，新建：

campaigns/generate-issue-XXX-images.js

输出目录：

campaigns/issue-XXX-images/

预览页：

campaigns/issue-XXX-images.html

### Step 4 生成 SVG

运行：

node campaigns/generate-issue-XXX-images.js

### Step 5 导出 PNG

用 Chrome headless 把 SVG 导出成 PNG。

小红书图：1080 x 1440。
X 横图：1600 x 900。

Issue 003 的导出方式已经在实际流程里跑通，之后可以复用同样脚本。

### Step 6 预览

打开：

campaigns/issue-XXX-images.html

检查：

- 8 张小红书图是否都能显示。
- X 横图是否能显示。
- 图内文案是否完整。
- 文字是否都在色块里。
- 有没有长句冲出纸片。
- 词条是否小写。
- 中文是否面向中文用户。

### Step 7 长度审计

对所有 SVG 文本做一次长度审计。

目标：找出可能过长的图内文字行。

如果发现长行，回到生成器里手动拆行，然后重新生成 SVG 和 PNG。

Issue 003 已经验证过：最后一轮审计结果是没有明显过长文字行。

## 发布建议

### 小红书

先发小红书，因为轮播更适合 Word Sense 的慢读感。

使用：

campaigns/issue-XXX-images/xhs-01-cover.png 到 xhs-08-closing.png
campaigns/issue-XXX-social-pack.md 里的标题、正文、标签

### X

可以发单帖，也可以发 thread。

推荐：

- 想轻一点：中文单帖 + x-cover.png。
- 想解释产品：thread + x-cover.png。

## 发布后沉淀

发布完成后保留：

campaigns/generate-issue-XXX-images.js
campaigns/issue-XXX-images.html
campaigns/issue-XXX-images/*.svg
campaigns/issue-XXX-images/*.png
campaigns/issue-XXX-social-pack.md

这些文件就是下一期的模板和复盘材料。

## Issue 003 已跑通结果

Issue 003 已经完成：

- 小红书 8 张 PNG。
- X 横图 1 张 PNG。
- 图内文案已放入色块。
- 长句已手动换行。
- 运行过文字长度审计。
- 已发布。

参考：

campaigns/generate-issue-003-images.js
campaigns/issue-003-images.html
campaigns/issue-003-social-pack.md
