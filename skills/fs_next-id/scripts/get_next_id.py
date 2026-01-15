#!/usr/bin/env python3
import os
import re
import sys

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

def get_next_id(directory):
    """
    在给定目录中为新文章计算下一个可用的序列 ID。

    Args:
        directory (str): 需要扫描 .md 文件的目录路径（支持相对路径和绝对路径）。

    脚本会扫描匹配 'XXX_*.md' 模式的文件名,
    找到当前最大的序列号, 并打印下一个序列号 (格式化为三位补零的字符串)。
    """
    # 处理路径：如果是相对路径，基于项目根来解析
    if not os.path.isabs(directory):
        project_root = find_project_root()
        directory = os.path.join(project_root, directory)

    # 转换为绝对路径
    directory = os.path.abspath(directory)

    if not os.path.isdir(directory):
        # 如果目录不存在 (例如草稿目录刚被创建), 则从 1 开始。
        print("001")
        return

    max_id = 0
    # 用于匹配 "001_title.md" 这类文件名的正则表达式 (Regex)
    pattern = re.compile(r"^(\d{3})_.*\.md$")

    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            current_id = int(match.group(1))
            if current_id > max_id:
                max_id = current_id

    next_id = max_id + 1
    # 打印下一个 ID, 补零至三位数
    print(f"{next_id:03d}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法: ./get_next_id.py <目录路径>", file=sys.stderr)
        sys.exit(1)
    
    target_directory = sys.argv[1]
    get_next_id(target_directory)
