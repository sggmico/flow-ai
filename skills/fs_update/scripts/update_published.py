#!/usr/bin/env python3
import os
import sys
import json
import shutil
import argparse
from datetime import datetime, timezone

def update_published(draft_file, map_file):
    """
    根据草稿内容，更新一篇已发布的文章。

    - 读取发布映射 (.publish-map.json) 来查找已发布文章的路径。
    - 检查草稿的修改时间是否晚于上次更新时间。
    - 复制草稿内容覆盖已发布的文章。
    - 更新映射中的 'updated_at' 时间戳。
    """
    if not os.path.exists(draft_file):
        print(f"错误: 未找到草稿文件 '{draft_file}'", file=sys.stderr)
        sys.exit(1)
        
    if not os.path.exists(map_file):
        print(f"错误: 未找到映射文件 '{map_file}'，无法更新。", file=sys.stderr)
        sys.exit(1)

    # 1. 读取映射文件
    with open(map_file, "r", encoding="utf-8") as f:
        try:
            map_data = json.load(f)
        except json.JSONDecodeError:
            print(f"错误: 无法解析映射文件 '{map_file}'。", file=sys.stderr)
            sys.exit(1)

    # 2. 查找映射关系
    mapping_index = -1
    for i, mapping in enumerate(map_data.get("mappings", [])):
        if os.path.normpath(mapping.get("draft")) == os.path.normpath(draft_file):
            mapping_index = i
            break
            
    if mapping_index == -1:
        print(f"错误: 未找到草稿 '{draft_file}' 对应的已发布文章，请先发布。", file=sys.stderr)
        sys.exit(1)
        
    target_mapping = map_data["mappings"][mapping_index]
    published_filepath = target_mapping.get("published")
    
    # 3. 验证修改时间
    draft_mtime_utc = datetime.fromtimestamp(os.path.getmtime(draft_file), tz=timezone.utc)
    last_update_utc = datetime.fromisoformat(target_mapping.get("updated_at"))
    
    if draft_mtime_utc <= last_update_utc:
        print(f"信息: 草稿 '{os.path.basename(draft_file)}' 不比上次发布版本新，无需操作。", file=sys.stdout)
        sys.exit(0)

    # 4. 复制内容
    try:
        shutil.copyfile(draft_file, published_filepath)
    except (IOError, shutil.SameFileError) as e:
        print(f"更新已发布文件时出错: {e}", file=sys.stderr)
        sys.exit(1)

    # 5. 在映射中更新时间戳并写回
    now_utc_iso = datetime.now(timezone.utc).isoformat()
    map_data["mappings"][mapping_index]["updated_at"] = now_utc_iso
    
    try:
        with open(map_file, "w", encoding="utf-8") as f:
            json.dump(map_data, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"写入已更新的映射文件时出错: {e}", file=sys.stderr)
        sys.exit(1)
        
    print(f"成功更新 '{published_filepath}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="根据草稿内容更新一篇已发布的文章。")
    parser.add_argument("--draft-file", required=True, help="源草稿文件的完整路径。")
    parser.add_argument("--map-file", required=True, help="'.publish-map.json' 文件的路径。")
    
    args = parser.parse_args()
    update_published(args.draft_file, args.map_file)
