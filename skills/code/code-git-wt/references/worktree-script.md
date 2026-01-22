# Worktree 脚本细节

## 概述

通用 Git worktree 管理脚本, 适用于任意仓库的多分支并行开发与共享配置.

## 配置加载

优先级:
1. `.worktree.config`
2. 默认值

配置项:

| 配置项 | 默认值 | 说明 |
| --- | --- | --- |
| `PROJECT_NAME` | 自动检测 | 用于 worktree 目录名 |
| `WORKTREE_BASE` | `../` | worktree 基础路径 |
| `BRANCH_PREFIX` | `dev` | 分支前缀 |
| `SHARED_ITEMS` | `.env`, `.env.local` | 共享文件/目录 |
| `AUTO_CREATE_SHARED` | `false` | 是否自动创建共享项 |

## 命令行为要点

- `init`: 生成 `.worktree.config`, 若存在需确认覆盖.
- `add <name>...`:
  - 创建或复用分支 `${BRANCH_PREFIX}/${name}`.
  - 创建 worktree 目录 `${WORKTREE_BASE}${PROJECT_NAME}-${name}`.
  - 为共享项创建相对路径软链接.
- `remove <name>...`:
  - 交互确认删除 worktree.
  - 可选删除对应分支(需确认).
- `list`: 直接调用 `git worktree list`.
- `status`: 检查共享项是否为软链接.
- `clean`: 删除所有非主目录 worktree, 可选删除所有 `${BRANCH_PREFIX}/*`.
- `config`: 输出当前配置与共享项.

## 共享机制

- 共享项通过相对路径软链接指向主仓库.
- 主目录不存在的共享项会被跳过.
- 若 worktree 内已有同名文件, 会先移除再创建软链接.

## 安全与前置检查

- 必须在有效 Git 仓库内执行.
- 创建前检查目标路径是否存在.
- 破坏性操作(删除 worktree/分支/clean)需要交互确认.
 - 默认不自动创建共享项, 避免改动主仓库; 如需创建, 设置 `AUTO_CREATE_SHARED=true`.

## 依赖

- Git: worktree 功能
- Bash: 脚本运行
- Python 3: 计算相对路径

## 参考

- Git worktree 文档: https://git-scm.com/docs/git-worktree
