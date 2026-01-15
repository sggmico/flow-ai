---
name: code_git-wt
description: 使用 scripts/worktree.sh 管理 Git worktree, 适用于并行开发、多分支独立工作区、批量创建或清理 worktree、共享配置文件等场景。用户提到创建或删除 worktree、并行开发、不切换分支修 bug、管理 worktree、清理 worktree 时使用。
---

# Git Worktree 管理

## 执行入口

- 推荐使用技能脚本直调用(无侵入): `~/.claude/skills/code_git-wt/scripts/worktree.sh <command>`
- 如需项目内脚本再复制: `cp ~/.claude/skills/code_git-wt/scripts/worktree.sh ./`
- 仅在 Git 仓库根目录执行
- 依赖: Git, Bash, Python 3
- 默认不自动创建共享项, 避免改动主仓库; 如需创建, 设置 `AUTO_CREATE_SHARED=true`

## 快速流程

1. 在仓库根目录检查是否已有 `./worktree.sh`.
2. 若需零侵入, 直接用脚本绝对路径执行即可.
3. 需要自定义时执行 `./worktree.sh init` 生成 `.worktree.config`.
4. 按目标命令执行.

## 命令

- `init`: 生成或更新 `.worktree.config`.
- `add <name>...`: 创建一个或多个 worktree.
- `remove <name>...`: 删除一个或多个 worktree.
- `list`: 列出 worktree.
- `status`: 检查共享软链接状态.
- `clean`: 清理所有 worktree.
- `config`: 打印当前配置.
- `help`: 显示帮助.

## 默认行为

- 项目名: 自动检测
- Worktree 路径: `../<项目名>-<分支名>`
- 分支前缀: `dev/`
- 默认共享: `.env`, `.env.local`

## 安全约束

- `remove`/`clean`/删除分支前必须征询用户确认.
- 禁止绕过确认(例如 `yes | ./worktree.sh clean`).
- 创建前检查目标路径是否存在.

## 常见任务处理

- 并行开发: `./worktree.sh add feature-a feature-b`
- 紧急修复: `./worktree.sh add hotfix-<id>`
- 清理无用 worktree: `./worktree.sh clean`

## 参考

- 使用说明与示例: `references/user-guide.md`
- 脚本细节与安全机制: `references/worktree-script.md`
- 变更记录: `CHANGELOG.md`
