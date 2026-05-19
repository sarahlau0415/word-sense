# 查证报告: deprecate

## 待查事实清单

1. “`deprecate` 最早的画面不是‘贬低’，而是‘把某事祈求走’：来自拉丁语 *deprecari*，大意是‘通过祈求来避开、求免除’。”
2. “`deprecate` 的核心质感不是大声骂，而是‘撤销背书’。”
3. “在正式语境里，`to deprecate something` 像是……这个做法不值得鼓励。”
4. “它比 `criticize` 更书面、更克制，也比 `condemn` 轻。”
5. “在技术语境里，`deprecated` 很常见。”
6. “它不是‘已经不能用’，而是‘还能用，但官方不再推荐；未来可能会移除’。”
7. “`supported` → `discouraged` → `deprecated` → `removed`” 这个梯度。
8. “`self-deprecating`……更像是在社交里主动把自己放低一点，用幽默、谦逊或自嘲降低压力。”
9. “`deprecate` 和 `depreciate` 长得像，但气质不同。”
10. “`depreciate` 更偏‘价值下降’：房子、货币、资产、设备都可以 `depreciate`。”
11. “`deprecate` 更偏‘评价/认可被撤回’：一个做法、说法、功能、习惯被人认为不该再推。”
12. “`The car depreciated quickly.` / `This method has been deprecated.` 这两个例句所表达的区别：一个是价值缩水，一个是不推荐使用。”
13. “英语母语者用 `deprecate` 时，脑子里常常不是在做‘骂’这个动作，而是在处理‘许可、推荐、认可’的状态。”
14. “技术英语特别爱用 `deprecated`。代码世界里很多东西不是一夜之间死掉的。它们先被标记为‘你还能用，但别再新用了’。”
15. “`self-deprecating` 也是同一个底层动作，只不过对象变成了自己……不是彻底否定自己，而是一种社交上的降压动作。”
16. 文中例句 “The committee deprecated the old reporting practice …” 是否符合 `deprecate` 可用于“做法 / practice”的事实用法。

## 查证过程

我主要查了四类来源：

