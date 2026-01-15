# React 技术栈开发规范

> 基于全局规范,针对 React 项目的特定标准
> 适用于: React 18+, TypeScript

---

## 📋 继承全局规范

请首先遵循 [全局开发规范](./global.md) 中的所有标准。

本文档补充 React 特定的开发规范和最佳实践。

---

## 🎯 React 核心原则

### 组件设计原则
- **单一职责**: 每个组件只负责一个功能
- **可组合性**: 通过组合小组件构建复杂功能
- **可复用性**: 组件应该易于在不同场景复用
- **可测试性**: 组件逻辑应该易于测试

### 状态管理原则
- 状态提升到最近的共同父组件
- 避免不必要的全局状态
- 使用合适的状态管理方案 (Context/Zustand/Redux)

---

## 📁 React 项目结构

```
src/
├── components/           # 通用组件
│   ├── ui/              # 基础 UI 组件 (Button, Input)
│   ├── layout/          # 布局组件 (Header, Footer)
│   └── common/          # 通用业务组件
├── features/            # 功能模块 (按业务划分)
│   ├── auth/
│   │   ├── components/  # 模块内组件
│   │   ├── hooks/       # 模块内 hooks
│   │   ├── services/    # 模块内服务
│   │   └── types/       # 模块内类型
│   └── user/
├── hooks/               # 全局自定义 hooks
├── services/            # API 服务
├── store/               # 状态管理
├── utils/               # 工具函数
├── types/               # 全局类型定义
├── constants/           # 常量配置
├── styles/              # 全局样式
├── assets/              # 静态资源
├── App.tsx             # 根组件
└── main.tsx            # 入口文件
```

---

## 🧩 组件规范

### 组件命名
```typescript
// ✅ PascalCase 命名
export const UserProfile = () => { }
export const DataTable = () => { }

// ✅ 文件名与组件名一致
UserProfile.tsx  // 导出 UserProfile 组件
DataTable.tsx    // 导出 DataTable 组件

// ❌ 避免
export const userProfile = () => { }  // 小驼峰
export default () => { }               // 匿名导出
```

### 组件结构顺序
```typescript
// 1. 导入
import { useState, useEffect } from 'react';
import { Button } from '@/components/ui';
import { useAuth } from '@/hooks';
import type { User } from '@/types';

// 2. 类型定义
interface UserProfileProps {
  userId: string;
  onUpdate?: (user: User) => void;
}

// 3. 组件定义
export const UserProfile: React.FC<UserProfileProps> = ({ 
  userId, 
  onUpdate 
}) => {
  // 3.1 Hooks (顺序固定)
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  
  useEffect(() => {
    // 副作用逻辑
  }, [userId]);

  // 3.2 事件处理函数
  const handleUpdate = () => {
    // 处理逻辑
  };

  // 3.3 渲染条件判断
  if (loading) {
    return <div>Loading...</div>;
  }

  // 3.4 JSX 返回
  return (
    <div className="user-profile">
      <Button onClick={handleUpdate}>Update</Button>
    </div>
  );
};

// 4. 默认属性 (如果需要)
UserProfile.defaultProps = {
  onUpdate: undefined,
};
```

### 组件类型选择

#### 函数组件 (推荐)
```typescript
// ✅ 默认使用函数组件
export const Welcome: React.FC<{ name: string }> = ({ name }) => {
  return <h1>Hello, {name}!</h1>;
};

// ✅ 简单组件可省略 React.FC
export const Button = ({ children }: { children: React.ReactNode }) => {
  return <button>{children}</button>;
};
```

#### Props 定义
```typescript
// ✅ 使用 interface 定义 Props (推荐)
interface ButtonProps {
  variant?: 'primary' | 'secondary';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}

// ✅ 使用 type 也可以
type ButtonProps = {
  variant?: 'primary' | 'secondary';
  children: React.ReactNode;
};

// ✅ 继承原生属性
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}
```

---

## 🎣 Hooks 使用规范

### 自定义 Hooks 命名
```typescript
// ✅ 必须以 use 开头
export const useAuth = () => { };
export const useLocalStorage = () => { };

// ❌ 错误命名
export const getAuth = () => { };  // 不是 hook
```

### 自定义 Hooks 结构
```typescript
// ✅ 好的 hook 设计
export const useUser = (userId: string) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchUser = async () => {
      setLoading(true);
      try {
        const data = await userService.getUser(userId);
        setUser(data);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, [userId]);

  // 返回对象 (推荐) 或数组
  return { user, loading, error };
};

// 使用
const { user, loading, error } = useUser('123');
```

### useState 使用
```typescript
// ✅ 使用类型推断
const [count, setCount] = useState(0);
const [name, setName] = useState('');

// ✅ 复杂类型显式声明
const [user, setUser] = useState<User | null>(null);

// ✅ 函数式更新
setCount(prev => prev + 1);

// ❌ 避免直接使用之前的值
setCount(count + 1);  // 在异步场景可能出错
```

