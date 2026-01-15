# 项目开发规范 - [项目名称]

> 本项目特定的开发规范和指南
> 基于: 全局规范 + [技术栈]规范

---

## 📋 规范继承关系

本项目遵循以下规范,优先级从高到低:

1. **本文档** (项目特定规范) - 最高优先级
2. **技术栈规范** (选择对应的技术栈)
   - React: `~/.claude/rules/stacks/react.md`
   - Vue: `~/.claude/rules/stacks/vue.md`
   - Node.js: `~/.claude/rules/stacks/nodejs.md`
3. **全局规范** (基础标准) - `~/.claude/rules/global.md`

> 💡 当规范冲突时,优先级高的规范覆盖优先级低的规范

---

## 🎯 项目概述

### 项目信息
- **项目名称**: [填写项目名称]
- **项目类型**: [Web应用 / 移动应用 / API服务 / 工具库 等]
- **主要功能**: [简要描述项目的核心功能]
- **目标用户**: [描述目标用户群体]

### 技术栈
```yaml
前端:
  - 框架: [React 18 / Vue 3 / 其他]
  - 语言: [TypeScript 5.x]
  - 状态管理: [Zustand / Pinia / Redux]
  - 样式方案: [Tailwind CSS / CSS Modules / Styled Components]
  - 构建工具: [Vite / Webpack]

后端:
  - 运行时: [Node.js 18+]
  - 框架: [Express / Fastify / Nest.js]
  - 数据库: [PostgreSQL / MySQL / MongoDB]
  - 缓存: [Redis]
  
工具链:
  - 包管理: [npm / pnpm / yarn]
  - 代码检查: [ESLint, Prettier]
  - 测试: [Vitest / Jest]
  - CI/CD: [GitHub Actions / GitLab CI]
```

---

## 📁 项目结构

```
[项目名称]/
├── src/
│   ├── [根据技术栈调整]
│   └── ...
├── tests/
├── docs/
├── scripts/
├── .env.example
├── README.md
└── claude.md          # 本文件
```

> 详细结构参考对应的技术栈规范

---

## 🎨 项目特定规范

### 命名约定

#### 特殊命名规则
```typescript
// 示例: 如果项目有特定的命名前缀
// ✅ 所有自定义 hooks 使用 useApp 前缀
useAppAuth()
useAppUser()
useAppData()

// ✅ 所有组件使用 App 前缀
AppButton
AppCard
AppModal
```

#### 文件命名特殊规则
```
// 如果项目有特殊要求,在此说明
pages/           # 使用 kebab-case
components/      # 使用 PascalCase
utils/           # 使用 camelCase
```

### 代码风格特殊要求

```typescript
// 示例: 如果项目有特殊的代码风格要求

// ✅ 本项目要求所有异步函数使用 async/await,不使用 Promise.then
async function fetchData() {
  const data = await api.get('/data');
  return data;
}

// ✅ 本项目要求错误必须使用自定义错误类
throw new AppError('USER_NOT_FOUND', 'User not found');

// ✅ 本项目的 API 响应格式
{
  "success": true,
  "data": {},
  "message": "操作成功"
}
```

---

## 🔧 开发工作流

### 环境准备
```bash
# 1. 克隆项目
git clone [repository-url]

# 2. 安装依赖
npm install

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 填入实际配置

# 4. 初始化数据库 (如果需要)
npm run db:migrate

# 5. 启动开发服务器
npm run dev
```

### 开发流程
```bash
# 1. 创建功能分支
git checkout -b feature/user-profile

# 2. 开发功能
# - 编写代码
# - 编写测试
# - 本地测试

# 3. 提交代码
git add .
git commit -m "feat(user): 添加用户资料页面"

# 4. 推送并创建 PR
git push origin feature/user-profile
```

### Git 分支策略
```
main         - 生产环境分支 (受保护)
develop      - 开发环境分支
feature/*    - 功能开发分支
bugfix/*     - Bug 修复分支
hotfix/*     - 紧急修复分支
release/*    - 发布准备分支
```

