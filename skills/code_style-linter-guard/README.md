# Style Linter Guard 补充说明

## 快速开始

当用户要求“统一风格/规范化/lint/format/TS 严格性”时，输出以下固定结构：
- Naming
- File structure
- Error handling
- Logging
- Types
- Run formatter/linter and fix all issues, no exceptions.

## 示例

**Naming（命名约定）**
- 文件 `kebab-case`，组件 `PascalCase`，函数 `camelCase`

**File structure（文件组织）**
- `src/feature/*` 下放置实现与测试，禁止新增 `misc/`

**Error handling（错误处理模式）**
- 统一返回 `Result<T, E>`，禁止混用异常与错误码

**Logging（日志规范）**
- 使用统一 logger，并附带 `requestId`

**Types（类型严谨度）**
- 禁止 `any`，必须显式类型

**Run formatter/linter and fix all issues, no exceptions.**

## 最佳实践

- 规则必须可验证、可执行
- 输出不允许“建议”“可选”等措辞
- 若发现混用错误处理模式，立即要求统一

## 测试建议

1. 重启 Claude Code 以加载 Skill
2. 询问“请按团队规范统一风格”确保触发
3. 检查输出是否包含固定六段结构
