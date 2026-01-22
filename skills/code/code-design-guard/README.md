# Design Guard 补充说明

## 快速开始

当用户要求“检查架构/依赖方向/分层约束”时，输出以下固定结构：
- Allowed modules
- Forbidden imports
- Dependency direction
- Data flow
- If violated, reject

## 示例

**Allowed modules（允许改哪些目录）**
- `apps/web`
- `packages/ui`

**Forbidden imports（禁止跨包/跨层）**
- `packages/*` -> `apps/*`
- `packages/ui` -> `apps/web`
- `shared` -> `server-only`

**Dependency direction（依赖方向）**
- 允许 `apps/*` 依赖 `packages/*` 与 `shared`

**Data flow（数据流）**
- UI 事件由 `apps/*` 触发，经 `packages/*` 组装后调用 `server-only`，返回数据仅通过 `shared` 传递

**If violated, reject（硬性拒绝条件）**
- 出现 `packages/*` 反向依赖 `apps/*` 直接拒绝
- `shared` 引入 `server-only` 直接拒绝

## 最佳实践

- 明确目录级边界，优先使用路径而非文件名描述
- 输出必须完整且固定，不允许省略任何段落
- 若项目结构与默认约束冲突，先提示并请求确认

## 测试建议

1. 重启 Claude Code 以加载 Skill
2. 询问类似“检查 monorepo 架构边界”确保触发
3. 检查输出是否包含固定五段结构
