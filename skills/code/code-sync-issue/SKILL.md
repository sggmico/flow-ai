---
name: code-sync-issue
description: 整理当前迭代的更新项并同步到 GitHub Issues 与 Projects 看板, 使用 GitHub MCP 和 Playwright 远程更新状态, 适用于用户要求更新项目看板或 Issue 状态, 同步任务进度, 或依据 docs/task.md 与最新提交进行远程状态同步的场景.
---

# Code Remote Update

## 概述

用于把本地或当前迭代的完成项整理为可更新清单, 并远程同步到 GitHub Issues 列表与 Projects 看板. 输出中文优先, 必要时补充英文术语或原名.

## 配置与默认值

为降低调用成本, 默认使用以下占位符与默认值. 用户可只覆盖变更项.

- org: LearnFlowAI
- repo: starter
- project_id: 1
- project_url: https://github.com/orgs/{org}/projects/{project_id}
- issues_url: https://github.com/{org}/{repo}/issues?q=sort:updated-desc+is:issue+is:open

在接到任务时, 若用户未提供这些参数, 直接使用默认值. 若用户提供完整 URL, 解析并覆盖对应参数.

## 工作流

1. 评估当前进度并更新 docs/task.md
2. 补充收集迭代变化
3. 生成更新清单
4. 更新 Issues
5. 更新 Projects 看板
6. 复核并回报

## 具体步骤

### 1. 评估当前进度并更新 docs/task.md

- 先评估当前项目实际进度, 明确已完成/进行中/阻塞项.
- 将评估结果更新到 docs/task.md, 确保后续同步以该文件为准.
- 如 docs/task.md 不存在或不清晰, 先确认路径与格式再继续.

### 2. 补充收集迭代变化

- 优先读取当前仓库的迭代来源, 例如 docs/task.md, 最近提交, 用户提供的完成列表.
- 若信息不完整, 先向用户确认要更新的 Issue 编号或完成范围.

### 3. 生成更新清单

- 输出待更新的 Issue 列表, 包含编号, 标题, 目标状态.
- 避免重复更新, 若存在重复 Issue, 记录并说明处理策略.
- 读取 docs/task.md 的进度后, 映射出可更新的 Issues 与 Projects 状态.

### 4. 更新 Issues

- 使用 GitHub MCP 获取开放 Issue 列表或搜索结果.
- 对已完成项执行关闭操作, 优先使用 state_reason=completed.
- 需要说明时添加简短中文评论, 记录依据与变更来源.

### 5. 更新 Projects 看板

- 仅使用 Playwright 更新 Projects 看板.
- 若出现登录页或 404, 先提示用户完成登录后再继续.
- 在看板中定位 Issue 行, 更新 Status 字段为 Done 或对应完成状态.

### 6. 复核并回报

- 确认 Issues 与 Projects 状态一致.
- 汇总已更新的 Issue 编号与状态结果.
- 如发现未覆盖项或权限问题, 明确指出并请求下一步指令.

## 输出规范

- 中文优先, 必要时附英文术语.
- 使用简洁列表报告更新结果.
- 不要关闭或移动未经确认的事项.
- 降低调用成本: 优先使用 docs/task.md 与用户提供的编号列表, 再做最小范围的查询.

## 工具使用指引

- Issues 更新: 使用 GitHub MCP 的 list_issues 或 search_issues 获取列表, 再用 issue_write 更新状态.
- Projects 更新: 使用 Playwright 导航并操作看板, 必要时等待用户登录.
