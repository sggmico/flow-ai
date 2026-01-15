---
name: post_prep
description: 总结长文本并提取关键信息，输出结构化摘要。用于用户提到总结、摘要、提炼要点、会话记录整理或文章要点提取时。
---

# Summarize Content

将长文本提炼为结构化摘要，为后续写作或分析提供清晰输入。

## 快速开始

先获取原始文本，然后输出包含核心概念、关键决策、可执行步骤和最终结果的摘要。

## 输入

- `RAW_CONTENT`：需要总结的原始文本（会话、文章、文档等）。

## 输出

结构化摘要，包含以下四个部分：
- Core Concepts
- Key Decisions
- Actionable Steps
- Final Outcome

## 评审流程

1. 只做摘要，不写正文或扩展观点。
2. 保持结构化标题，信息简洁但完整。
3. 重点保留可执行步骤、关键决策与结论。
4. 避免重复与无关细节。

## 示例

输入：一段较长的技术会话或多篇文章合集。
输出：
```markdown
## Core Concepts
- ...

## Key Decisions
- ...

## Actionable Steps
1. ...

## Final Outcome
...
```

## 最佳实践

- 输入越完整，摘要越稳定。
- 保留原文中的关键数据与约束条件。
