---
name: fs_publish
description: 发布草稿文章到目标目录并更新映射文件。用于用户要求发布文章、从草稿生成正式发布版本或维护发布记录时。
---

# Publish Draft

复制草稿到发布目录，重命名并写入发布映射。

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

## 输出

- 发布后的文件路径。
- 如果草稿已发布过，会直接报错并停止。

## 要求

- Python 3
