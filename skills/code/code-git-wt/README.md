# code-git-wt

通用 Git Worktree 管理工具, 支持多分支并行开发与共享配置.
默认不在主仓库创建共享项文件, 如需自动创建设置 `AUTO_CREATE_SHARED=true`.

## 快速开始

```bash
cd /path/to/project
~/.claude/skills/code-git-wt/scripts/worktree.sh add feature-auth
cd ../<项目名>-feature-auth
```

## 命令速查

| 命令 | 说明 | 示例 |
| --- | --- | --- |
| `init` | 初始化配置 | `~/.claude/skills/code-git-wt/scripts/worktree.sh init` |
| `add <name>...` | 创建 worktree | `~/.claude/skills/code-git-wt/scripts/worktree.sh add feature-login` |
| `remove <name>...` | 删除 worktree | `~/.claude/skills/code-git-wt/scripts/worktree.sh remove feature-login` |
| `list` | 列出 worktree | `~/.claude/skills/code-git-wt/scripts/worktree.sh list` |
| `status` | 检查共享状态 | `~/.claude/skills/code-git-wt/scripts/worktree.sh status` |
| `clean` | 清理所有 worktree | `~/.claude/skills/code-git-wt/scripts/worktree.sh clean` |
| `config` | 查看配置 | `~/.claude/skills/code-git-wt/scripts/worktree.sh config` |
| `help` | 帮助 | `~/.claude/skills/code-git-wt/scripts/worktree.sh help` |

## 典型场景

```bash
# 并行开发
~/.claude/skills/code-git-wt/scripts/worktree.sh add feature-login feature-payment

# 紧急修复
~/.claude/skills/code-git-wt/scripts/worktree.sh add hotfix-123

# 清理
~/.claude/skills/code-git-wt/scripts/worktree.sh clean
```

## 配置示例

```bash
~/.claude/skills/code-git-wt/scripts/worktree.sh init

PROJECT_NAME="my-app"
WORKTREE_BASE="../"
BRANCH_PREFIX="dev"
SHARED_ITEMS=(
  ".env"
  ".env.local"
  ".vscode/settings.json"
)
```

## 文档

- 使用说明: `references/user-guide.md`
- 脚本细节: `references/worktree-script.md`
- Skill 入口: `SKILL.md`
- 变更记录: `CHANGELOG.md`
