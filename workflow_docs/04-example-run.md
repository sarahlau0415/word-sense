# 完整示例:brainrot 一遍工作流跑下来长什么样

这是 Leon 在产品设计阶段**真实跑过的一次工作流**,作为 Codex 实现时的参照样本。

如果你的实现跑出来的结果跟下面这个**大致接近**(三个文件都有、长度合理、维度结构对),说明工作流跑通了。

---

## Step 1: 初稿(用 v3-write 跑出来的)

**输入:** `词:brainrot`

**输出:** 保存到 `output/brainrot/step-1-draft.md`

```markdown
**字面含义** · brain + rot,字面是"脑子在腐烂"。Rot 这个词有强烈的画面感 —— 不是干净的损坏,是有机物腐败发酸、缓慢溃败的那种烂。所以 brainrot 的字面意象很刺激:脑子像放久了的水果一样在自己烂掉。

**本体质感** · 这个词最迷人的地方是它**带着自嘲、近乎躺平的姿态**。

它不是用来骂别人的(那是"脑残")。它的典型使用者**就是它描述的对象** —— 一个人说"I have such bad brainrot",意思是"我自己被算法和短视频喂废了,我知道,但我没打算停下来"。这种"我看清楚自己在干嘛但我接受这个状态"的姿态是 brainrot 的灵魂。

它跟"addiction"(上瘾)很不一样。addiction 是严肃的、病理化的、需要治疗的;brainrot 是日常化的、轻盈的、自我开玩笑的。说"我有 brainrot"几乎是社交润滑 —— 你在告诉对方"我跟你一样,我也在沉沦,我们坐在同一条船上"。

这个词还有几种衍生用法:

- **brainrot content**:指代某类内容本身(尤其是 TikTok 上那些极度无意义、视觉刺激密集的短视频)
- **X brainrot**:指某人过度沉迷某事物(Taylor Swift brainrot、Skibidi Toilet brainrot)

最有趣的元层面:**用 brainrot 这个词本身,就是 brainrot 的一部分**。它是一个 Gen Z / Gen Alpha 圈层的内部黑话,你知道这个词、你在用这个词,你就已经在那个圈子里。

**寻根溯源** · "Brain rot"作为短语在英语里其实很老 —— 据说 19 世纪美国作家梭罗在《瓦尔登湖》(1854 年)里用过,批判同时代精神上的退化。但作为一个连写的词(brainrot)在互联网语境里复活、然后爆炸式流行,是 2020 年代的事。

它的兴起跟 TikTok 算法推送密切相关。当一个人能连续刷几小时短视频,然后感觉自己"什么都没获得但又停不下来",需要一个词来命名这种状态。brainrot 抢到了这个位置 —— 既精确(腐烂的画面感),又自嘲(不像"成瘾"那么沉重)。这个词在 2024 年被牛津年度词汇收录。

**各路用法** · 这个词主要在日常和社媒场景出现,职场基本不用:

**[日常,跟朋友吐槽]**
I have such bad TikTok brainrot right now — I literally can't read a book for more than ten minutes.

**[社媒,典型用法]**
the skibidi toilet brainrot is real my 8-year-old nephew speaks in a different language now

**[社媒,自嘲式]**
sorry for the typo im running on three hours of sleep and pure brainrot

注意社媒例句里那种"低 effort"的写法 —— 全小写、没标点、不修语法。

**原生思维** · 中文里没有这个概念。这是真正的"中文没有对应词"情况。

可以考虑的近似翻译都不够:
- "脑子坏掉了" —— 太字面,且听起来像真的骂人
- "信息过载" —— 学术词,完全没有 brainrot 的自嘲玩味
- "刷废了" —— 抓住了状态,但漏掉了 brainrot 也能指内容类型这一层
- "短视频毒害" —— 长辈视角,单向批判,brainrot 是用户自己嘴里说出来的

中文母语者表达类似意思时,通常用一连串的句式而不是单个词:"我最近抖音刷得脑子都不会转了"、"这种视频看多了人会变傻"、"我现在脑子里全是 XX"。

**悟道时刻** · brainrot 属于 Gen Z 在做的一件大事:**给算法时代的新型精神状态命名**。同族词:

- doomscrolling(忍不住一直滑负面新闻)
- cooked(完蛋了,通常自嘲)
- down bad(陷得很深)
- touch grass(去摸摸草,意思是别上网了)
- chronically online(过度上网的)
- enshittification(平台慢慢变坏的过程)

这一族词的共同特点是:**它们命名的是数字时代独有的精神状态**,在前互联网时代根本不存在这些处境。
```

