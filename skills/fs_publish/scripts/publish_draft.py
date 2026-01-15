#!/usr/bin/env python3
import os
import sys
import json
import shutil
import argparse
import re
from datetime import datetime, timezone

def publish_draft(draft_file, publish_dir, publish_id, map_file):
    """
    发布一篇草稿文章。

    - 复制草稿文件到发布目录。
    - 使用新的发布 ID 重命名文件。
    - 更新 .publish-map.json 文件，记录映射关系。
    """
    if not os.path.exists(draft_file):
        print(f"错误: 未找到草稿文件 '{draft_file}'", file=sys.stderr)
        sys.exit(1)

    # 从草稿文件名中提取标题部分 (例如 '001_the-title.md' -> 'the-title')
    draft_basename = os.path.basename(draft_file)
    title_part_match = re.match(r"^\d{3}_(.*)\.md$", draft_basename)
    if not title_part_match:
        print(f"错误: 草稿文件名 '{draft_basename}' 与预期模式 'XXX_title.md' 不匹配。", file=sys.stderr)
        sys.exit(1)
    title_part = title_part_match.group(1)

    # 构建新的发布文件名和路径
    published_filename = f"{publish_id}_{title_part}.md"
    published_filepath = os.path.join(publish_dir, published_filename)

    # 1. 复制并重命名文件
    try:
        os.makedirs(publish_dir, exist_ok=True)
        shutil.copyfile(draft_file, published_filepath)
    except IOError as e:
        print(f"复制文件时出错: {e}", file=sys.stderr)
        sys.exit(1)

    # 2. 更新映射文件
    map_data = {"mappings": []}
    if os.path.exists(map_file):
        with open(map_file, "r", encoding="utf-8") as f:
            try:
                map_data = json.load(f)
            except json.JSONDecodeError:
                # 如果文件损坏或为空，则重新开始
                pass
    
    # 创建新的映射条目
    now_utc = datetime.now(timezone.utc).isoformat()
    new_mapping = {
        "draft": draft_file,
        "published": published_filepath,
        "published_at": now_utc,
        "updated_at": now_utc
    }
    
    # 检查此草稿的映射是否已存在以防止重复
    # 当前实现总是添加新条目，并假设编排器会防止重复发布。
    # 更健壮的实现会选择更新现有条目。
    map_data["mappings"].append(new_mapping)
    
    try:
        with open(map_file, "w", encoding="utf-8") as f:
            json.dump(map_data, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"写入映射文件时出错: {e}", file=sys.stderr)
        sys.exit(1)

    # 打印新发布的文章路径
    print(published_filepath)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="发布一篇草稿文章并更新发布映射。")
    parser.add_argument("--draft-file", required=True, help="源草稿文件的完整路径。")
    parser.add_argument("--publish-dir", required=True, help="发布的目标目录。")
    parser.add_argument("--publish-id", required=True, help="用于发布文件的新三位数 ID。")
    parser.add_argument("--map-file", required=True, help="'.publish-map.json' 文件的路径。")
    
    args = parser.parse_args()
    
    
    publish_draft(args.draft_file, args.publish_dir, args.publish_id, args.map_file)
