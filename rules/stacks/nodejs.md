# Node.js 后端开发规范

> 基于全局规范,针对 Node.js 后端项目的特定标准
> 适用于: Node.js 18+, Express/Fastify, TypeScript

---

## 📋 继承全局规范

请首先遵循 [全局开发规范](./global.md) 中的所有标准。

本文档补充 Node.js 后端特定的开发规范和最佳实践。

---

## 🎯 后端核心原则

### 架构原则
- **单一职责**: 每个模块职责明确
- **依赖注入**: 降低耦合,便于测试
- **关注点分离**: Controller → Service → Repository
- **错误优先**: 完善的错误处理机制

### 代码组织原则
- 按功能模块组织代码
- 业务逻辑与框架代码分离
- 可测试、可维护、可扩展

---

## 📁 项目结构

```
project-root/
├── src/
│   ├── config/              # 配置文件
│   │   ├── database.ts
│   │   ├── redis.ts
│   │   └── app.ts
│   ├── modules/             # 业务模块
│   │   ├── users/
│   │   │   ├── user.controller.ts
│   │   │   ├── user.service.ts
│   │   │   ├── user.repository.ts
│   │   │   ├── user.model.ts
│   │   │   ├── user.types.ts
│   │   │   ├── user.validator.ts
│   │   │   └── user.routes.ts
│   │   └── auth/
│   ├── middleware/          # 中间件
│   │   ├── auth.ts
│   │   ├── error-handler.ts
│   │   └── logger.ts
│   ├── utils/               # 工具函数
│   │   ├── logger.ts
│   │   ├── crypto.ts
│   │   └── validators.ts
│   ├── types/               # 类型定义
│   │   ├── express.d.ts
│   │   └── common.ts
│   ├── constants/           # 常量
│   │   ├── errors.ts
│   │   └── config.ts
│   └── app.ts              # 应用入口
├── tests/                   # 测试
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── scripts/                 # 脚本
├── docs/                    # 文档
├── .env.example            # 环境变量示例
└── tsconfig.json           # TS 配置
```

---

## 🏗️ 分层架构

### Controller 层 (控制器)
```typescript
// user.controller.ts
import { Request, Response, NextFunction } from 'express';
import { UserService } from './user.service';
import { CreateUserDto, UpdateUserDto } from './user.types';
import { validateDto } from '@/utils/validators';

export class UserController {
  constructor(private userService: UserService) {}

  // ✅ 职责: 处理 HTTP 请求/响应
  async createUser(req: Request, res: Response, next: NextFunction) {
    try {
      // 1. 验证请求数据
      const dto = await validateDto(CreateUserDto, req.body);
      
      // 2. 调用服务层
      const user = await this.userService.createUser(dto);
      
      // 3. 返回响应
      res.status(201).json({
        success: true,
        data: user,
      });
    } catch (error) {
      next(error);
    }
  }

  async getUser(req: Request, res: Response, next: NextFunction) {
    try {
      const { id } = req.params;
      const user = await this.userService.getUserById(id);
      
      res.json({
        success: true,
        data: user,
      });
    } catch (error) {
      next(error);
    }
  }

  async updateUser(req: Request, res: Response, next: NextFunction) {
    try {
      const { id } = req.params;
      const dto = await validateDto(UpdateUserDto, req.body);
      
      const user = await this.userService.updateUser(id, dto);
      
      res.json({
        success: true,
        data: user,
      });
    } catch (error) {
      next(error);
    }
  }
}
```

