# MISSION: <survey title> — <one-line scope / lens>

授权：<who>，<date>。镜头=<technique-transfer / domain-mapping / failure-mode>（写清是哪种视角，避免变成领域铺陈）；规模=<~N 篇>；搜索 <sonnet/haiku>、精读 <opus>；<是否设 cron / 是否本 session 同步跑完>。

## 阶段

1. **搜索**（轻量模型并行，N 角度）→ 每角度写 `findings-<角度>.md`，目标 8-12 篇/角度。
2. **排重 + 下载**（主循环）→ 跨角度去重、排除已有（见排重清单）、选定 ~N 篇、PDF 下到 `reference/<topic>/`、生成 `review-manifest.md`（编号表：# | Title | Venue+Year | Primary angle | PDF filename | Note filename）。可旁出 `<topic>.bib`。
3. **精读**（强模型，≤4 篇/agent，幂等）→ 笔记写 `ai-survey-notes/<YYYY-MM>/`，frontmatter `status: reading` / `origin: ai-survey`，tag 加 `ai-survey` + 主题 tag；杂谈节=迁移分析（高/中/低 + 具体机制 + 命中哪个 transfer target + 风险）。笔记格式见 `references/literature-survey.md`。
4. **核验 + 综述 + 汇报** → 全量 verify（`verify-wf.js`，逐篇对 PDF，FIXED/PASS/FLAG，就地改）→ 每族 digest（`digest-wf.js`）→ 合成 `synthesis-draft.md` → 写 vault research log → 终检链接（0 死链）→ proactive 汇报。

## 规则

1. 模型：搜索用轻量、精读/撰写/核验用强模型、不指定的禁止。
2. 笔记规范：`references/literature-survey.md` 的 "Per-paper note format"。
3. 检索纪律：peer-reviewed 优先、venue 从论文核实、read-before-claim、负面结果一等公民、收敛 ≥2 源、originals over surveys。
4. AI 不设 `status: read`（那是人亲读后才翻）；log 里不记哪个 AI 干的（人是作者）。
5. 综述引用 AI 笔记标「出自 AI 精读，未亲核」。
6. <项目特定红线，例如：不碰服务器代码、不跑训练>。

## N 角度（每角度带迁移钩子）

> 每个角度 = 一个 `findings-<key>.md` + digest-wf.js / verify-wf.js 的 manifest "Primary angle"。钩子写清「从本项目视角，这个角度要找什么」。

- A. `<key>` — <技术族关键词>；钩子=<项目视角下要找什么>。
- B. `<key>` — …；钩子=…。
- …

## 排重清单（搜索 agent 须排除）

- 已有笔记：<列已存在的 AI-survey / human-read 笔记>。
- 已有 PDF：<列 reference/ 下已有的>。
- Zotero 相关分类：<列分类>——跳过通用基础综述。

## STATE

> 每阶段完成后在此打勾 + 留断点信息（task/run id、文件落点）。这是断点续跑的依据。

- [ ] 阶段1 搜索：
- [ ] 阶段2 排重+下载：
- [ ] 阶段3 精读：
- [ ] 阶段3.5 全量验证：
- [ ] 阶段4 综述+汇报：

## RESUME（usage limit 中断后断点续跑）

**checkpoint = 文件系统**。每篇笔记写到 `ai-survey-notes/<YYYY-MM>/` 即落盘，不依赖 session / workflow 内存。精读 workflow 须幂等：每个 agent 写前先查目标笔记是否已完整，是则 SKIP。中断后重发同一 script 只补缺的。

续跑步骤：
1. 查进度：`bash check-progress.sh`（先填好里面的 MANIFEST / NOTEDIR）→ 打印 已写 / 缺失 + 缺失笔记名。
2. 有缺失就重发精读 workflow（幂等，已完成秒 SKIP）：`Workflow({scriptPath: "<精读 wf 脚本路径>"})`。同一 session 内可加 `resumeFromRunId` 用缓存；跨 session 缓存失效，靠幂等 STEP 0 跳过已写的。
3. 精读齐了 → 阶段3.5 verify → 阶段4 digest + synthesis + log + 终检。

> 注：用 `name: '<workflow>'` + args 调 workflow 可能失败（args 未注入 `args` 全局 → context undefined）。稳妥做法：内联 script 把 context / angles 写死，agent 自己 Write 到 findings / notes 文件。
