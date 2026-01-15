# Claude Code 全局开发规范

> 适用于所有项目的通用开发标准和最佳实践
> 版本: v1.0.0 | 更新日期: 2024-12

---

## 📋 核心原则

### 编程原则
- **DRY (Don't Repeat Yourself)**: 避免重复代码,提取公共逻辑
- **KISS (Keep It Simple, Stupid)**: 保持简单,避免过度设计
- **YAGNI (You Aren't Gonna Need It)**: 不做超前设计
- **单一职责原则**: 每个模块/函数只做一件事
- **开闭原则**: 对扩展开放,对修改关闭

### 代码质量标准
- 函数长度不超过 50 行 (建议 20-30 行)
- 圈复杂度不超过 10
- 函数参数不超过 4 个 (建议 3 个以内)
- 避免深层嵌套 (不超过 3 层)
- 优先使用纯函数和不可变数据

---

## 🎨 代码风格

### 命名规范
```
✅ 变量/函数: camelCase (userInfo, getUserData)
✅ 常量: UPPER_SNAKE_CASE (MAX_COUNT, API_URL)
✅ 类/组件: PascalCase (UserProfile, DataService)
✅ 文件名: kebab-case (user-service.ts, data-utils.ts)
✅ 私有变量: _prefix (_privateMethod, _internalState)
```

### 格式化
- **缩进**: 2 空格 (不使用 tab)
- **行宽**: 最大 100 字符 (建议 80)
- **引号**: 单引号 (JavaScript/TypeScript)
- **分号**: 必须使用
- **逗号**: 尾随逗号 (对象、数组最后一项)

### 注释规范
```javascript
// ✅ 好的注释: 解释"为什么"
// 使用 debounce 避免频繁触发 API 请求
const debouncedSearch = debounce(search, 300);

// ❌ 坏的注释: 重复代码逻辑
// 创建一个用户对象
const user = { name: 'John' };

/**
 * 复杂函数必须添加 JSDoc
 * @param {string} userId - 用户ID
 * @param {Object} options - 配置选项
 * @returns {Promise<User>} 用户信息
 */
```

---

## 📁 项目结构

### 标准目录结构
```
project-root/
├── src/                # 源代码
│   ├── components/     # 组件
│   ├── services/       # 业务逻辑
│   ├── utils/          # 工具函数
│   ├── types/          # 类型定义
│   ├── constants/      # 常量配置
│   └── assets/         # 静态资源
├── tests/              # 测试文件
│   ├── unit/          # 单元测试
│   └── integration/   # 集成测试
├── docs/              # 文档
├── scripts/           # 构建脚本
├── .env.example       # 环境变量示例
├── .gitignore        # Git 忽略文件
├── README.md         # 项目说明
└── claude.md         # 项目开发规范
```

### 文件组织原则
- 按功能模块划分,不按文件类型
- 相关文件就近放置
- 避免深层目录结构 (不超过 4 层)

---

## 🔐 安全规范

### 敏感信息处理
```bash
# ✅ 使用环境变量
DB_PASSWORD=xxx
API_KEY=xxx

# ❌ 禁止硬编码
const apiKey = 'sk-1234567890abcdef';
```

### .gitignore 必需项
```
.env
.env.local
*.log
node_modules/
dist/
.DS_Store
*.key
*.pem
```

### 安全检查清单
- [ ] 所有密钥使用环境变量
- [ ] API 接口有权限验证
- [ ] 用户输入进行验证和转义
- [ ] 依赖包定期安全扫描
- [ ] 敏感日志不输出到生产环境

---

## 📝 Git 提交规范

### Conventional Commits 格式
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 类型
```
feat:     新功能
fix:      修复 bug
docs:     文档变更
style:    代码格式调整 (不影响功能)
refactor: 重构 (既不是新增功能也不是修复 bug)
perf:     性能优化
test:     测试相关
chore:    构建过程或辅助工具变动
ci:       CI 配置变更
```

### 提交示例
```bash
# 基础提交
git commit -m "feat(auth): 添加用户登录功能"

# 详细提交
git commit -m "fix(api): 修复用户列表分页错误

- 修正 offset 计算逻辑
- 添加边界条件检查
- 更新相关单元测试

Closes #123"
```

### 提交频率
- 每完成一个独立功能点就提交
- 避免一次提交过多改动
- 提交前确保代码可运行

---

## ✅ 测试规范

### 测试覆盖率
- 关键业务逻辑: 必须 100%
- 工具函数: 必须 100%
- 组件逻辑: 不低于 80%
- 整体覆盖率: 不低于 80%

### 测试原则
```javascript
// ✅ 好的测试: 清晰、独立、快速
describe('calculateTotal', () => {
  it('应该正确计算商品总价', () => {
    const items = [{ price: 10 }, { price: 20 }];
    expect(calculateTotal(items)).toBe(30);
  });
});

// ❌ 坏的测试: 依赖外部状态
it('测试用户功能', () => {
  // 测试描述不清晰
  // 测试多个功能点
});
```

### 测试文件命名
```
src/utils/format.ts       → tests/unit/utils/format.test.ts
src/services/user.ts      → tests/unit/services/user.test.ts
src/components/Button.tsx → tests/unit/components/Button.test.tsx
```

---

## ⚡ 性能优化

### 通用优化策略
- 懒加载非首屏资源
- 使用适当的缓存策略
- 避免不必要的重复计算
- 优化循环和递归
- 控制包体积大小

### 代码层面
```javascript
// ✅ 使用 memo 避免重复计算
const expensiveValue = useMemo(() => {
  return computeExpensiveValue(a, b);
}, [a, b]);

// ✅ 使用 debounce/throttle
const handleSearch = debounce((query) => {
  searchAPI(query);
}, 300);

// ❌ 避免在循环中进行复杂操作
data.forEach(item => {
  // 避免在这里调用 API
});
```

---

## 📦 依赖管理

### 依赖选择原则
- 优先使用官方/主流库
- 检查项目活跃度和维护状态
- 评估包体积大小
- 查看 license 类型
- 避免过度依赖

### 版本管理
```json
{
  "dependencies": {
    "react": "^18.2.0",        // 使用 ^ 允许小版本更新
    "lodash": "~4.17.21"       // 使用 ~ 只允许补丁更新
  }
}
```

### 定期维护
```bash
# 检查过期依赖
npm outdated

# 安全审计
npm audit

# 更新依赖
npm update
```

---

## 📚 文档规范

### README.md 必需内容
```markdown
# 项目名称

## 项目简介
简短描述项目用途

## 功能特性
- 特性 1
- 特性 2

## 技术栈
- 前端框架
- 后端技术
- 数据库

## 快速开始
### 环境要求
- Node.js >= 18
- npm >= 9

### 安装
\`\`\`bash
npm install
\`\`\`

### 运行
\`\`\`bash
npm run dev
\`\`\`

## 项目结构
说明主要目录

## 开发指南
参考 claude.md

## License
MIT
```

### 代码文档
- 复杂算法必须添加注释说明
- 公共 API 必须有使用示例
- 类型定义必须有描述注释

---

## 🔄 错误处理

### 错误处理原则
```javascript
// ✅ 统一的错误处理
async function fetchUser(id) {
  try {
    const response = await api.get(`/users/${id}`);
    return response.data;
  } catch (error) {
    logger.error('获取用户失败:', error);
    throw new AppError('USER_FETCH_FAILED', error.message);
  }
}

// ✅ 提供有意义的错误信息
if (!userId) {
  throw new Error('用户ID不能为空');
}

// ❌ 吞掉错误
try {
  riskyOperation();
} catch (e) {
  // 什么都不做
}
```

### 错误日志
- 错误必须记录到日志系统
- 包含上下文信息 (用户ID、请求参数等)
- 区分错误级别 (error, warn, info)
- 生产环境不输出敏感信息

---

## 🚀 CI/CD 规范

### 必需的 CI 流程
```yaml
# 基本流程
- Lint 检查
- 单元测试
- 构建验证
- 安全扫描

# 高级流程
- E2E 测试
- 性能测试
- 代码覆盖率检查
```

### Pre-commit Hook
```bash
# 提交前自动执行
- 代码格式化
- Lint 检查
- 运行相关测试
```

---

## 🎯 代码审查 Checklist

### 功能性
- [ ] 实现符合需求
- [ ] 边界条件处理
- [ ] 错误处理完善

### 代码质量
- [ ] 遵循命名规范
- [ ] 无重复代码
- [ ] 函数职责单一
- [ ] 注释清晰有效

### 性能
- [ ] 无明显性能问题
- [ ] 合理使用缓存
- [ ] 避免不必要的计算

### 安全
- [ ] 无硬编码密钥
- [ ] 输入验证完整
- [ ] 依赖无安全漏洞

### 测试
- [ ] 单元测试覆盖
- [ ] 测试用例充分
- [ ] 测试可以通过

---

## 📌 注意事项

1. **本规范是基础标准**: 具体技术栈规范请参考对应的技术栈规范文件
2. **项目特殊需求**: 可在项目 claude.md 中覆盖或补充
3. **持续改进**: 规范会根据实践经验持续优化
4. **团队共识**: 规范需要团队成员共同遵守和维护

---

## 🔗 相关资源

- [技术栈规范目录](./stacks/)
- [项目模板](./templates/)
- [常用工具配置](./configs/)

---

**最后更新**: 2024-12-16
**维护者**: Sggmico