#!/usr/bin/env python3
import os
import sys
import json
import shutil
import argparse
import re
import unicodedata
from datetime import datetime, timezone

PUBLISHED_PATTERN = re.compile(r"^(\d{3})_.*\.md$")
HEADING_PATTERN = re.compile(r"^#\s+(.+)$")

def get_next_publish_id(publish_dir):
    """
    根据发布目录内已有文件的最大序号计算下一个发布 ID。
    """
    if not os.path.isdir(publish_dir):
        return "001"

    max_id = 0
    for filename in os.listdir(publish_dir):
        match = PUBLISHED_PATTERN.match(filename)
        if match:
            current_id = int(match.group(1))
            if current_id > max_id:
                max_id = current_id

    return f"{max_id + 1:03d}"

def load_map(map_file):
    map_data = {"mappings": []}
    if os.path.exists(map_file):
        with open(map_file, "r", encoding="utf-8") as f:
            try:
                map_data = json.load(f)
            except json.JSONDecodeError:
                pass
    return map_data

def extract_first_heading(draft_file, max_chars=2048):
    """
    只读取文件前 2KB 内容，在其中寻找第一个一级标题。
    """
    bytes_read = 0
    with open(draft_file, "r", encoding="utf-8") as f:
        for line in f:
            bytes_read += len(line)
            match = HEADING_PATTERN.match(line.strip())
            if match:
                return match.group(1).strip()
            if bytes_read >= max_chars:
                break
    return None


def slugify(value):
    if not value:
        return None
    normalized = unicodedata.normalize("NFKC", value).strip().lower()

    def is_chinese(ch):
        return "\u4e00" <= ch <= "\u9fff" or "\u3400" <= ch <= "\u4dbf"

    parts = []
    for ch in normalized:
        if is_chinese(ch):
            parts.append(ch)
        elif ch.isascii():
            if ch.isalnum():
                parts.append(ch)
            elif ch in "-_":
                parts.append(ch)
            elif ch.isspace():
                parts.append("-")
            else:
                parts.append("-")
        else:
            parts.append("-")

    slug = re.sub(r"-+", "-", "".join(parts)).strip("-")
    return slug or None


def find_existing_mapping(map_data, draft_file):
    for mapping in map_data.get("mappings", []):
        if mapping.get("draft") == draft_file:
            return mapping
    return None

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

    # 读取映射，防止重复发布同一草稿
    map_data = load_map(map_file)
    existing_mapping = find_existing_mapping(map_data, draft_file)
    if existing_mapping:
        print(
            f"错误: 草稿已发布过，发布文件为 '{existing_mapping.get('published')}'",
            file=sys.stderr,
        )
        sys.exit(1)

    # 计算发布 ID（若未提供）
    publish_id = (publish_id or "").strip()
    if not publish_id:
        publish_id = get_next_publish_id(publish_dir)

    # 若目标发布文件已存在，则阻止覆盖
    if os.path.isdir(publish_dir):
        for filename in os.listdir(publish_dir):
            match = PUBLISHED_PATTERN.match(filename)
            if match and match.group(1) == publish_id:
                print(
                    f"错误: 发布 ID '{publish_id}' 已存在，请使用其他 ID。",
                    file=sys.stderr,
                )
                sys.exit(1)

    # 基于文章标题(优先)构建 slug
    heading = extract_first_heading(draft_file)
    slug_candidate = slugify(heading) or slugify(title_part) or title_part
    if not slug_candidate:
        print("错误: 无法从草稿文件名或内容中生成合法标题", file=sys.stderr)
        sys.exit(1)

    # 构建新的发布文件名和路径
    published_filename = f"{publish_id}_{slug_candidate}.md"
    published_filepath = os.path.join(publish_dir, published_filename)

    # 1. 复制并重命名文件
    try:
        os.makedirs(publish_dir, exist_ok=True)
        shutil.copyfile(draft_file, published_filepath)
    except IOError as e:
        print(f"复制文件时出错: {e}", file=sys.stderr)
        sys.exit(1)

    # 2. 更新映射文件
    # 创建新的映射条目
    now_utc = datetime.now(timezone.utc).isoformat()
    new_mapping = {
        "draft": draft_file,
        "published": published_filepath,
        "published_at": now_utc,
        "updated_at": now_utc
    }
    
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
    parser.add_argument(
        "--publish-id",
        default="",
        help="用于发布文件的新三位数 ID。留空则自动使用发布目录内的下一个序号。",
    )
    parser.add_argument("--map-file", required=True, help="'.publish-map.json' 文件的路径。")
    
    args = parser.parse_args()
    
    
    publish_draft(args.draft_file, args.publish_dir, args.publish_id, args.map_file)