### 提交规范 (项目特定)
```bash
# 基于 Conventional Commits,但本项目有特殊要求

# ✅ 格式
<type>(<scope>): <subject>

# Type 必须使用以下之一
feat:     新功能
fix:      修复
docs:     文档
style:    格式
refactor: 重构
test:     测试
chore:    构建/工具

# Scope 必须是以下之一 (根据项目模块调整)
auth:     认证模块
user:     用户模块
order:    订单模块
payment:  支付模块
admin:    管理后台

# 示例
git commit -m "feat(auth): 添加微信登录功能"
git commit -m "fix(order): 修复订单金额计算错误"
```

---

## 🔐 环境变量

### 必需的环境变量
```bash
# 应用配置
NODE_ENV=development
PORT=3000

# 数据库
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
DB_USER=postgres
DB_PASSWORD=secret

# Redis
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET=your-secret-key-at-least-32-chars

# 第三方服务 (根据项目需要)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
STRIPE_SECRET_KEY=
```

### 环境配置说明
- 开发环境使用 `.env.development`
- 测试环境使用 `.env.test`
- 生产环境使用 `.env.production`
- 敏感信息不提交到版本控制

---

## 🧪 测试要求

### 测试覆盖率要求
- 工具函数: 100%
- Service 层: 100%
- Controller 层: ≥ 80%
- 组件: ≥ 80%
- 整体: ≥ 85%

### 测试命名规范
```typescript
// ✅ 测试描述使用中文,清晰描述测试意图
describe('用户服务', () => {
  describe('创建用户', () => {
    it('应该成功创建用户', () => {});
    it('邮箱已存在时应该抛出错误', () => {});
    it('密码格式不正确时应该抛出错误', () => {});
  });
});
```

### 运行测试
```bash
# 运行所有测试
npm test

# 运行特定测试文件
npm test user.test.ts

# 生成覆盖率报告
npm run test:coverage

# 监听模式
npm run test:watch
```

---

## 📦 依赖管理

### 添加依赖原则
1. 优先使用项目已有的依赖解决问题
2. 评估新依赖的必要性
3. 检查依赖的维护状态和安全性
4. 记录添加原因

### 依赖更新策略
```bash
# 每周检查一次依赖更新
npm outdated

# 安全漏洞每日检查
npm audit

# 重要依赖及时更新,次要依赖月度批量更新
```

### 禁止使用的包
```
# 本项目明确禁止使用以下包 (根据项目需要)
- moment (请使用 dayjs)
- lodash (请使用 lodash-es 或原生方法)
- [其他]
```

---

## 🎯 API 设计规范

### RESTful API 路由规范
```
GET    /api/users           获取用户列表
GET    /api/users/:id       获取单个用户
POST   /api/users           创建用户
PUT    /api/users/:id       更新用户
DELETE /api/users/:id       删除用户
```

### 请求格式
```typescript
// POST/PUT 请求 Body
{
  "email": "user@example.com",
  "name": "User Name"
}
```

### 响应格式 (项目特定)
```typescript
// ✅ 成功响应
{
  "success": true,
  "data": {
    "id": "123",
    "email": "user@example.com"
  },
  "message": "操作成功"
}

// ✅ 错误响应
{
  "success": false,
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "用户不存在"
  }
}

// ✅ 列表响应 (带分页)
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 100,
    "totalPages": 10
  }
}
```

### 错误码定义
```typescript
// 本项目的错误码规范
export enum ErrorCode {
  // 认证相关 (1xxx)
  UNAUTHORIZED = 1001,
  TOKEN_EXPIRED = 1002,
  INVALID_TOKEN = 1003,
  
  // 用户相关 (2xxx)
  USER_NOT_FOUND = 2001,
  USER_EXISTS = 2002,
  INVALID_PASSWORD = 2003,
  
  // 业务相关 (3xxx)
  ORDER_NOT_FOUND = 3001,
  INSUFFICIENT_BALANCE = 3002,
  
  // 系统相关 (9xxx)
  INTERNAL_ERROR = 9001,
  DATABASE_ERROR = 9002,
}
```

---

## 🔒 安全要求

### 本项目特定安全规则
```typescript
// 1. 所有用户输入必须验证和转义
const sanitizedInput = sanitize(userInput);

// 2. 敏感操作必须二次验证
if (isDestructiveAction) {
  await verifyUser(userId);
}

// 3. 所有对外 API 必须有限流
app.use('/api/', rateLimiter);

// 4. 密码必须加盐哈希
const hashedPassword = await bcrypt.hash(password, 10);

// 5. JWT token 必须设置过期时间
const token = jwt.sign(payload, secret, { expiresIn: '1h' });
```

