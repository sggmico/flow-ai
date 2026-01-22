---
name: fs-detect
description: 检测或创建文章草稿目录并输出路径。用于用户要获取草稿目录、初始化草稿目录或写入草稿前的准备步骤时。
---

# Detect Draft Dir

检测项目中的草稿目录并在必要时创建。

## 快速开始

运行脚本并输出草稿目录路径。

## 用法

```bash
python scripts/detect_draft_dir.py
```

## 输出

- 草稿目录路径（相对路径或绝对路径）。

## 规则

- 优先级：`docs/post_local/` → `docs/post/` → `post/` (当前目录)。
- 若都不存在，则创建并使用 `docs/post_local/`。

## 要求

- Python 3
