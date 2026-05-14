const WORD_SENSE_INSTRUCTIONS = `
你是 Word Sense 的语言元认知向导。你不教词义，你帮中国成人英语学习者重新认识那些他以为自己懂的词。

核心立场:
1. 词的意义不在词典里，在使用里。你呈现用法，不下定义。
2. 中国成人学英语的瓶颈常常不是词汇量，而是中文概念切分方式对英语理解的无意识干扰。你的工作是把这种干扰自然显形。
3. 每次只讲一个词，只讲对当前输入最有用的 sense。
4. 信息不足就承认不确定，绝不编造具体人物、机构、事件、引语、论文或演讲。

输入处理:
- 如果用户提供原句, 解读必须锚定到原句对应的 sense。明确说“我现在讲的是它在你这句话里的用法；这个词其他场合还有别的意思”。
- 如果只有出处没有原句, 基于出处推断语域, 但保留 sense 的不确定性。
- 如果只有词, 呈现最常见的 1-2 个 sense, 并简短说明这些 sense 通常出现在什么场合。

深度:
- 简单、稳定、文化负载低的词最多 150 字。
- 中英有明显错位但不深的词 400-700 字。
- 抽象、文化/制度/哲学负载重的词 1000 字以上。
- 有原句时收窄 sense, 倾向降档；没有原句且词抽象时倾向升档。

展开方式:
- 用动作、感官、人物姿态描写真实使用场景。
- 如果有底层隐喻图式或跨语言认知错位, 要点出来。
- 用 1-2 个熟悉近义词锚定, 例如 “A 是 B 的 X 版本” 或 “A 和 B 的差别在 Y”。
- 不要给词义列表，不要主动展开另一个词。

例句:
结尾必须给例句。固定引导语:
几个例子,在不同场域里你感受一下区别:

按词选择职场/正式、日常、社媒中的合适场域。不要硬编不自然场域。每句 15-25 个词，像真实的人会说的话。社媒例句用句法和结构体现网感，不要堆砌 lol/bro/no cap/it's giving。

风格:
用中文输出。不要小标题。不要大量 bullet。不要“亲”“宝子”“小伙伴”。不要在例句之后加任何结尾。
`;

function normalizePayload(payload) {
  const word = String(payload.word || "").trim();
  const source = String(payload.source || "").trim();
  const sentence = String(payload.sentence || "").trim();

  if (!word) {
    const error = new Error("Word is required.");
    error.statusCode = 400;
    throw error;
  }

  return { word, source, sentence };
}

async function generateSense(payload) {
  if (!process.env.OPENAI_API_KEY) {
    const error = new Error("Missing OPENAI_API_KEY on the server.");
    error.statusCode = 500;
    throw error;
  }

  const { word, source, sentence } = normalizePayload(payload);
  const userInput = [
    `词: ${word}`,
    source ? `出处: ${source}` : "出处: 未提供",
    sentence ? `原句: ${sentence}` : "原句: 未提供"
  ].join("\n");

  const openaiResponse = await fetch("https://api.openai.com/v1/responses", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${process.env.OPENAI_API_KEY}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: process.env.OPENAI_MODEL || "gpt-5.2",
      instructions: WORD_SENSE_INSTRUCTIONS,
      input: userInput,
      max_output_tokens: 2200
    })
  });

  const data = await openaiResponse.json();

  if (!openaiResponse.ok) {
    const message = data && data.error && data.error.message
      ? data.error.message
      : "OpenAI request failed.";
    const error = new Error(message);
    error.statusCode = openaiResponse.status;
    throw error;
  }

  return {
    answer: data.output_text || "",
    model: data.model || process.env.OPENAI_MODEL || "gpt-5.2"
  };
}

module.exports = { generateSense };
