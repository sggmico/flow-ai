---
name: fs_write
description: 将文章内容写入草稿文件并生成可选配套文件。用于用户要求写入草稿、保存文章到草稿目录或生成扩展信息文件时。
---

# Write Draft

根据标题与内容生成草稿文件名，并写入主文章与可选配套内容。

## 快速开始

```bash
python scripts/write_draft.py \
  --dir <draft_dir> \
  --id <file_id> \
  --title "文章标题" \
  --main-content-file <main.md> \
  --companion-content-file <companion.md>
```

## 输入

- `--dir`：草稿目录路径。
- `--id`：三位数 ID。
- `--title`：文章标题。
- `--main-content-file`：主文章内容文件。
- `--companion-content-file`：可选配套内容文件。

## 输出

- 主草稿文件路径。

## 说明

- 文件名格式：`{ID}_{sanitized_title}.md`。
- 如果有配套内容，生成 `{ID}_{sanitized_title}_扩展信息.md`。
- 可直接把 `--dir` 指定为用户目标目录（如 `/Users/.../post/...`），避免在默认草稿目录再复制一份。

## 要求

- Python 3
