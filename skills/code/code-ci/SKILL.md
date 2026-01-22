---
name: code-ci
description: 生成符合规范的 git 提交信息并完成本地提交（不推送），支持按文件类型自动拆分提交、检测混合提交、拦截敏感文件。用户提到“提交代码/提交信息/拆分提交/规范提交/Conventional Commits/ci”时使用。
---

# Code CI（规范提交助手）

为当前改动生成规范提交信息，并在需要时自动拆分为多次提交（不推送）。

详细说明与示例见 `README.md`。

## 指令流程

1. 检查改动：运行 `git status --short` 和 `git diff --stat` 收集改动概览。
2. 类型检测与拆分：
   - 提交拆分原则：优先按照功能完整性进行拆分。
   - 若检测到混合提交（3 种以上文件类型或 10+ 文件），先询问用户是否自动拆分或手动选择。
   - 若是单一类型改动，继续单次提交流程。
3. 每组文件智能分析：
   - 从路径推断 `type` 与 `scope`，生成 50 字以内、祈使语气的提交信息。
4. 安全检查：拦截 `.env`, `*.key`, `*.pem`, `secret/password/token` 等敏感文件。
5. 执行提交：
   - `git add <文件组>`
   - `git commit -m "<type>(<scope>): <描述>"`

## 提交类型与格式

- 类型：feat, fix, docs, refactor, perf, test, chore, style
- 常用 scope：api, ui, auth, db, config, deps
- Breaking Change：
  - `refactor(api)!: 重构认证接口`
  - 另起段落：`BREAKING CHANGE: 路径变更`
- 关联 Issue：`Closes #123`

## 交互原则

- 发现混合提交时，必须先征求是否自动拆分。
- 不推送远端，只做本地提交。
- 如果提交信息不确定，先给出 2–3 个备选让用户选。
- 提交信息优先使用中文，除非用户明确要求英文或项目规范要求英文。
