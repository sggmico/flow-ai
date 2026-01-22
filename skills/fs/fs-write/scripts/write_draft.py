#!/usr/bin/env python3
import os
import re
import sys
import argparse
import io

def find_project_root(start_path=None):
    """
    向上查找项目根目录（包含 .git, package.json, pyproject.toml 或 CLAUDE.md 的目录）

    Args:
        start_path: 开始查找的路径，默认为当前工作目录

    Returns:
        项目根目录的绝对路径，如果找不到则返回当前工作目录
    """
    if start_path is None:
        start_path = os.getcwd()

    current = os.path.abspath(start_path)

    # 项目根标志文件/目录
    root_markers = ['.git', 'package.json', 'pyproject.toml', 'CLAUDE.md', 'claude.md']

    # 向上查找，最多到文件系统根目录
    while True:
        # 检查是否存在任何项目根标志
        for marker in root_markers:
            if os.path.exists(os.path.join(current, marker)):
                return current

        # 到达文件系统根目录
        parent = os.path.dirname(current)
        if parent == current:
            # 找不到项目根，返回当前工作目录
            return os.getcwd()

        current = parent

def sanitize_filename(title):
    """
    将字符串转换为安全的文件名格式。

    - 空格替换为连字符。
    - 移除除非法字符 (仅保留字母、数字、连字符、下划线)。
    - 转换为小写。
    """
    s = title.strip().replace(" ", "-")
    s = re.sub(r"(?u)[^-\w.]", "", s)
    return s.lower()

def write_draft(directory, file_id, title, content, companion_content):
    """
    写入主草稿文件和可选的配套文件。
    """
    # 处理路径：如果是相对路径，基于项目根来解析
    if not os.path.isabs(directory):
        project_root = find_project_root()
        directory = os.path.join(project_root, directory)

    # 转换为绝对路径
    directory = os.path.abspath(directory)

    # 确保目录存在
    os.makedirs(directory, exist_ok=True)

    sanitized_title = sanitize_filename(title)
    base_filename = f"{file_id}_{sanitized_title}"
    
    # --- 主文章 ---
    main_filepath = os.path.join(directory, f"{base_filename}.md")
    try:
        with open(main_filepath, "w", encoding="utf-8") as f:
            f.write(content)
    except IOError as e:
        print(f"写入主文件时出错: {e}", file=sys.stderr)
        sys.exit(1)

    # --- 配套文章 (如果提供了内容) ---
    if companion_content:
        companion_filepath = os.path.join(directory, f"{base_filename}_扩展信息.md")
        try:
            with open(companion_filepath, "w", encoding="utf-8") as f:
                f.write(companion_content)
        except IOError as e:
            print(f"写入配套文件时出错: {e}", file=sys.stderr)
            sys.exit(1)
            
    # 打印已创建的主文件路径
    print(main_filepath)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="写入一篇草稿文章及其配套文件。")
    parser.add_argument("--dir", required=True, help="存放草稿文件的目标目录。")
    parser.add_argument("--id", required=True, help="文件的三位数 ID (例如 '001')。")
    parser.add_argument("--title", required=True, help="文章的标题。")
    parser.add_argument("--main-content-file", required=True, help="包含主内容的文件路径。")
    parser.add_argument("--companion-content-file", default="", help="（可选）包含配套内容的文件路径。")
    
    args = parser.parse_args()
    
    main_content = ""
    companion_content = ""

    try:
        with open(args.main_content_file, "r", encoding="utf-8") as f:
            main_content = f.read()
    except IOError as e:
        print(f"读取主内容文件时出错: {e}", file=sys.stderr)
        sys.exit(1)

    if args.companion_content_file:
        try:
            with open(args.companion_content_file, "r", encoding="utf-8") as f:
                companion_content = f.read()
        except IOError as e:
            print(f"读取配套内容文件时出错: {e}", file=sys.stderr)
            sys.exit(1)
        
    write_draft(args.dir, args.id, args.title, main_content, companion_content)
