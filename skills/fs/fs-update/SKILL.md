---
name: fs-update
description: 根据草稿更新已发布文章并刷新映射时间。用于用户提到更新发布文章、同步草稿到发布版本或修订已发布内容时。
---

# Update Published

根据草稿内容更新已发布文章，并更新映射文件的时间戳。

## 快速开始

```bash
python scripts/update_published.py \
  --draft-file <draft.md> \
  --map-file <map.json>
```

## 输入

- `--draft-file`：草稿文件路径。
- `--map-file`：发布映射文件路径（如 `.publish-map.json`）。

## 输出

- 更新结果信息。

## 要求

- Python 3