### useEffect 使用
```typescript
// ✅ 明确依赖项
useEffect(() => {
  fetchData(userId);
}, [userId]);

// ✅ 清理副作用
useEffect(() => {
  const timer = setInterval(() => {}, 1000);
  
  return () => {
    clearInterval(timer);
  };
}, []);

// ❌ 避免缺少依赖
useEffect(() => {
  fetchData(userId);
}, []); // 缺少 userId 依赖

// ❌ 避免对象/数组字面量作为依赖
useEffect(() => {
  // 每次都会执行
}, [{ userId }]); // 应该使用 [userId]
```

### useMemo / useCallback 使用
```typescript
// ✅ 优化昂贵计算
const expensiveValue = useMemo(() => {
  return items.reduce((sum, item) => sum + item.value, 0);
}, [items]);

// ✅ 优化子组件渲染
const handleClick = useCallback(() => {
  doSomething(value);
}, [value]);

// ❌ 过度优化简单值
const double = useMemo(() => count * 2, [count]); // 不必要
```

---

## 🎨 样式解决方案

### CSS Modules (推荐)
```typescript
// UserProfile.module.css
.container {
  padding: 20px;
}

.title {
  font-size: 24px;
}

// UserProfile.tsx
import styles from './UserProfile.module.css';

export const UserProfile = () => {
  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Title</h1>
    </div>
  );
};
```

### Tailwind CSS
```typescript
// ✅ 使用 Tailwind 类名
export const Button = () => {
  return (
    <button className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
      Click me
    </button>
  );
};

// ✅ 动态类名使用 clsx/classnames
import clsx from 'clsx';

export const Button = ({ variant }: { variant: 'primary' | 'secondary' }) => {
  return (
    <button className={clsx(
      'px-4 py-2 rounded',
      variant === 'primary' && 'bg-blue-500 text-white',
      variant === 'secondary' && 'bg-gray-200 text-gray-800'
    )}>
      Click me
    </button>
  );
};
```

### Styled Components (可选)
```typescript
import styled from 'styled-components';

// ✅ 组件外定义样式
const StyledButton = styled.button<{ $primary?: boolean }>`
  padding: 8px 16px;
  background: ${props => props.$primary ? '#007bff' : '#6c757d'};
  color: white;
`;

export const Button = ({ primary }: { primary?: boolean }) => {
  return <StyledButton $primary={primary}>Click</StyledButton>;
};
```

---

## 🔄 状态管理

### Context API (轻量级)
```typescript
// ✅ 创建 Context
interface AuthContextType {
  user: User | null;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// ✅ Provider 组件
export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ 
  children 
}) => {
  const [user, setUser] = useState<User | null>(null);

  const login = async (credentials: Credentials) => {
    const user = await authService.login(credentials);
    setUser(user);
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// ✅ 自定义 hook 访问 context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
```

### Zustand (中型项目推荐)
```typescript
// ✅ 定义 store
import { create } from 'zustand';

interface UserStore {
  user: User | null;
  setUser: (user: User) => void;
  clearUser: () => void;
}

export const useUserStore = create<UserStore>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  clearUser: () => set({ user: null }),
}));

// ✅ 在组件中使用
const UserProfile = () => {
  const user = useUserStore((state) => state.user);
  const setUser = useUserStore((state) => state.setUser);
  
  return <div>{user?.name}</div>;
};
```

---

## 📡 数据获取

### React Query (推荐)
```typescript
import { useQuery, useMutation } from '@tanstack/react-query';

// ✅ 数据查询
export const useUser = (userId: string) => {
  return useQuery({
    queryKey: ['user', userId],
    queryFn: () => userService.getUser(userId),
  });
};

// ✅ 数据变更
export const useUpdateUser = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (user: User) => userService.updateUser(user),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['user'] });
    },
  });
};

// 使用
const UserProfile = ({ userId }: { userId: string }) => {
  const { data: user, isLoading } = useUser(userId);
  const updateUser = useUpdateUser();

  if (isLoading) return <div>Loading...</div>;

  return <div>{user?.name}</div>;
};
```

### 传统 useEffect 方式
```typescript
// ✅ 标准数据获取模式
export const UserProfile = ({ userId }: { userId: string }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let cancelled = false;

    const fetchUser = async () => {
      try {
        setLoading(true);
        const data = await userService.getUser(userId);
        
        if (!cancelled) {
          setUser(data);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err as Error);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    fetchUser();

    // 清理函数防止内存泄漏
    return () => {
      cancelled = true;
    };
  }, [userId]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return <div>{user?.name}</div>;
};
```

---

## 🧪 测试规范

