---
name: multi-agent-discussion
description: "suit-for-ai-research-assistant: Conduct file-based debate when the user requests a multi-agent discussion or a response to another agent. Write only the assigned agent file, quote claims accurately, and preserve evidence labels and human arbitration."
---

# Multi-Agent Discussion Protocol

## 目的

多个 AI agent（Claude / DeepSeek / Codex 等）与人类围绕一个 topic 进行多轮结构化讨论。通过迭代辩论、互相质疑、补充盲点，让想法越来越清晰，最终收敛为经过压力测试的共识方案。

**核心理念**：真理越辩越明，想法越迭代越清晰。

## 参与者

- **人类（mux）**：提出 topic、给定 persona（optional）、仲裁分歧、做最终决策
- **AI agents**：各自独立思考，互相质疑，不预设主从关系

## 机制

### 文件结构

```
agents-human-discussion/
  {topic}-{date}/           # e.g. ae-pretrain-for-fprop-2026-06-06
    claude_said.md          # Claude 的发言
    ds_said.md              # DeepSeek 的发言
    codex_said.md           # Codex 的发言
    final.md                # 讨论收敛后的 summary（人类指示下撰写）
```

### 读写规则

1. **写**：每个 agent 只写自己的 `*_said.md`。可以追加多轮（用 `# Round N` 分隔）
2. **读**：每个 agent 可以自由阅读**任何**其他 agent 写的 `.md` 文件
3. **回应**：在自己的 `*_said.md` 里撰写对其他 agent 或对人类的回应。引用对方原话再反驳，不 strawman

### 发言格式

```markdown
# {Agent名} → {回应对象} (Round N, {date})

## Agreement
引用原话，说明同意什么、为什么

## Pushback
引用原话，说明不同意什么、给替代方案

## 补充
对方没提到但重要的点
```

### Persona（可选）

人类可以在发起讨论时给每个 agent 指定 persona / 思考角度（如"你从数学角度想"、"你从工程角度想"）。未指定时各自独立判断。

### 讨论流程

```
1. 人类发起 topic，可选指定 persona
2. 各 agent 撰写初始观点到各自的 *_said.md
   **约束：第一轮（Round 1）每个 agent 不回应任何其他 agent 的发言，应当直面人类提出的议题独立阐述自己的意见。** 这确保每个 agent 的初始观点是独立的，不被最先发言的 agent 的框架带偏。
3. 人类路由：让某个 agent 去读另一个 agent 的发言并回应
   （具体路由方式由人类掌握——可以是直接转述、可以是让 agent 自己去读文件）
4. 多轮迭代，直到收敛或人类判断够了
5. 人类指示某个 agent（或自己）撰写 final.md
```

### Final Summary（`final.md`）

讨论收敛后，在人类的指示下撰写。包含：

```markdown
# {Topic} — Discussion Summary

## 参与者与日期
## 问题背景
## 最终共识方案
## 各方关键贡献（谁提出了什么、谁纠正了什么）
## 未解决的分歧（如有）
## 待定设计点
## 相关文件引用
```

### 深度调查（Deep Research）

讨论中遇到文献/技术不确定性时，任何 agent 可以请求深度调查。

**流程**：
1. Agent 撰写调查 prompt 到讨论目录下的 `{topic}_deepresearch_prompt.md`
2. 人类把 prompt 发给调查用模型（GPT / Perplexity / 其他）
3. 人类把结果保存到 `{topic}_report_{research_model}.md`（如 `film_report_gpt.md`）
4. 各 agent 可自由阅读调查报告，在自己的 `*_said.md` 里引用和回应

**写 prompt 的原则**：
- 明确写出调查背景（当前讨论的 context、已知信息、已排除的方案）
- 列出具体的调查目标（不是泛泛的"调查一下 X"，而是"X 在 Y 条件下是否成立，特别关注 Z"）
- 附上搜索关键词建议
- 说明期望的输出格式（每篇 paper 要什么信息、是否需要公式/代码）

**命名惯例**：
```
agents-human-discussion/{topic}-{date}/
  {subtopic}_deepresearch_prompt.md    # 调查 prompt
  {subtopic}_report_{model}.md         # 调查结果（人类保存）
```

### Evidence Discipline（沿用项目标准）

讨论中同样遵守 evidence discipline：
- `[Observation]`：从代码、log、实验输出验证过的事实
- `[Claim (source)]`：经核对的文献陈述
- `[Data]`：实验 run 中的具体数字
- `[Hypothesis]`：未验证的推理，标注置信度和可验证方式

### 讨论纪律

- 引用对方原话再反驳，不 strawman 成更弱的版本
- 区分 evidence 与 speculation
- 同意就明说，不同意给替代方案
- 一次一个主题，不混杂
- 决策权在人类
