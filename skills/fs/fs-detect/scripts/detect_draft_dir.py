#!/usr/bin/env python3
import os

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

def find_or_create_draft_dir():
    """
    根据项目约定，检测并返回草稿目录路径。

    优先级逻辑如下:
    1. docs/post_local/ （本地草稿，不提交）
    2. docs/post/ （公开目录）
    3. post/ (当前目录下的文章目录)
    4. 如果都不存在，则创建并使用 docs/post_local/

    如果目录不存在，会自动创建。
    返回绝对路径，确保在不同工作目录下都能正确使用。
    """
    # 找到项目根目录
    project_root = find_project_root()

    # 基于项目根构建候选路径
    post_local_dir = os.path.join(project_root, "docs", "post_local")
    post_dir = os.path.join(project_root, "docs", "post")
    current_post_dir = os.path.join(project_root, "post")

    # 按优先级检查目录是否存在
    if os.path.isdir(post_local_dir):
        draft_dir = post_local_dir
    elif os.path.isdir(post_dir):
        draft_dir = post_dir
    elif os.path.isdir(current_post_dir):
        draft_dir = current_post_dir
    else:
        # 如果都不存在，则选择最高优先级的目录作为创建目标
        draft_dir = post_local_dir

    # 确保草稿目录存在
    if not os.path.isdir(draft_dir):
        os.makedirs(draft_dir, exist_ok=True)

    # 返回绝对路径
    print(draft_dir)

if __name__ == "__main__":
    find_or_create_draft_dir()