### Service 层 (业务逻辑)
```typescript
// user.service.ts
import { UserRepository } from './user.repository';
import { CreateUserDto, UpdateUserDto, User } from './user.types';
import { AppError } from '@/utils/errors';
import { hashPassword, comparePassword } from '@/utils/crypto';

export class UserService {
  constructor(
    private userRepository: UserRepository,
    private emailService: EmailService,
  ) {}

  // ✅ 职责: 业务逻辑处理
  async createUser(dto: CreateUserDto): Promise<User> {
    // 1. 业务验证
    const existingUser = await this.userRepository.findByEmail(dto.email);
    if (existingUser) {
      throw new AppError('USER_EXISTS', 'Email already registered', 400);
    }

    // 2. 数据处理
    const hashedPassword = await hashPassword(dto.password);
    const userData = {
      ...dto,
      password: hashedPassword,
    };

    // 3. 调用数据层
    const user = await this.userRepository.create(userData);

    // 4. 触发副作用 (异步)
    this.emailService.sendWelcomeEmail(user.email).catch(err => {
      console.error('Failed to send welcome email:', err);
    });

    // 5. 返回结果 (不包含敏感信息)
    const { password, ...userWithoutPassword } = user;
    return userWithoutPassword;
  }

  async getUserById(id: string): Promise<User> {
    const user = await this.userRepository.findById(id);
    
    if (!user) {
      throw new AppError('USER_NOT_FOUND', 'User not found', 404);
    }

    const { password, ...userWithoutPassword } = user;
    return userWithoutPassword;
  }

  async updateUser(id: string, dto: UpdateUserDto): Promise<User> {
    const user = await this.getUserById(id);

    // 如果更新邮箱,检查是否已被使用
    if (dto.email && dto.email !== user.email) {
      const existing = await this.userRepository.findByEmail(dto.email);
      if (existing) {
        throw new AppError('EMAIL_EXISTS', 'Email already in use', 400);
      }
    }

    const updated = await this.userRepository.update(id, dto);
    const { password, ...result } = updated;
    return result;
  }

  async deleteUser(id: string): Promise<void> {
    await this.getUserById(id); // 确保存在
    await this.userRepository.delete(id);
  }
}
```

### Repository 层 (数据访问)
```typescript
// user.repository.ts
import { Database } from '@/config/database';
import { User, CreateUserData } from './user.types';

export class UserRepository {
  constructor(private db: Database) {}

  // ✅ 职责: 数据库操作
  async create(data: CreateUserData): Promise<User> {
    const result = await this.db.query(
      `INSERT INTO users (email, password, name) 
       VALUES ($1, $2, $3) 
       RETURNING *`,
      [data.email, data.password, data.name]
    );
    return result.rows[0];
  }

  async findById(id: string): Promise<User | null> {
    const result = await this.db.query(
      'SELECT * FROM users WHERE id = $1',
      [id]
    );
    return result.rows[0] || null;
  }

  async findByEmail(email: string): Promise<User | null> {
    const result = await this.db.query(
      'SELECT * FROM users WHERE email = $1',
      [email]
    );
    return result.rows[0] || null;
  }

  async update(id: string, data: Partial<User>): Promise<User> {
    const fields = Object.keys(data);
    const values = Object.values(data);
    
    const setClause = fields
      .map((field, index) => `${field} = $${index + 2}`)
      .join(', ');

    const result = await this.db.query(
      `UPDATE users SET ${setClause} WHERE id = $1 RETURNING *`,
      [id, ...values]
    );
    
    return result.rows[0];
  }

  async delete(id: string): Promise<void> {
    await this.db.query('DELETE FROM users WHERE id = $1', [id]);
  }

  async findAll(options: {
    limit?: number;
    offset?: number;
  }): Promise<User[]> {
    const { limit = 10, offset = 0 } = options;
    
    const result = await this.db.query(
      'SELECT * FROM users LIMIT $1 OFFSET $2',
      [limit, offset]
    );
    
    return result.rows;
  }
}
```

---

## 🛣️ 路由定义