---

## Step 2: 查证报告(用 v3-research 跑出来的)

**保存到** `output/brainrot/step-2-research.md`

```markdown
# 查证报告:brainrot

## 待查事实清单

1. "梭罗在《瓦尔登湖》1854 年用过 brain rot 短语,批判同时代精神退化"
2. "brainrot 这个连写词在 2020 年代爆炸式流行"
3. "brainrot 在 2024 年被牛津年度词汇收录"
4. "doomscrolling / cooked / down bad / touch grass / chronically online / enshittification 是 brainrot 的同族词"

## 查证过程

通过多个来源查证:
- NPR (https://www.npr.org/.../thoreau-warned-of-brain-rot-in-1854)
- Wikipedia "Brain rot" (https://en.wikipedia.org/wiki/Brain_rot)
- Oxford University Press 官方公告 (https://corp.oup.com/news/brain-rot-named-oxford-word-of-the-year-2024/)
- Know Your Meme "Brain Rot / Brainrot"
- Adam Aleksic 词源 Substack
- Smithsonian Magazine
- Merriam-Webster 2024 字典更新报道

## 查证结果

### ✅ 证实(可保留)

- **断言 1(梭罗 1854)**:**完全证实,且找到了原句**。
  - 来源:Oxford University Press、NPR、Wikipedia、Smithsonian 多源确认
  - 原文:"While England endeavors to cure the potato-rot, will not any endeavor to cure the brain-rot, which prevails so much more widely and fatally?"
  - 出处:Henry David Thoreau, _Walden_ (1854), 结尾章节
  - 上下文:梭罗在批判同时代人对复杂思想的轻视,把"脑之腐"跟当时正在爱尔兰肆虐的马铃薯枯萎病作类比

- **断言 3(2024 牛津年度词)**:完全证实。
  - 来源:Oxford University Press 官方公告(2024 年 12 月)
  - 关键数据:2023-2024 brainrot 使用频率增长 230%

### ⚠️ 部分证实(需软化或细化)

- **断言 2(2020 年代爆炸式流行)**:大方向对,但时间线可以更精确。
  - 实际时间线:
    - 2007 年首次在 Twitter 出现(Know Your Meme)
    - 2010 年代逐步增加
    - **2020 年在 Discord 上成为 meme**(Wikipedia 关键节点)
    - 2023 年 11 月开始随着 Skibidi Toilet 等病毒视频在 TikTok 爆发
    - 2024 年被牛津宣布为年度词汇(230% 增长)
    - **2025 年衍生出"Italian Brainrot"子流派**(AI 生成的伪意大利怪物 Tralalero Tralala、Tung Tung Tung Sahur 等)
  - 建议改写方向:把模糊的"2020 年代"改成更精确的时间节点链

- **断言 4(同族词)**:大部分证实,但 enshittification 是例外。
  - doomscrolling / touch grass / chronically online:完全是同族,Merriam-Webster 2024 同时收入 doomscroll 和 brainrot
  - cooked / down bad:确实是 Gen Z 网络语言一部分,接近同族
  - **enshittification 是例外**:它是 Cory Doctorow 2022/2023 年造的有明确作者的术语词,跟其他自发演化的网络词不完全同源
  - 建议:删除 enshittification,或单独说明它的特殊性

### ❓ 无法确认

- 无重大无法确认项

### ❌ 证伪

- 无需要证伪的内容

## 改写建议

1. **加入梭罗原句**(中英对照):
   "While England endeavors to cure the potato-rot, will not any endeavor to cure the brain-rot, which prevails so much more widely and fatally?"
   这是 brainrot 一篇真正的重量级素材,强烈建议加进"寻根溯源"维度。

2. **细化时间线**:从"2020 年代爆炸式流行"改成"2007 Twitter 首现 → 2020 Discord 成 meme → 2023 TikTok 爆发 → 2024 牛津年度词汇"。

3. **加入 Italian Brainrot 2025 现象**(可选):这是非常当代的、Word Sense 读者可能完全没听过但已经在英语世界发生的事。

4. **处理 enshittification**:从同族词列表里去掉(最安全),或单独说一句它的特殊性。

5. **加入 Merriam-Webster 2024 认证**:让"同族词成族"这个判断有具体的语言学认证支撑。

## 查证带来的额外素材

- **梭罗原句**(已上)
- **Italian Brainrot 2025 现象**:Tralalero Tralala、Tung Tung Tung Sahur 等 AI 生成怪物成为新一轮浪潮。Hungary 总理 Orbán 都在 TikTok 上发过 Italian Brainrot 视频。
- **Merriam-Webster 2024 同时收入 doomscroll 和 brainrot**,可作为同族词"成族"的官方证据
```