- **词源**：Etymonline、Merriam-Webster、Oxford Learner’s Dictionaries。Etymonline 明确给出 `deprecate` 1620s 的英语早期义为“pray against / pray the removal or deliverance from”，来自拉丁 *deprecari* “to pray something away”；Merriam-Webster 也给出拉丁 *deprecari* “to avert by prayer”。([etymonline.com](https://www.etymonline.com/word/deprecate))
- **现代普通义**：Merriam-Webster、Cambridge、Oxford、Britannica。它们均收录 “express disapproval / not approve / feel and express strong disapproval / criticize or express disapproval” 等义项；Merriam-Webster 还收录 “play down / belittle / disparage”。([merriam-webster.com](https://www.merriam-webster.com/dictionary/deprecate))
- **技术语境**：Merriam-Webster 词典和专文、Oxford、MDN、Microsoft、Python PEP。它们均支持 “deprecated = no longer recommended / no longer in active development / may be removed in future / may still work or still ship” 这一技术含义。([merriam-webster.com](https://www.merriam-webster.com/dictionary/deprecate))
- **`depreciate` 与 `self-deprecating`**：Oxford、Merriam-Webster、Cambridge、Britannica。`depreciate` 的核心义为“价值下降 / 降低资产账面价值”，但也有“使显得不重要、贬低”的重叠义；`self-deprecating` 多被解释为让自己的能力、成就或自己显得不重要，常见搭配包括 humor/humour。([oxfordlearnersdictionaries.com](https://www.oxfordlearnersdictionaries.com/us/definition/english/depreciate))

## 用户可见来源

- Etymonline: https://www.etymonline.com/word/deprecate
- Merriam-Webster — deprecate: https://www.merriam-webster.com/dictionary/deprecate
- Merriam-Webster — A New Meaning of “Deprecate”: https://www.merriam-webster.com/wordplay/deprecate
- Oxford Learner’s Dictionaries — deprecate: https://www.oxfordlearnersdictionaries.com/us/definition/english/deprecate
- Oxford Learner’s Dictionaries — depreciate: https://www.oxfordlearnersdictionaries.com/us/definition/english/depreciate
- MDN Web Docs — Experimental, deprecated, and obsolete: https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Experimental_deprecated_obsolete
- Microsoft Learn — Windows client features lifecycle: https://learn.microsoft.com/en-us/windows/whats-new/feature-lifecycle
- Cambridge Dictionary — self-deprecating: https://dictionary.cambridge.org/dictionary/english/self-deprecating

## 查证结果

### ✅ 证实（可保留）

- **断言 1**：`deprecate` 的词源说明基本准确。
  - 证据来源: https://www.etymonline.com/word/deprecate、https://www.merriam-webster.com/dictionary/deprecate、https://www.oxfordlearnersdictionaries.com/us/definition/english/deprecate
  - 关键证据: Etymonline 说 `deprecate` 1620s 的早期义是“pray against or for deliverance from”，来自拉丁 *deprecari* “to pray (something) away”；Merriam-Webster 给出 “to avert by prayer”；Oxford 给出早期义 “pray against”。([etymonline.com](https://www.etymonline.com/word/deprecate))

- **断言 3**：`deprecate` 在正式语境中表示“不赞成 / 表达反对”是准确的。
  - 证据来源: https://dictionary.cambridge.org/us/dictionary/english/deprecate、https://www.oxfordlearnersdictionaries.com/us/definition/english/deprecate、https://www.britannica.com/dictionary/deprecate
  - 关键证据: Cambridge 标注为 formal，释义为 “to not approve of something or say that you do not approve”；Oxford 释义为 “to feel and express strong disapproval”；Britannica 释义为 “to criticize or express disapproval”。([dictionary.cambridge.org](https://dictionary.cambridge.org/us/dictionary/english/deprecate))

- **断言 5 + 6**：技术语境中 `deprecated` 的解释“仍可能可用，但不再推荐，未来可能移除”准确。
  - 证据来源: https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Experimental_deprecated_obsolete、https://learn.microsoft.com/en-us/windows/whats-new/feature-lifecycle、https://www.oxfordlearnersdictionaries.com/us/definition/english/deprecate、https://peps.python.org/pep-0004/
  - 关键证据: MDN 说 deprecated API/technology “no longer recommended”，可能未来移除，也可能因兼容性保留并仍可工作；Microsoft 说 deprecation 是“不再 active development，可能在未来版本移除”；Oxford 说软件功能 “best avoided, even though you can still use it”；Python PEP 4 说 deprecated module “may be removed from a future Python release”。([developer.mozilla.org](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Experimental_deprecated_obsolete))

- **断言 9 + 10**：`deprecate` 与 `depreciate` 形近但核心义不同；`depreciate` 常表示价值下降。
  - 证据来源: https://www.oxfordlearnersdictionaries.com/us/definition/english/depreciate、https://www.merriam-webster.com/dictionary/depreciate、https://www.etymonline.com/word/deprecate
  - 关键证据: Oxford 对 `depreciate` 的第一义是“to become less valuable over a period of time”，例子包括 cars、shares、Sterling、peso；Merriam-Webster 也给出 “to lower the price or estimated value of / to fall in value”。([oxfordlearnersdictionaries.com](https://www.oxfordlearnersdictionaries.com/us/definition/english/depreciate))

- **断言 11 + 12**：`deprecate` 可表示对某物不赞成，技术上可表示撤回官方支持 / 不再推荐；例句 `This method has been deprecated.` 的解释正确。
  - 证据来源: https://www.merriam-webster.com/dictionary/deprecate、https://www.oxfordlearnersdictionaries.com/us/definition/english/deprecate、https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Experimental_deprecated_obsolete
  - 关键证据: Merriam-Webster 技术义为 “withdraw official support for or discourage the use of”；Oxford 技术义说软件功能 outdated and best avoided；MDN 说 no longer recommended。([merriam-webster.com](https://www.merriam-webster.com/dictionary/deprecate))

- **断言 14**：技术英语中 `deprecated` 表示“中间状态：不推荐但未必死亡 / 移除”成立。
  - 证据来源: https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Experimental_deprecated_obsolete、https://learn.microsoft.com/en-us/windows-server/get-started/removed-deprecated-features-windows-server、https://learn.microsoft.com/en-us/windows/whats-new/feature-lifecycle
  - 关键证据: MDN 区分 deprecated 与 obsolete；Microsoft Server 文档说 deprecated component “still ships”、仍可用于生产部署并继续获得安全和质量更新；Microsoft lifecycle 文档区分 deprecation、end of support、retirement、remove。([developer.mozilla.org](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Experimental_deprecated_obsolete))

- **断言 16**：`deprecate` 可以用于“做法 / practice / method / use”等对象；例句方向成立。
  - 证据来源: https://dictionary.cambridge.org/us/dictionary/english/deprecate、https://www.britannica.com/dictionary/deprecate、https://www.merriam-webster.com/dictionary/deprecate
  - 关键证据: Cambridge 例句有 “We deprecate this use of company funds…”、“Physicians strongly deprecate the use of hair dyes”；Britannica 有 “the deprecation of old methods”；Merriam-Webster 例句也有 deprecates attempts at humor。([dictionary.cambridge.org](https://dictionary.cambridge.org/us/dictionary/english/deprecate))

### ⚠️ 部分证实（需软化或细化）

- **断言 2**：“核心质感不是大声骂，而是‘撤销背书’。”
  - 实际情况: “不是大声骂”是教学性概括，词典不能直接验证；但 `deprecate` 的确包括 “express disapproval” 和技术义 “withdraw official support / discourage use”。“撤销背书”非常适合解释技术义，但对普通义来说可能略窄，因为普通义还包括“批评、不赞成、贬低 / 淡化”。([merriam-webster.com](https://www.merriam-webster.com/dictionary/deprecate))
  - 建议改写方向: 可改为“在技术语境里尤其像‘撤销背书’；在普通正式语境里则是‘表达不赞成 / 不鼓励’。”

- **断言 4**：“它比 `criticize` 更书面、更克制，也比 `condemn` 轻。”
  - 实际情况: “更书面”有来源支持：Cambridge、Oxford、Britannica 都标注或体现 formal；“比 condemn 轻 / 更克制”属于语感和语用强度判断，词典释义能间接支持，但无法严格量化查证。([dictionary.cambridge.org](https://dictionary.cambridge.org/us/dictionary/english/deprecate))
  - 建议改写方向: 改成“通常更正式；很多语境下语气不像 `condemn` 那样强烈”，避免绝对化。

- **断言 7**：`supported` → `discouraged` → `deprecated` → `removed` 的梯度。
  - 实际情况: `deprecated` 与 `removed` 的区别有强来源支持；`deprecated` “不再推荐 / 可能未来移除”也有来源支持。但 `discouraged` 并非所有技术文档中的正式生命周期状态，更多是作者为了学习而搭的理解梯度。([developer.mozilla.org](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Experimental_deprecated_obsolete))
  - 建议改写方向: 保留为“可以这样粗略理解”，不要写成所有技术生态的正式标准。

- **断言 8 + 15**：`self-deprecating` 是自嘲式降低自己、用幽默或谦逊降低压力，不等于沉重的自我否定。
  - 实际情况: 词典支持“让自己的能力 / 成就 / 自己显得不重要”“disparage or undervalue oneself”，也支持常见搭配 `self-deprecating humor/humour`；但“降低社交压力”“不是彻底否定自己”属于语用解释，不能由词典完全证明。([merriam-webster.com](https://www.merriam-webster.com/dictionary/self-deprecating))
  - 建议改写方向: 可写成“常见于 humor/humour 等搭配，通常是把自己的能力或成就说得轻一点；至于是否在‘降压’，要看具体语境。”

- **断言 9 + 11 的对比**：`depreciate` 是价值下降，`deprecate` 是背书撤销。
  - 实际情况: 大方向正确，但需要提醒：两词语义有历史和现代重叠。Merriam-Webster 的 `deprecate` 收录 “make little of / belittle / disparage”；`depreciate` 也可表示 “to lower in honor or esteem” 或 formal “make something seem unimportant”。Merriam-Webster 专文还明确说这两个词长期被混淆，`self-deprecating` 原先曾是 `self-depreciating`。([merriam-webster.com](https://www.merriam-webster.com/dictionary/deprecate))
  - 建议改写方向: 保留“核心差异”，但加一句“不过在‘贬低 / 看轻’这一义上两者有重叠，不能说完全互不相通。”

### ❓ 无法确认（建议删除或标“一种说法”）

- **断言 13**：“英语母语者用 `deprecate` 时，脑子里常常不是在做‘骂’这个动作，而是在处理‘许可、推荐、认可’的状态。”
  - 搜索情况: 词典和技术文档能支持 `deprecate` 的“express disapproval”和技术义“withdraw official support / discourage use”，但无法验证“母语者脑子里常常……”这种心理过程判断。
  - 建议: 改成“在技术语境里，可以把它理解为在处理‘推荐 / 支持 / 认可’状态”，避免声称母语者心理活动。

- **“很多中国学习者看到 `deprecated` 会以为是‘废弃的’”**
  - 搜索情况: 这属于学习者群体的经验判断，未查到可靠语料或调查数据支持。
  - 建议: 可软化为“学习时容易误解为‘已经废弃 / 不能用’”。

### ❌ 证伪（必须改）

- 暂未发现必须证伪的核心断言。主要问题不是事实错误，而是若干表达把“教学性隐喻 / 语感判断”写得过于像客观事实。

## 改写建议

1. 词源段可保留，并可更精确写成：`deprecate` 进入英语约在 17 世纪早期，早期义为“pray against / pray for deliverance from”，来自拉丁 *deprecari* “to pray something away / avert by prayer”。
2. “撤销背书”适合解释技术义，但不宜作为 `deprecate` 全部核心义。建议写成：“在普通正式语境里是‘表达不赞成 / 不鼓励’；在技术语境里尤其像‘撤销官方背书’。”
3. “比 `criticize` 更书面”可保留；“比 `condemn` 轻”建议软化为“通常不像 `condemn` 那样强烈”。
4. 技术段建议保留，且可以加一句：“不同项目的 deprecation policy 不完全一样，但常见含义是 no longer recommended / may be removed later / may still work for compatibility。”
5. `supported → discouraged → deprecated → removed` 这组梯度建议前加“粗略可以这样理解”，避免被误读为正式通用标准。
6. `deprecate` vs `depreciate` 对比应加一句限定：“不过两者在‘贬低 / 看轻’义上有重叠，尤其在非技术语境里不能机械切分。”
7. `self-deprecating` 段可保留，但把“降低压力 / 不危险 / 不难接近”等心理和社交效果标成解释性描述，而不是词典事实。
8. “母语者脑子里……”建议改成“在很多技术文本里，与其把它理解成‘骂’，不如把它理解成‘官方不再推荐 / 不再背书’。”
9. “很多中国学习者……”建议改成“学习者容易把它误解成‘已经不能用’”，除非另有学习者调查来源。
10. 职场会议例句 `The committee deprecated the old reporting practice...` 可保留，但它偏正式、书面；若想更自然一点，可改成 “The committee formally deprecated the old reporting practice...” 或 “The committee formally discouraged the old reporting practice...”。

## 查证带来的额外素材

- **技术义进入词典的时间点**：Merriam-Webster 专文写明，`deprecate` 的技术义 “was added in June 2018”；同文还列出 1984 年计算机用户使用 `deprecated` 描述 obsolescent technology 的早期例子。这个素材可以增强“技术义如何出现”的时间线。来源: https://www.merriam-webster.com/wordplay/deprecate ([merriam-webster.com](https://www.merriam-webster.com/wordplay/deprecate))
- **`self-deprecating` 的早期记录**：Merriam-Webster 给出 `self-deprecating` first known use 为 1834；Etymonline 给出 1835，并解释为 “expressed disapproval of oneself”。来源: https://www.merriam-webster.com/dictionary/self-deprecating、https://www.etymonline.com/word/deprecate ([merriam-webster.com](https://www.merriam-webster.com/dictionary/self-deprecating))
- **可加入一个“别过度切分”的提醒**：Merriam-Webster 专文指出 `deprecate` 与 `depreciate` 长期被混淆，且 `self-deprecating` 原先曾是 `self-depreciating`。这能让文章更准确：两词核心不同，但历史上并非完全泾渭分明。来源: https://www.merriam-webster.com/wordplay/deprecate ([merriam-webster.com](https://www.merriam-webster.com/wordplay/deprecate))