```typescript
// user.routes.ts
import { Router } from 'express';
import { UserController } from './user.controller';
import { authenticate } from '@/middleware/auth';
import { validateRequest } from '@/middleware/validation';
import { createUserSchema, updateUserSchema } from './user.validator';

export const createUserRouter = (controller: UserController): Router => {
  const router = Router();

  // ✅ RESTful 路由设计
  router.post(
    '/users',
    validateRequest(createUserSchema),
    controller.createUser.bind(controller)
  );

  router.get(
    '/users/:id',
    authenticate,
    controller.getUser.bind(controller)
  );

  router.put(
    '/users/:id',
    authenticate,
    validateRequest(updateUserSchema),
    controller.updateUser.bind(controller)
  );

  router.delete(
    '/users/:id',
    authenticate,
    controller.deleteUser.bind(controller)
  );

  router.get(
    '/users',
    authenticate,
    controller.listUsers.bind(controller)
  );

  return router;
};
```

---

## 🔐 中间件

### 认证中间件
```typescript
// middleware/auth.ts
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { AppError } from '@/utils/errors';
import { config } from '@/config';

interface JwtPayload {
  userId: string;
  email: string;
}

declare global {
  namespace Express {
    interface Request {
      user?: JwtPayload;
    }
  }
}

export const authenticate = (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  try {
    // 1. 获取 token
    const token = req.headers.authorization?.replace('Bearer ', '');
    
    if (!token) {
      throw new AppError('UNAUTHORIZED', 'No token provided', 401);
    }

    // 2. 验证 token
    const decoded = jwt.verify(token, config.jwtSecret) as JwtPayload;

    // 3. 将用户信息附加到请求对象
    req.user = decoded;

    next();
  } catch (error) {
    if (error instanceof jwt.JsonWebTokenError) {
      next(new AppError('UNAUTHORIZED', 'Invalid token', 401));
    } else {
      next(error);
    }
  }
};

// 角色检查中间件
export const authorize = (...roles: string[]) => {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      return next(new AppError('UNAUTHORIZED', 'Not authenticated', 401));
    }

    // 这里需要从数据库获取用户角色
    // 简化示例
    const userRole = 'user';
    
    if (!roles.includes(userRole)) {
      return next(new AppError('FORBIDDEN', 'Insufficient permissions', 403));
    }

    next();
  };
};
```

### 错误处理中间件
```typescript
// middleware/error-handler.ts
import { Request, Response, NextFunction } from 'express';
import { AppError } from '@/utils/errors';
import { logger } from '@/utils/logger';

export const errorHandler = (
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  // 记录错误
  logger.error('Error occurred:', {
    error: error.message,
    stack: error.stack,
    url: req.url,
    method: req.method,
    body: req.body,
    user: req.user,
  });

  // AppError (已知错误)
  if (error instanceof AppError) {
    return res.status(error.statusCode).json({
      success: false,
      error: {
        code: error.code,
        message: error.message,
      },
    });
  }

  // 验证错误
  if (error.name === 'ValidationError') {
    return res.status(400).json({
      success: false,
      error: {
        code: 'VALIDATION_ERROR',
        message: error.message,
      },
    });
  }

  // 数据库错误
  if (error.name === 'DatabaseError') {
    return res.status(500).json({
      success: false,
      error: {
        code: 'DATABASE_ERROR',
        message: 'Database operation failed',
      },
    });
  }

  // 未知错误
  res.status(500).json({
    success: false,
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred',
    },
  });
};

// 404 处理
export const notFoundHandler = (req: Request, res: Response) => {
  res.status(404).json({
    success: false,
    error: {
      code: 'NOT_FOUND',
      message: 'Resource not found',
    },
  });
};
```

### 请求日志中间件
```typescript
// middleware/logger.ts
import { Request, Response, NextFunction } from 'express';
import { logger } from '@/utils/logger';

export const requestLogger = (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  const startTime = Date.now();

  // 响应完成时记录
  res.on('finish', () => {
    const duration = Date.now() - startTime;

    logger.info('Request completed', {
      method: req.method,
      url: req.url,
      statusCode: res.statusCode,
      duration: `${duration}ms`,
      userAgent: req.get('user-agent'),
      ip: req.ip,
    });
  });

  next();
};
```