---

## 📊 性能要求

### 性能指标
- API 响应时间: P95 < 200ms
- 页面加载时间: FCP < 1.5s
- 交互响应时间: < 100ms
- 内存使用: < 512MB

### 性能优化检查清单
- [ ] 图片已压缩和优化
- [ ] 启用 HTTP/2
- [ ] 启用 Gzip/Brotli 压缩
- [ ] CDN 加速静态资源
- [ ] 数据库查询已优化 (使用索引)
- [ ] 实现缓存策略 (Redis)
- [ ] 代码分割和懒加载
- [ ] 删除未使用的代码

---

## 🚀 部署流程

### 部署前检查
```bash
# 1. 运行所有测试
npm test

# 2. 代码检查
npm run lint

# 3. 类型检查
npm run type-check

# 4. 构建
npm run build

# 5. 本地验证构建产物
npm run preview
```

### 部署步骤
```bash
# 1. 合并到 develop 分支
git checkout develop
git merge feature/xxx

# 2. 创建发布分支
git checkout -b release/v1.2.0

# 3. 更新版本号
npm version patch/minor/major

# 4. 推送代码
git push origin release/v1.2.0

# 5. 创建 PR 到 main
# 6. Review 通过后合并
# 7. 自动触发 CI/CD 部署
```

---

## 📚 文档要求

### 必需的文档
1. **README.md** - 项目说明
2. **API.md** - API 接口文档
3. **CHANGELOG.md** - 变更日志
4. **本文件** (claude.md) - 开发规范

### 代码注释要求
```typescript
// ✅ 复杂业务逻辑必须注释
/**
 * 计算订单优惠金额
 * 
 * 优惠规则:
 * 1. VIP 用户享受 9 折
 * 2. 满 100 减 10
 * 3. 首单用户额外减 5
 * 
 * @param order 订单信息
 * @param user 用户信息
 * @returns 优惠金额
 */
function calculateDiscount(order: Order, user: User): number {
  // 实现逻辑
}
```

---

## 🐛 调试指南

### 常见问题排查
```bash
# 问题 1: 依赖安装失败
rm -rf node_modules package-lock.json
npm install

# 问题 2: 数据库连接失败
# 检查 .env 配置
# 确认数据库服务已启动

# 问题 3: 端口被占用
# macOS/Linux
lsof -i :3000
kill -9 [PID]

# Windows
netstat -ano | findstr :3000
taskkill /PID [PID] /F
```

### 开发调试技巧
```typescript
// 使用 VS Code 调试配置
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Debug",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "console": "integratedTerminal"
    }
  ]
}
```

---

## 👥 团队协作

### Code Review 要求
- 所有代码必须经过至少 1 人 review
- 必须通过所有自动化测试
- 必须解决所有 review 意见
- Approve 后才能合并

### 沟通渠道
- 日常沟通: [Slack / 企业微信 / 飞书]
- 技术讨论: [GitHub Discussions / 团队 Wiki]
- Bug 追踪: [GitHub Issues / Jira]
- 文档协作: [Notion / Confluence]

---

## 🎓 学习资源

### 项目相关资源
- [项目 Wiki](链接)
- [API 文档](链接)
- [设计稿](链接)
- [原型图](链接)

### 技术文档
- [React 官方文档](https://react.dev)
- [Vue 官方文档](https://vuejs.org)
- [Node.js 文档](https://nodejs.org)
- [TypeScript 文档](https://www.typescriptlang.org)

---

## 📝 变更记录

### v1.0.0 - 2024-12-16
- 初始版本
- 建立基础开发规范
- 定义项目结构和工作流

---

## 🔗 相关文档

- [全局开发规范](~/.claude/global-rules.md)
- [React 规范](~/.claude/stack-react.md) / [Vue 规范](~/.claude/stack-vue.md)
- [Node.js 规范](~/.claude/stack-nodejs.md)
- [项目 README](./README.md)

---

## 📧 联系方式

- **项目负责人**: [姓名]
- **技术负责人**: [姓名]
- **团队邮箱**: [邮箱]

---

**重要提示**: 本文档是项目的核心开发规范,所有团队成员必须遵守。如有疑问或建议,请及时提出讨论。