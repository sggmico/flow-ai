---
name: publish_local-blog
description: 发布草稿到目标目录并更新映射，确保发布文件名优先来自文章内一级标题，缺失时才用原文件名。
---

# Publish Local Blog

将草稿移动到正式目录，并在映射文件维护历史记录。

## 快速开始

```bash
python scripts/publish_draft.py \
  --draft-file <draft.md> \
  --publish-dir <publish_dir> \
  --publish-id <publish_id_or_empty> \
  --map-file <map.json>
```

## 输入

- `--draft-file`：草稿文件路径。
- `--publish-dir`：发布目录。
- `--publish-id`：发布用三位数 ID；留空则自动使用发布目录内的下一个序号。
- `--map-file`：发布映射文件路径（如 `.publish-map.json`）。

## 命名策略

1. 优先读取草稿内的第一个一级标题（`# 标题`），严格遵循“中文优先”原则：保留标题中的中文字符，空格/标点统一替换为连字符，移除非法字符后作为 slug。
2. 如果找不到一级标题或标题为空，回退到原有的 `ID_title` 文件名部分。
3. 整个过程尽量只扫描文件前 2KB 内容，以保持 token 友好且控制执行成本。

## 输出

- 发布后的文件路径。
- 如果草稿已发布过，会直接报错并停止。

## 要求

- Python 3