---

## 📝 验证与类型

### DTO 定义
```typescript
// user.types.ts
import { z } from 'zod';

// ✅ 使用 Zod 定义验证 schema
export const createUserSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z
    .string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain uppercase letter')
    .regex(/[a-z]/, 'Password must contain lowercase letter')
    .regex(/[0-9]/, 'Password must contain number'),
  name: z.string().min(2, 'Name must be at least 2 characters'),
  age: z.number().int().min(18).optional(),
});

export const updateUserSchema = z.object({
  email: z.string().email().optional(),
  name: z.string().min(2).optional(),
  age: z.number().int().min(18).optional(),
});

// 类型推导
export type CreateUserDto = z.infer<typeof createUserSchema>;
export type UpdateUserDto = z.infer<typeof updateUserSchema>;

// 数据库模型类型
export interface User {
  id: string;
  email: string;
  password: string;
  name: string;
  age?: number;
  createdAt: Date;
  updatedAt: Date;
}

// 响应类型 (不包含敏感信息)
export type UserResponse = Omit<User, 'password'>;
```

### 验证中间件
```typescript
// middleware/validation.ts
import { Request, Response, NextFunction } from 'express';
import { ZodSchema } from 'zod';
import { AppError } from '@/utils/errors';

export const validateRequest = (schema: ZodSchema) => {
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      req.body = await schema.parseAsync(req.body);
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        const messages = error.errors.map(err => err.message).join(', ');
        next(new AppError('VALIDATION_ERROR', messages, 400));
      } else {
        next(error);
      }
    }
  };
};
```

---

## 🗄️ 数据库

### 数据库配置
```typescript
// config/database.ts
import { Pool } from 'pg';
import { config } from './app';

export const pool = new Pool({
  host: config.db.host,
  port: config.db.port,
  database: config.db.name,
  user: config.db.user,
  password: config.db.password,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

// 连接测试
pool.on('connect', () => {
  console.log('Database connected');
});

pool.on('error', (err) => {
  console.error('Database connection error:', err);
  process.exit(-1);
});

export class Database {
  async query(text: string, params?: any[]) {
    const start = Date.now();
    
    try {
      const result = await pool.query(text, params);
      const duration = Date.now() - start;
      
      console.log('Query executed', { text, duration, rows: result.rowCount });
      
      return result;
    } catch (error) {
      console.error('Query error:', { text, error });
      throw error;
    }
  }

  async transaction<T>(callback: (client: any) => Promise<T>): Promise<T> {
    const client = await pool.connect();
    
    try {
      await client.query('BEGIN');
      const result = await callback(client);
      await client.query('COMMIT');
      return result;
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }
}
```

### 迁移脚本
```typescript
// scripts/migrate.ts
import { pool } from '@/config/database';

const migrations = [
  {
    version: 1,
    name: 'create_users_table',
    up: `
      CREATE TABLE IF NOT EXISTS users (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        age INTEGER,
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
      );
      
      CREATE INDEX idx_users_email ON users(email);
    `,
    down: `
      DROP TABLE IF EXISTS users;
    `,
  },
];

async function runMigrations() {
  const client = await pool.connect();
  
  try {
    // 创建迁移记录表
    await client.query(`
      CREATE TABLE IF NOT EXISTS migrations (
        version INTEGER PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        executed_at TIMESTAMP DEFAULT NOW()
      );
    `);

    // 获取已执行的迁移
    const result = await client.query(
      'SELECT version FROM migrations ORDER BY version'
    );
    const executed = result.rows.map(r => r.version);

    // 执行未执行的迁移
    for (const migration of migrations) {
      if (!executed.includes(migration.version)) {
        console.log(`Running migration: ${migration.name}`);
        
        await client.query('BEGIN');
        await client.query(migration.up);
        await client.query(
          'INSERT INTO migrations (version, name) VALUES ($1, $2)',
          [migration.version, migration.name]
        );
        await client.query('COMMIT');
        
        console.log(`✓ Migration completed: ${migration.name}`);
      }
    }
  } catch (error) {
    await client.query('ROLLBACK');
    console.error('Migration failed:', error);
    throw error;
  } finally {
    client.release();
  }
}

runMigrations().then(() => {
  console.log('All migrations completed');
  process.exit(0);
}).catch(error => {
  console.error('Migration error:', error);
  process.exit(1);
});
```

