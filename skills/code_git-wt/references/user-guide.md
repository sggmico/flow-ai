# Git Worktree 用户指南

## 快速开始

```bash
# 进入项目
cd /path/to/project

# 可选: 初始化配置
~/.claude/skills/code_git-wt/scripts/worktree.sh init

# 创建 worktree
~/.claude/skills/code_git-wt/scripts/worktree.sh add feature-auth
```

进入新目录:

```bash
cd ../<项目名>-feature-auth
```

## 命令速查

```bash
~/.claude/skills/code_git-wt/scripts/worktree.sh init                 # 生成 .worktree.config
~/.claude/skills/code_git-wt/scripts/worktree.sh add <name>...         # 创建 worktree
~/.claude/skills/code_git-wt/scripts/worktree.sh remove <name>...      # 删除 worktree(需确认)
~/.claude/skills/code_git-wt/scripts/worktree.sh list                  # 列表
~/.claude/skills/code_git-wt/scripts/worktree.sh status                # 共享软链接检查
~/.claude/skills/code_git-wt/scripts/worktree.sh clean                 # 清理所有 worktree(需确认)
~/.claude/skills/code_git-wt/scripts/worktree.sh config                # 当前配置
~/.claude/skills/code_git-wt/scripts/worktree.sh help                  # 帮助
```

## 配置

`.worktree.config` 最小示例:

```bash
PROJECT_NAME="my-app"
```

完整示例:

```bash
PROJECT_NAME="my-app"
WORKTREE_BASE="../"
BRANCH_PREFIX="dev"
SHARED_ITEMS=(
  ".env"
  ".env.local"
  ".vscode/settings.json"
)
AUTO_CREATE_SHARED="false"
```

## 典型场景

- 并行开发多个功能:
  - `~/.claude/skills/code_git-wt/scripts/worktree.sh add feature-login feature-pay`
- 紧急修复且不打断当前分支:
  - `~/.claude/skills/code_git-wt/scripts/worktree.sh add hotfix-<id>`
- 清理无用 worktree:
  - `~/.claude/skills/code_git-wt/scripts/worktree.sh clean`

## 常见问题

- 提示未找到 Python:
  - 安装 Python 3(如 macOS: `brew install python3`).
- 目标路径已存在:
  - 换名称或手动删除目录.
- 软链接状态异常:
  - 删除并重建 worktree 或手动修复软链接.