### 组件测试
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('应该渲染按钮文本', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('应该在点击时调用 onClick', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click</Button>);
    
    fireEvent.click(screen.getByText('Click'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('禁用状态不应该触发点击', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick} disabled>Click</Button>);
    
    fireEvent.click(screen.getByText('Click'));
    expect(handleClick).not.toHaveBeenCalled();
  });
});
```

### Hooks 测试
```typescript
import { renderHook, waitFor } from '@testing-library/react';
import { useUser } from './useUser';

describe('useUser', () => {
  it('应该获取用户数据', async () => {
    const { result } = renderHook(() => useUser('123'));

    expect(result.current.loading).toBe(true);

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
      expect(result.current.user).toBeDefined();
    });
  });
});
```

---

## ⚡ 性能优化

### 组件优化
```typescript
// ✅ 使用 React.memo 避免不必要的重渲染
export const ExpensiveComponent = React.memo<Props>(({ data }) => {
  return <div>{/* 复杂渲染 */}</div>;
});

// ✅ 使用 useMemo 缓存计算结果
const sortedData = useMemo(() => {
  return data.sort((a, b) => a.value - b.value);
}, [data]);

// ✅ 使用 useCallback 缓存回调函数
const handleClick = useCallback(() => {
  console.log('clicked');
}, []);
```

### 代码分割
```typescript
// ✅ 路由级别的懒加载
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

export const App = () => {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
};

// ✅ 组件级别的懒加载
const HeavyComponent = lazy(() => import('./HeavyComponent'));
```

### 列表优化
```typescript
// ✅ 必须使用 key
const UserList = ({ users }: { users: User[] }) => {
  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
};

// ❌ 避免使用 index 作为 key
{users.map((user, index) => (
  <li key={index}>{user.name}</li>  // 可能导致问题
))}

// ✅ 虚拟滚动 (大列表)
import { FixedSizeList } from 'react-window';

const VirtualList = ({ items }: { items: any[] }) => {
  return (
    <FixedSizeList
      height={600}
      itemCount={items.length}
      itemSize={50}
      width="100%"
    >
      {({ index, style }) => (
        <div style={style}>{items[index].name}</div>
      )}
    </FixedSizeList>
  );
};
```

---

## 🔒 类型安全

### Props 类型定义
```typescript
// ✅ 完整的类型定义
interface UserCardProps {
  user: User;
  onEdit?: (user: User) => void;
  onDelete?: (userId: string) => void;
  className?: string;
  children?: React.ReactNode;
}

// ✅ 联合类型
type ButtonVariant = 'primary' | 'secondary' | 'danger';

interface ButtonProps {
  variant: ButtonVariant;
  size?: 'small' | 'medium' | 'large';
}

// ✅ 泛型组件
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
}

export const List = <T,>({ items, renderItem }: ListProps<T>) => {
  return <>{items.map(renderItem)}</>;
};
```

### 事件类型
```typescript
// ✅ 使用正确的事件类型
const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
  e.preventDefault();
};

const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  console.log(e.target.value);
};

const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
  e.preventDefault();
};
```

---

## 📋 最佳实践

### 避免的反模式
```typescript
// ❌ 在渲染中定义组件
const Parent = () => {
  const Child = () => <div>Child</div>;  // 每次渲染都创建新组件
  return <Child />;
};

// ✅ 在外部定义
const Child = () => <div>Child</div>;
const Parent = () => <Child />;

// ❌ 在 JSX 中定义对象
<Component config={{ key: 'value' }} />  // 每次渲染都创建新对象

// ✅ 使用 useMemo 或提取到外部
const config = useMemo(() => ({ key: 'value' }), []);
<Component config={config} />

// ❌ Props drilling (过深的属性传递)
<Parent>
  <Child user={user}>
    <GrandChild user={user}>
      <GreatGrandChild user={user} />
    </GrandChild>
  </Child>
</Parent>

// ✅ 使用 Context 或状态管理
const { user } = useAuth();
```

### 条件渲染
```typescript
// ✅ 使用 && 运算符
{isLoggedIn && <Dashboard />}

// ✅ 使用三元运算符
{isLoading ? <Spinner /> : <Content />}

// ✅ 早期返回
if (isLoading) {
  return <Spinner />;
}

return <Content />;

// ❌ 避免嵌套三元运算符
{condition1 ? (
  condition2 ? <A /> : <B />
) : (
  condition3 ? <C /> : <D />
)}
```

---

## 🛠️ 常用工具配置

### ESLint 配置
```json
{
  "extends": [
    "react-app",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended"
  ],
  "rules": {
    "react/prop-types": "off",
    "react/react-in-jsx-scope": "off",
    "react-hooks/rules-of-hooks": "error",
    "react-hooks/exhaustive-deps": "warn"
  }
}
```

### TypeScript 配置
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "jsx": "react-jsx",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  }
}
```

---

**继承自**: [全局开发规范](./global.md)
**最后更新**: 2024-12-16