---

## 🔒 安全最佳实践

### 环境变量管理
```typescript
// config/app.ts
import dotenv from 'dotenv';
import { z } from 'zod';

dotenv.config();

// ✅ 验证环境变量
const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']),
  PORT: z.string().transform(Number),
  JWT_SECRET: z.string().min(32),
  DB_HOST: z.string(),
  DB_PORT: z.string().transform(Number),
  DB_NAME: z.string(),
  DB_USER: z.string(),
  DB_PASSWORD: z.string(),
  REDIS_URL: z.string().url(),
});

const env = envSchema.parse(process.env);

export const config = {
  env: env.NODE_ENV,
  port: env.PORT,
  jwtSecret: env.JWT_SECRET,
  db: {
    host: env.DB_HOST,
    port: env.DB_PORT,
    name: env.DB_NAME,
    user: env.DB_USER,
    password: env.DB_PASSWORD,
  },
  redis: {
    url: env.REDIS_URL,
  },
} as const;
```

### 密码加密
```typescript
// utils/crypto.ts
import bcrypt from 'bcrypt';
import crypto from 'crypto';

const SALT_ROUNDS = 10;

export async function hashPassword(password: string): Promise<string> {
  return bcrypt.hash(password, SALT_ROUNDS);
}

export async function comparePassword(
  password: string,
  hash: string
): Promise<boolean> {
  return bcrypt.compare(password, hash);
}

export function generateToken(length: number = 32): string {
  return crypto.randomBytes(length).toString('hex');
}
```

### 请求限流
```typescript
// middleware/rate-limit.ts
import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';
import { redis } from '@/config/redis';

export const apiLimiter = rateLimit({
  store: new RedisStore({
    client: redis,
    prefix: 'rate-limit:',
  }),
  windowMs: 15 * 60 * 1000, // 15 分钟
  max: 100, // 最多 100 次请求
  message: 'Too many requests, please try again later',
  standardHeaders: true,
  legacyHeaders: false,
});

export const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // 登录尝试限制
  skipSuccessfulRequests: true,
});
```

---

## 📊 日志系统

```typescript
// utils/logger.ts
import winston from 'winston';
import { config } from '@/config';

const logFormat = winston.format.combine(
  winston.format.timestamp(),
  winston.format.errors({ stack: true }),
  winston.format.json()
);

export const logger = winston.createLogger({
  level: config.env === 'production' ? 'info' : 'debug',
  format: logFormat,
  transports: [
    // 控制台输出
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple()
      ),
    }),
    
    // 错误日志文件
    new winston.transports.File({
      filename: 'logs/error.log',
      level: 'error',
    }),
    
    // 所有日志文件
    new winston.transports.File({
      filename: 'logs/combined.log',
    }),
  ],
});

// 生产环境不输出 debug
if (config.env === 'production') {
  logger.remove(new winston.transports.Console());
}
```

---

## 🧪 测试规范

