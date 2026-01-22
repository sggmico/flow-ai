# Quality Gate 补充说明

## 快速开始

当用户要求“质量关/测试计划/边界/性能/回滚”时，输出以下固定结构：
- Test Plan
- Required tests
- Performance considerations
- Migration/rollback
- Risk level
- 修正清单（Checklist）
- 指令：按清单逐项修复，直到通过 quality gate。

## 示例

**Test Plan（哪些测试，覆盖哪些边界）**
- 单元测试覆盖空输入、非法参数、权限不足

**Required tests（必须新增/更新的测试文件清单）**
- `tests/user/create-user.test.ts`

**Performance considerations（是否引入 N+1、重渲染、重查询）**
- 有潜在 N+1，需批量查询

**Migration/rollback（是否需要迁移脚本、如何回滚）**
- 需要迁移脚本，回滚通过 feature flag 禁用新路径

**Risk level（low/medium/high）**
- medium：涉及写路径与迁移

**修正清单（Checklist）**
- `src/user/create.ts`：改为批量查询以避免 N+1；以查询次数断言验证
- `tests/user/create-user.test.ts`：新增空输入与权限不足用例

**指令**
- 按清单逐项修复，直到通过 quality gate。

## 最佳实践

- 清单必须可独立执行与验证
- 风险等级与回滚策略必须明确
- 若信息不足，先要求补充上下文

## 测试建议

1. 重启 Claude Code 以加载 Skill
2. 询问“给出质量关清单”确保触发
3. 检查输出是否包含固定七段结构