---

## Step 3: 改写终稿(用 v3-rewrite 跑出来的)

**保存到** `output/brainrot/step-3-final.md`

```markdown
# 改写终稿

**字面含义** · brain + rot,字面是"脑子在腐烂"。Rot 这个词有强烈的画面感 —— 不是干净的损坏,是有机物腐败发酸、缓慢溃败的那种烂。所以 brainrot 的字面意象很刺激:脑子像放久了的水果一样在自己烂掉。

**本体质感** · 这个词最迷人的地方是它**带着自嘲、近乎躺平的姿态**。

它不是用来骂别人的(那是"脑残")。它的典型使用者**就是它描述的对象** —— 一个人说"I have such bad brainrot",意思是"我自己被算法和短视频喂废了,我知道,但我没打算停下来"。这种"我看清楚自己在干嘛但我接受这个状态"的姿态是 brainrot 的灵魂。

它跟"addiction"(上瘾)很不一样。addiction 是严肃的、病理化的、需要治疗的;brainrot 是日常化的、轻盈的、自我开玩笑的。说"我有 brainrot"几乎是社交润滑 —— 你在告诉对方"我跟你一样,我也在沉沦,我们坐在同一条船上"。

这个词还有几种衍生用法:

- **brainrot content**:指代某类内容本身(尤其是 TikTok 上那些极度无意义、视觉刺激密集的短视频)
- **X brainrot**:指某人过度沉迷某事物(Taylor Swift brainrot、Skibidi Toilet brainrot)

最有趣的元层面:**用 brainrot 这个词本身,就是 brainrot 的一部分**。它是一个 Gen Z / Gen Alpha 圈层的内部黑话,你知道这个词、你在用这个词,你就已经在那个圈子里。

**寻根溯源** · 这个词的来历比你想的有重量得多。

第一次在英语里出现"brain-rot",是在梭罗 1854 年的《瓦尔登湖》。书的结尾,他在批判同时代人对复杂思想的轻视,对照当时正在爱尔兰肆虐的马铃薯枯萎病,他写道:

> "While England endeavors to cure the potato-rot, will not any endeavor to cure the brain-rot, which prevails so much more widely and fatally?"
>
> (英国正努力医治马铃薯之腐,又有谁来医治那比之更广泛、更致命的——脑之腐?)

注意梭罗的关切跟今天的 brainrot 几乎是同一件事 —— 同时代精神生活在大众化的低质内容(当时是廉价小说和煽情报纸)的浸泡中逐渐退化。一百七十年后这个词以连写形式(brainrot)在互联网语境里复活,并不是巧合 —— 是因为他描述的那种状态没消失,只是换了载体。

时间线大致这样:2007 年第一次在 Twitter 上出现;2010 年代逐步流通;2020 年在 Discord 上成为 meme;2023 年随着 Skibidi Toilet 等病毒视频在 TikTok 爆发;2024 年牛津宣布它为年度词汇(使用频率从 2023 到 2024 涨了 230%);2025 年衍生出"Italian Brainrot"子流派 —— AI 生成的伪意大利怪物(Tralalero Tralala、Tung Tung Tung Sahur 之类)成为新一轮的浪潮。

**各路用法** · 这个词主要在日常和社媒场景出现,职场基本不用:

**[日常,跟朋友吐槽]**
I have such bad TikTok brainrot right now — I literally can't read a book for more than ten minutes.

**[社媒,典型用法]**
the skibidi toilet brainrot is real my 8-year-old nephew speaks in a different language now

**[社媒,自嘲式]**
sorry for the typo im running on three hours of sleep and pure brainrot

注意社媒例句里那种"低 effort"的写法 —— 全小写、没标点、不修语法。这种写法本身就和 brainrot 这个词的姿态高度一致:"我知道这不对但我懒得纠正"。

**原生思维** · 中文里没有这个概念。这是真正的"中文没有对应词"情况。

可以考虑的近似翻译都不够:

- "脑子坏掉了" —— 太字面,且听起来像真的骂人
- "信息过载" —— 学术词,完全没有 brainrot 的自嘲玩味
- "刷废了" —— 抓住了状态,但漏掉了 brainrot 也能指内容类型这一层
- "短视频毒害" —— 长辈视角,单向批判,brainrot 是用户自己嘴里说出来的

中文母语者表达类似意思时,通常用一连串的句式而不是单个词:"我最近抖音刷得脑子都不会转了"、"这种视频看多了人会变傻"、"我现在脑子里全是 XX"。中文承担 brainrot 功能的是这一整套句式,不是任何一个词。

更深一层 —— brainrot 这个词能存在,可能是因为英语世界相对成熟地形成了一种"承认自己被算法操控但继续躺平"的姿态语境,而中文公共语言里这种姿态相对少被直接命名。我们对短视频沉迷的讨论更多是家长视角(批判)或卫健视角(劝戒),用户自己嘴里说出来的、带嘲讽带接受的中性词不多。这是一种观察角度,未必能上升到普遍的文化结论。

**悟道时刻** · brainrot 属于 Gen Z 在做的一件大事:**给算法时代的新型精神状态命名**。同族词:

- doomscrolling(忍不住一直滑负面新闻)
- touch grass(去摸摸草,意思是别上网了)
- chronically online(过度上网的,"网瘾发作中")
- cooked(完蛋了,通常自嘲)
- down bad(陷得很深)

2024 年 Merriam-Webster 大字典正式收入了 doomscroll 和 brainrot,这一族词被语言学层面"认证"了 —— 它们不再只是网络梗,而是英语词汇的一部分。

这一族词的共同特点是:**它们命名的是数字时代独有的精神状态**。在前互联网时代根本不存在这些处境,所以也不需要这些词。识别出这一族,你看 Gen Z 的英文写作时会发现一个特征 —— 他们的词汇里很大一部分是在描述"我和我的屏幕之间发生了什么"。这是一代人语言遗产的一部分,跟 Boomer 时代留下来的工业词汇、Millennial 时代留下来的办公室词汇,处于完全不同的层。看懂这一族词,你能看懂一代人怎么试图理解他们自己的处境。

而梭罗 170 年前那个问题 —— "脑之腐,谁来医治?" —— 在今天读起来,仍然是悬在 Gen Z 头顶上的同一个问题。

---

# 改动说明

1. **寻根溯源整段重写** —— 原稿只说"据说梭罗用过",改写后**直接引用梭罗原句**(中英对照),并把它跟当时爱尔兰马铃薯枯萎病的具体语境一起呈现。这是查证报告"额外素材"里提供的最大增量(参见报告中的 ✅ 第 1 条 + "额外素材")。

2. **加入精确时间线** —— 把模糊的"2020 年代爆炸式流行"改成具体的时间节点(2007 → 2020 Discord → 2023 TikTok → 2024 牛津年度词 → 2025 Italian Brainrot)(参见报告中的 ⚠️ 第 2 条)。

3. **删除 enshittification** —— 它是 Cory Doctorow 2022 年造的特定词,跟其他自发演化的网络词不完全同源,删掉避免不必要的解释成本(参见报告中的 ⚠️ 第 4 条)。

4. **原生思维部分加谦逊措辞** —— "可能是因为"、"未必能上升到普遍的文化结论",按改写原则软化文化判断,因为这部分超出查证助手能验证的范围。

5. **悟道时刻末尾增加梭罗回响** —— 用"梭罗 170 年前的问题在今天仍然悬在头顶"做收尾,呼应寻根溯源的引用,形成文章首尾的内部互文。这是查证带来的额外创作机会。

6. **悟道时刻里加入 Merriam-Webster 2024 收录的细节** —— 让"同族词成族"这个判断有了具体的语言学认证支撑(参见报告中的 ⚠️ 第 4 条 + "额外素材")。

7. **保留其他大部分内容** —— 字面含义、本体质感、各路用法 这三个维度查证报告确认站得住,完全没动。
```

---

## 这个例子说明什么

- **Step 1 的初稿是 1500 字左右**,质量已经不错,但有几个未经验证的事实性断言(梭罗、时间线、同族词)
- **Step 2 的查证报告是 1200 字左右**,真的去查了 4 条断言,有 ✅ ⚠️ 两类结果,并提供"额外素材"
- **Step 3 的改写终稿比初稿增量约 30%**,主要因为加入了梭罗原句和 Italian Brainrot 2025 这些新素材

如果你的实现跑出来的三个文件长度和质量大致接近这个样本,工作流就算跑通了。

如果跑出来明显短得多或质量明显不行,大概率是 prompt 没正确加载,或者 Step 2 的工具调用没真正发生(模型在靠内部知识"假装查"了)。
