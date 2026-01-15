---
name: code_style-linter-guard
description: 规范化输出，强制统一命名、文件组织、错误处理、日志与类型严谨度。用户提到代码风格、规范化、lint/format、TypeScript 严格性时使用。
---

# Style Linter Guard（规范化输出）

用于把代码输出收敛到可机器验证的统一风格，强调硬规则而非建议。

详细说明与示例见 `README.md`。

## 使用说明

1. 读取仓库规范或已有约定（若无则使用默认硬规则）。
2. 严格输出固定结构与硬性规则，不给“可选项”。
3. 若现有代码与硬规则冲突，直接指出并要求修正。

## 固定输出格式

**Naming（命名约定）**
- 使用一致的命名风格（例如：文件与目录 `kebab-case`，类型 `PascalCase`，函数/变量 `camelCase`）
- 禁止使用模糊缩写；缩写必须有说明

**File structure（文件组织）**
- 相关类型、实现与测试放在同层级或规定目录
- 禁止跨层引用与随意新增“杂项”目录

**Error handling（错误处理模式）**
- API 返回统一 `Result<T, E>` 或统一抛错/错误码（二选一，不混用）
- 异常必须可追踪，禁止静默吞错

**Logging（日志规范）**
- 统一日志入口与格式；禁止随意 `console.log`
- 必须包含上下文（模块名/请求 ID/关键参数）

**Types（类型严谨度）**
- TypeScript 以 strict 思维书写
- 不允许 `any`，如必须使用需添加注释说明原因
- 导出统一使用 `export type` / `export const`

**Run formatter/linter and fix all issues, no exceptions.**
- 必须执行格式化与静态检查并修复全部问题

## 默认硬规则（可机器验证）

- TypeScript：严格类型思维，不使用隐式 `any`
- 函数参数与返回值必须显式标注类型
- API 结果：统一 `Result<T, E>` 或统一抛错/错误码
- 导出：统一 `export type` / `export const`
- 任何 lint/format 报错都必须清零
