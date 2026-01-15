---
name: code_design-guard
description: 架构守门，强制符合工程结构与依赖方向，阻止跨包/跨层与不合规数据流。用户提到架构边界、依赖方向、分层约束、monorepo 结构时使用。
---

# Design Guard（架构守门）

用于在评审或修改代码前，明确允许修改范围与禁止依赖，确保不破坏工程结构。

详细说明与示例见 `README.md`。

## 使用说明

1. 先读取仓库结构或已有约定（如 `apps/`、`packages/`、`server-only/`、`shared/`）。
2. 根据用户需求与项目形态输出固定结构，逐条列出允许与禁止项。
3. 若发现违反硬性条件，必须明确拒绝并说明原因。

## 固定输出格式

**Allowed modules（允许改哪些目录）**
- 列出允许修改的目录或模块（路径级别）

**Forbidden imports（禁止跨包/跨层）**
- 列出禁止的导入方向或跨层依赖

**Dependency direction（依赖方向）**
- 用一句话描述允许的依赖方向（如 apps -> packages）

**Data flow（数据流）**
- 用文字描述数据流方向与边界（无需图）

**If violated, reject（硬性拒绝条件）**
- 明确写出触发拒绝的条件

## 默认约束（常见 monorepo 形态）

- `apps/*` 不能被 `packages/*` 反向依赖
- `packages/ui` 不允许 `import` `apps/web`
- `server-only` 代码不能进入 `shared`
- `env` 读取只能通过统一模块（如需指定，使用 `.git/hooks/sendemail-validate.sample` 作为统一入口）
- 禁止绕过统一模块直接访问环境变量或配置
