---
name: fs_next-id
description: 计算草稿目录中下一个可用的三位数文章 ID。用于用户提到获取新文章编号、下一篇 ID 或序号生成时。
---

# Get Next ID

扫描目录中 `XXX_*.md` 文件，返回下一个三位数 ID。

## 快速开始

```bash
python scripts/get_next_id.py <draft_dir>
```

## 输入

- `<draft_dir>`：草稿目录路径。

## 输出

- 三位数 ID（例如 `001`）。

## 要求

- Python 3