### 单元测试
```typescript
// tests/unit/user.service.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { UserService } from '@/modules/users/user.service';
import { UserRepository } from '@/modules/users/user.repository';

describe('UserService', () => {
  let userService: UserService;
  let userRepository: UserRepository;

  beforeEach(() => {
    userRepository = {
      findByEmail: vi.fn(),
      create: vi.fn(),
    } as any;

    userService = new UserService(userRepository);
  });

  describe('createUser', () => {
    it('应该成功创建用户', async () => {
      const dto = {
        email: 'test@example.com',
        password: 'Password123',
        name: 'Test User',
      };

      vi.mocked(userRepository.findByEmail).mockResolvedValue(null);
      vi.mocked(userRepository.create).mockResolvedValue({
        id: '1',
        ...dto,
        createdAt: new Date(),
        updatedAt: new Date(),
      });

      const result = await userService.createUser(dto);

      expect(result).toBeDefined();
      expect(result.email).toBe(dto.email);
      expect(result).not.toHaveProperty('password');
    });

    it('邮箱已存在时应该抛出错误', async () => {
      const dto = {
        email: 'existing@example.com',
        password: 'Password123',
        name: 'Test User',
      };

      vi.mocked(userRepository.findByEmail).mockResolvedValue({
        id: '1',
        ...dto,
        createdAt: new Date(),
        updatedAt: new Date(),
      });

      await expect(userService.createUser(dto)).rejects.toThrow('Email already registered');
    });
  });
});
```

### 集成测试
```typescript
// tests/integration/user.test.ts
import request from 'supertest';
import { app } from '@/app';
import { pool } from '@/config/database';

describe('User API', () => {
  afterAll(async () => {
    await pool.end();
  });

  describe('POST /api/users', () => {
    it('应该创建新用户', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({
          email: 'test@example.com',
          password: 'Password123',
          name: 'Test User',
        })
        .expect(201);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toHaveProperty('id');
      expect(response.body.data.email).toBe('test@example.com');
    });

    it('验证失败时应该返回 400', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({
          email: 'invalid-email',
          password: '123',
        })
        .expect(400);

      expect(response.body.success).toBe(false);
    });
  });
});
```

---

## ⚡ 性能优化

### 缓存策略
```typescript
// utils/cache.ts
import { redis } from '@/config/redis';

export class CacheService {
  async get<T>(key: string): Promise<T | null> {
    const value = await redis.get(key);
    return value ? JSON.parse(value) : null;
  }

  async set(
    key: string,
    value: any,
    ttl: number = 3600
  ): Promise<void> {
    await redis.setex(key, ttl, JSON.stringify(value));
  }

  async del(key: string): Promise<void> {
    await redis.del(key);
  }

  async invalidatePattern(pattern: string): Promise<void> {
    const keys = await redis.keys(pattern);
    if (keys.length > 0) {
      await redis.del(...keys);
    }
  }
}

// 使用示例
export class UserService {
  async getUserById(id: string): Promise<User> {
    const cacheKey = `user:${id}`;
    
    // 尝试从缓存获取
    const cached = await cache.get<User>(cacheKey);
    if (cached) {
      return cached;
    }

    // 从数据库获取
    const user = await this.userRepository.findById(id);
    
    // 写入缓存
    await cache.set(cacheKey, user, 3600);
    
    return user;
  }
}
```

### 数据库查询优化
```typescript
// ✅ 使用索引
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);

// ✅ 分页查询
async findAll(options: PaginationOptions) {
  const { page = 1, limit = 10 } = options;
  const offset = (page - 1) * limit;

  const [users, total] = await Promise.all([
    this.db.query(
      'SELECT * FROM users ORDER BY created_at DESC LIMIT $1 OFFSET $2',
      [limit, offset]
    ),
    this.db.query('SELECT COUNT(*) FROM users'),
  ]);

  return {
    data: users.rows,
    total: parseInt(total.rows[0].count),
    page,
    limit,
    totalPages: Math.ceil(total.rows[0].count / limit),
  };
}

// ✅ 使用连接池
// ✅ 预编译语句
// ✅ 批量操作
```

---

**继承自**: [全局开发规范](./global.md)
**最后更新**: 2024-12-16