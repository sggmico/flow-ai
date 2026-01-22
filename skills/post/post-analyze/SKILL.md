---
name: post-analyze
description: Use when 需要分析参考文章, 对比文章, 基于目录级资源或 OCR 图像生成综合方案或支撑融合写作时。
---

# Analyze References

对多篇参考文章做逐篇分析并生成可执行的综合创作方案。

## 快速开始

接收多篇文章全文（可用分隔符区分），输出 JSON 报告，供后续融合写作使用。

## 输入

- `REFERENCE_ARTICLES`: 多篇文章的完整内容(使用 `---` 或标题分隔)。
- `REFERENCE_DIR`: 目录路径(递归扫描, 见 references/dir-ingest.md)。

## 输出

只输出 JSON，包含：
- `article_analyses`：逐篇分析（结构、内容亮点、表达技巧、可改进）
- `synthesis_plan`：综合方案（架构、核心特色、差异化价值）
- `resource_index`：目录输入时的资源索引(可选)

## 分析流程

1. 逐篇深度分析：
   - 结构优点
   - 内容亮点
   - 表达技巧
   - 可改进之处
2. 设计综合方案：
   - 选择最优结构并说明理由
   - 列出 3-5 个核心特色（注明来源与价值）
   - 明确至少 3 个差异化价值点
3. 目录输入(可选):
   - 按 references/dir-ingest.md 生成 resource_index
   - OCR 结果作为强证据进入分析

## Quick Reference

| 输入类型 | 处理方式 | 产出 |
| --- | --- | --- |
| 多篇文章全文 | 逐篇分析 + 综合方案 | article_analyses, synthesis_plan |
| 目录路径 | 生成 resource_index + 相关性筛选 | resource_index, synthesis_plan |

## 输出示例（结构）

```json
{
  "article_analyses": [
    {
      "article_title": "参考文章标题",
      "structure_strengths": {
        "organization": "...",
        "sections": "...",
        "hierarchy": "...",
        "flow": "..."
      },
      "content_highlights": {
        "unique_perspective": "...",
        "depth": "...",
        "examples": "...",
        "innovation": "..."
      },
      "expression_techniques": {
        "metaphors": "...",
        "visuals": "...",
        "interaction": "...",
        "rhythm": "..."
      },
      "improvements": {
        "redundancy": "...",
        "gaps": "...",
        "clarity": "...",
        "practicality": "..."
      }
    }
  ],
  "synthesis_plan": {
    "content_architecture": {
      "structure": "...",
      "rationale": "...",
      "outline": ["..."]
    },
    "core_features": [
      {"feature": "...", "source": "...", "value": "..."}
    ],
    "differentiation": [
      {"difference": "...", "value": "..."}
    ]
  },
  "resource_index": [
    {"source": "...", "type": "...", "updated_at": "...", "summary": "...", "confidence": "..."}
  ]
}
```

## 注意事项

- 只输出 JSON，不附带其他文字。
- 分析必须具体，引用文章中的事实或例子。
- 差异化价值必须可执行、可验证。

## Common Mistakes

- 直接拼接目录全文导致 token 失控。
- 忽略 OCR 置信度标记，导致结论失真。
