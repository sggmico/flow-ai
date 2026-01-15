#!/usr/bin/env python3
"""
FlowAI 一键迁移工具

让开发者可以快速将 FlowAI 工作流迁移到自己的项目中.
通过配置文件和环境变量, 自动替换 Skills 中的占位符.

用法:
    python3 scripts/migrate.py init          # 初始化配置文件
    python3 scripts/migrate.py check         # 检查配置完整性
    python3 scripts/migrate.py apply         # 应用配置到 Skills
    python3 scripts/migrate.py show          # 显示当前配置
    python3 scripts/migrate.py reset         # 重置为占位符 (需 git)
    python3 scripts/migrate.py diff          # 显示将要修改的内容

文档: docs/001_一键迁移方案.md
"""

import argparse
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# 尝试导入 yaml, 提供友好错误信息
try:
    import yaml
except ImportError:
    print("错误: 需要安装 PyYAML")
    print("请运行: pip install pyyaml")
    sys.exit(1)


class Colors:
    """终端颜色"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

    @classmethod
    def disable(cls):
        """禁用颜色 (用于非 TTY 环境)"""
        cls.RED = cls.GREEN = cls.YELLOW = cls.BLUE = cls.RESET = cls.BOLD = ''


# 非 TTY 环境禁用颜色
if not sys.stdout.isatty():
    Colors.disable()


class FlowAIMigrator:
    """FlowAI 迁移管理器"""

    CONFIG_FILE = "flowai.config.yaml"
    CONFIG_EXAMPLE = "flowai.config.example"
    ENV_FILE = ".flowai.env"
    ENV_EXAMPLE = ".flowai.env.example"
    SKILLS_DIR = "skills"

    # 占位符到配置键的映射
    PLACEHOLDER_MAP = {
        "${PUBLISH_DIR}": "paths.publish_dir",
        "${GITHUB_ORG}": "github.org",
        "${GITHUB_REPO}": "github.repo",
        "${GITHUB_PROJECT_ID}": "github.project_id",
        "${CR_OUTPUT_DIR}": "paths.cr_output_dir",
        "${DEFAULT_MODEL}": "defaults.model",
        "${UI_STACK}": "defaults.ui_stack",
    }

    # 必填配置项
    REQUIRED_CONFIGS = [
        ("paths.publish_dir", "文章发布目录"),
        ("github.org", "GitHub 组织名"),
        ("github.repo", "GitHub 仓库名"),
        ("github.project_id", "GitHub Project ID"),
    ]

    # 环境变量到配置键的映射
    ENV_MAP = {
        "FLOWAI_PUBLISH_DIR": "paths.publish_dir",
        "FLOWAI_GITHUB_ORG": "github.org",
        "FLOWAI_GITHUB_REPO": "github.repo",
        "FLOWAI_GITHUB_PROJECT_ID": "github.project_id",
        "FLOWAI_CR_OUTPUT_DIR": "paths.cr_output_dir",
        "FLOWAI_DEFAULT_MODEL": "defaults.model",
        "FLOWAI_UI_STACK": "defaults.ui_stack",
    }

    def __init__(self, project_root: Path, verbose: bool = False):
        self.root = project_root
        self.verbose = verbose
        self.config: Dict[str, Any] = {}

    def log(self, msg: str, level: str = "info") -> None:
        """日志输出"""
        prefix = {
            "info": f"{Colors.BLUE}[INFO]{Colors.RESET}",
            "success": f"{Colors.GREEN}[OK]{Colors.RESET}",
            "warning": f"{Colors.YELLOW}[WARN]{Colors.RESET}",
            "error": f"{Colors.RED}[ERROR]{Colors.RESET}",
        }.get(level, "")
        print(f"{prefix} {msg}")

    def debug(self, msg: str) -> None:
        """调试日志"""
        if self.verbose:
            print(f"{Colors.YELLOW}[DEBUG]{Colors.RESET} {msg}")

    # ========== 命令实现 ==========

    def init(self) -> int:
        """初始化配置文件"""
        config_path = self.root / self.CONFIG_FILE
        example_path = self.root / self.CONFIG_EXAMPLE

        if config_path.exists():
            self.log(f"配置文件已存在: {config_path}", "warning")
            response = input("是否覆盖? [y/N]: ").strip().lower()
            if response != 'y':
                self.log("已取消", "info")
                return 0

        # 从示例文件复制, 或生成默认配置
        if example_path.exists():
            shutil.copy(example_path, config_path)
            self.log(f"已从模板创建: {config_path}", "success")
        else:
            config = self._get_default_config()
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, allow_unicode=True, default_flow_style=False,
                          sort_keys=False)
            self.log(f"已创建配置文件: {config_path}", "success")

        print(f"\n{Colors.BOLD}下一步:{Colors.RESET}")
        print(f"  1. 编辑 {config_path} 填入您的实际配置")
        print(f"  2. 运行 python3 scripts/migrate.py check 验证配置")
        print(f"  3. 运行 python3 scripts/migrate.py apply 应用配置")

        return 0

    def check(self) -> int:
        """检查配置完整性"""
        self._load_config()

        print(f"\n{Colors.BOLD}配置检查结果:{Colors.RESET}")
        print("-" * 50)

        all_valid = True
        for key, desc in self.REQUIRED_CONFIGS:
            value = self._get_nested(self.config, key)
            is_valid = self._is_valid_value(value)

            status = f"{Colors.GREEN}✓{Colors.RESET}" if is_valid else f"{Colors.RED}✗{Colors.RESET}"
            display_value = str(value) if value else "(未设置)"

            # 截断过长的值
            if len(display_value) > 40:
                display_value = display_value[:37] + "..."

            print(f"  {status} {desc}")
            print(f"      键: {key}")
            print(f"      值: {display_value}")

            if not is_valid:
                all_valid = False

        print("-" * 50)

        if all_valid:
            self.log("配置检查通过!", "success")
            return 0
        else:
            self.log("请完善上述配置项", "error")
            print(f"\n提示: 编辑 {self.root / self.CONFIG_FILE}")
            return 1

    def apply(self) -> int:
        """应用配置到 Skills"""
        # 先检查配置
        self._load_config()

        missing = []
        for key, desc in self.REQUIRED_CONFIGS:
            value = self._get_nested(self.config, key)
            if not self._is_valid_value(value):
                missing.append(desc)

        if missing:
            self.log("配置不完整, 请先运行 check 命令", "error")
            return 1

        skills_dir = self.root / self.SKILLS_DIR
        if not skills_dir.exists():
            self.log(f"Skills 目录不存在: {skills_dir}", "error")
            return 1

        print(f"\n{Colors.BOLD}应用配置到 Skills:{Colors.RESET}")

        modified_count = 0
        for skill_file in skills_dir.rglob("SKILL.md"):
            if self._apply_to_file(skill_file):
                modified_count += 1

        if modified_count > 0:
            self.log(f"已更新 {modified_count} 个文件", "success")
        else:
            self.log("没有需要更新的文件", "info")

        return 0

    def show(self) -> int:
        """显示当前配置"""
        self._load_config()

        print(f"\n{Colors.BOLD}当前配置:{Colors.RESET}")
        print("-" * 50)

        # 显示所有配置项
        all_keys = [
            ("paths.publish_dir", "发布目录"),
            ("paths.cr_output_dir", "评审输出目录"),
            ("github.org", "GitHub Org"),
            ("github.repo", "GitHub Repo"),
            ("github.project_id", "GitHub Project ID"),
            ("defaults.model", "默认模型"),
            ("defaults.article_style", "文章风格"),
            ("defaults.article_level", "技术难度"),
            ("defaults.article_length", "文章长度"),
            ("defaults.ui_stack", "UI 技术栈"),
        ]

        for key, desc in all_keys:
            value = self._get_nested(self.config, key)
            is_required = any(k == key for k, _ in self.REQUIRED_CONFIGS)
            is_valid = self._is_valid_value(value)

            if is_required:
                status = f"{Colors.GREEN}✓{Colors.RESET}" if is_valid else f"{Colors.RED}✗{Colors.RESET}"
            else:
                status = f"{Colors.BLUE}○{Colors.RESET}"

            display_value = str(value) if value else "(默认)"
            print(f"  {status} {desc}: {display_value}")

        print("-" * 50)
        print(f"\n配置文件: {self.root / self.CONFIG_FILE}")
        print(f"环境变量: {self.root / self.ENV_FILE}")

        return 0

    def reset(self) -> int:
        """重置为占位符"""
        skills_dir = self.root / self.SKILLS_DIR

        if not skills_dir.exists():
            self.log(f"Skills 目录不存在: {skills_dir}", "error")
            return 1

        print(f"\n{Colors.BOLD}重置 Skills 为占位符:{Colors.RESET}")
        print("提示: 使用 git 恢复原始文件")
        print()

        for skill_file in skills_dir.rglob("SKILL.md"):
            rel_path = skill_file.relative_to(self.root)
            print(f"  git checkout {rel_path}")

        print()
        response = input("是否执行上述命令? [y/N]: ").strip().lower()

        if response == 'y':
            import subprocess
            for skill_file in skills_dir.rglob("SKILL.md"):
                rel_path = skill_file.relative_to(self.root)
                result = subprocess.run(
                    ["git", "checkout", str(rel_path)],
                    cwd=self.root,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    self.log(f"已重置: {rel_path}", "success")
                else:
                    self.log(f"重置失败: {rel_path}", "error")
                    self.debug(result.stderr)

        return 0

    def diff(self) -> int:
        """显示将要修改的内容"""
        self._load_config()

        skills_dir = self.root / self.SKILLS_DIR
        if not skills_dir.exists():
            self.log(f"Skills 目录不存在: {skills_dir}", "error")
            return 1

        print(f"\n{Colors.BOLD}将要修改的内容:{Colors.RESET}")

        has_changes = False
        for skill_file in skills_dir.rglob("SKILL.md"):
            changes = self._get_file_changes(skill_file)
            if changes:
                has_changes = True
                rel_path = skill_file.relative_to(self.root)
                print(f"\n{Colors.BLUE}{rel_path}:{Colors.RESET}")
                for old, new in changes:
                    print(f"  {Colors.RED}- {old}{Colors.RESET}")
                    print(f"  {Colors.GREEN}+ {new}{Colors.RESET}")

        if not has_changes:
            self.log("没有需要修改的内容", "info")

        return 0

    # ========== 辅助方法 ==========

    def _load_config(self) -> None:
        """加载配置"""
        config_path = self.root / self.CONFIG_FILE

        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f) or {}
            self.debug(f"已加载配置: {config_path}")
        else:
            self.config = {}
            self.debug("配置文件不存在, 使用默认值")

        # 加载环境变量覆盖
        self._load_env_overrides()

    def _load_env_overrides(self) -> None:
        """加载环境变量覆盖"""
        # 先加载 .flowai.env 文件
        env_file = self.root / self.ENV_FILE
        if env_file.exists():
            self._parse_env_file(env_file)
            self.debug(f"已加载环境变量: {env_file}")

        # 然后应用系统环境变量
        for env_key, config_key in self.ENV_MAP.items():
            value = os.environ.get(env_key)
            if value:
                self._set_nested(self.config, config_key, value)
                self.debug(f"环境变量覆盖: {env_key} -> {config_key}")

    def _parse_env_file(self, path: Path) -> None:
        """解析 .env 文件"""
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"\'')
                    os.environ[key] = value

    def _get_nested(self, d: dict, key: str) -> Any:
        """获取嵌套键值"""
        keys = key.split('.')
        for k in keys:
            if isinstance(d, dict) and k in d:
                d = d[k]
            else:
                return None
        return d

    def _set_nested(self, d: dict, key: str, value: Any) -> None:
        """设置嵌套键值"""
        keys = key.split('.')
        for k in keys[:-1]:
            d = d.setdefault(k, {})
        d[keys[-1]] = value

    def _is_valid_value(self, value: Any) -> bool:
        """检查值是否有效 (非占位符)"""
        if value is None:
            return False
        str_value = str(value)
        # 检查是否是占位符或示例值
        invalid_patterns = [
            "${",
            "/path/to",
            "YourOrg",
            "your-",
            "example",
        ]
        return not any(p in str_value for p in invalid_patterns)

    def _get_default_config(self) -> dict:
        """获取默认配置"""
        return {
            "version": "1.0",
            "paths": {
                "publish_dir": "${PUBLISH_DIR}",
                "cr_output_dir": "docs/cr_local/",
                "draft_dirs": [
                    "docs/post_local/",
                    "docs/post/",
                    "post/",
                ],
            },
            "github": {
                "org": "${GITHUB_ORG}",
                "repo": "${GITHUB_REPO}",
                "project_id": 1,
            },
            "defaults": {
                "model": "sonnet",
                "article_style": "tutorial",
                "article_level": "intermediate",
                "article_length": "medium",
                "ui_stack": "html-tailwind",
            },
        }

    def _apply_to_file(self, path: Path) -> bool:
        """应用配置到单个文件"""
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        for placeholder, config_key in self.PLACEHOLDER_MAP.items():
            value = self._get_nested(self.config, config_key)
            if value and placeholder in content:
                content = content.replace(placeholder, str(value))

        if content != original:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            rel_path = path.relative_to(self.root)
            self.log(f"已更新: {rel_path}", "success")
            return True

        return False

    def _get_file_changes(self, path: Path) -> List[Tuple[str, str]]:
        """获取文件将要进行的更改"""
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        changes = []
        for placeholder, config_key in self.PLACEHOLDER_MAP.items():
            if placeholder in content:
                value = self._get_nested(self.config, config_key)
                if value and self._is_valid_value(value):
                    changes.append((placeholder, str(value)))

        return changes


def main():
    parser = argparse.ArgumentParser(
        description="FlowAI 一键迁移工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 scripts/migrate.py init     # 初始化配置
  python3 scripts/migrate.py check    # 检查配置
  python3 scripts/migrate.py apply    # 应用配置
  python3 scripts/migrate.py show     # 显示配置
  python3 scripts/migrate.py diff     # 预览更改
  python3 scripts/migrate.py reset    # 重置为占位符

文档: docs/001_一键迁移方案.md
        """
    )

    parser.add_argument(
        "command",
        choices=["init", "check", "apply", "show", "reset", "diff"],
        help="要执行的命令"
    )
    parser.add_argument(
        "--root", "-r",
        default=".",
        help="项目根目录 (默认: 当前目录)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="显示详细日志"
    )

    args = parser.parse_args()

    # 确定项目根目录
    root = Path(args.root).resolve()

    # 如果从 scripts/ 目录运行, 自动调整到项目根
    if root.name == "scripts" and (root.parent / "skills").exists():
        root = root.parent

    migrator = FlowAIMigrator(root, verbose=args.verbose)

    commands = {
        "init": migrator.init,
        "check": migrator.check,
        "apply": migrator.apply,
        "show": migrator.show,
        "reset": migrator.reset,
        "diff": migrator.diff,
    }

    try:
        sys.exit(commands[args.command]())
    except KeyboardInterrupt:
        print("\n已取消")
        sys.exit(130)
    except Exception as e:
        migrator.log(f"发生错误: {e}", "error")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
