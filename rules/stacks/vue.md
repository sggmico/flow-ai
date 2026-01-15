# Vue 3 技术栈开发规范

> 基于全局规范,针对 Vue 3 项目的特定标准
> 适用于: Vue 3 + Composition API + TypeScript

---

## 📋 继承全局规范

请首先遵循 [全局开发规范](./global.md) 中的所有标准。

本文档补充 Vue 3 特定的开发规范和最佳实践。

---

## 🎯 Vue 核心原则

### 组件设计原则
- 优先使用 Composition API
- 单文件组件 (SFC) 结构清晰
- Props 单向数据流
- 合理使用响应式 API

### 代码组织原则
- 按功能组织代码,不按选项
- 提取可复用的组合式函数 (Composables)
- 保持模板简洁,复杂逻辑放到脚本中

---

## 📁 Vue 项目结构

```
src/
├── components/           # 通用组件
│   ├── base/            # 基础组件 (BaseButton, BaseInput)
│   ├── layout/          # 布局组件
│   └── common/          # 通用业务组件
├── views/               # 页面视图
├── composables/         # 组合式函数
├── stores/              # Pinia 状态管理
├── router/              # 路由配置
├── services/            # API 服务
├── utils/               # 工具函数
├── types/               # 类型定义
├── directives/          # 自定义指令
├── plugins/             # 插件
├── assets/              # 静态资源
├── styles/              # 全局样式
├── App.vue             # 根组件
└── main.ts             # 入口文件
```

---

## 🧩 组件规范

### 单文件组件结构
```vue
<!-- UserProfile.vue -->
<script setup lang="ts">
// 1. 导入
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import BaseButton from '@/components/base/BaseButton.vue';

// 2. 类型定义
interface Props {
  userId: string;
  showDetails?: boolean;
}

interface Emits {
  (e: 'update', user: User): void;
  (e: 'delete', userId: string): void;
}

// 3. Props & Emits
const props = withDefaults(defineProps<Props>(), {
  showDetails: true,
});

const emit = defineEmits<Emits>();

// 4. Composables & Stores
const router = useRouter();
const userStore = useUserStore();

// 5. 响应式数据
const loading = ref(false);
const user = ref<User | null>(null);

// 6. 计算属性
const fullName = computed(() => {
  return `${user.value?.firstName} ${user.value?.lastName}`;
});

// 7. 方法
const fetchUser = async () => {
  loading.value = true;
  try {
    user.value = await userStore.fetchUser(props.userId);
  } finally {
    loading.value = false;
  }
};

const handleUpdate = () => {
  if (user.value) {
    emit('update', user.value);
  }
};

// 8. 生命周期
onMounted(() => {
  fetchUser();
});
</script>

<template>
  <div class="user-profile">
    <!-- 模板内容 -->
    <div v-if="loading">Loading...</div>
    <div v-else-if="user">
      <h2>{{ fullName }}</h2>
      <BaseButton @click="handleUpdate">Update</BaseButton>
    </div>
  </div>
</template>

<style scoped lang="scss">
.user-profile {
  padding: 20px;
  
  h2 {
    font-size: 24px;
  }
}
</style>
```

### 组件命名
```typescript
// ✅ 多单词组件名 (避免与 HTML 元素冲突)
UserProfile.vue
DataTable.vue
NavigationBar.vue

// ❌ 单个单词
User.vue
Table.vue

// ✅ 基础组件使用 Base 前缀
BaseButton.vue
BaseInput.vue
BaseIcon.vue

// ✅ 单例组件使用 The 前缀
TheHeader.vue
TheSidebar.vue
TheFooter.vue

// ✅ 紧密耦合的子组件
TodoList.vue
TodoListItem.vue
TodoListItemButton.vue
```

### Props 定义
```vue
<script setup lang="ts">
// ✅ 使用 TypeScript 定义 Props
interface Props {
  // 基础类型
  title: string;
  count: number;
  isActive: boolean;
  
  // 可选属性
  description?: string;
  
  // 联合类型
  size?: 'small' | 'medium' | 'large';
  
  // 复杂类型
  user: {
    id: string;
    name: string;
  };
  
  // 数组
  items: string[];
  users: User[];
  
  // 函数
  onUpdate?: (value: string) => void;
}

// ✅ 使用 withDefaults 设置默认值
const props = withDefaults(defineProps<Props>(), {
  description: '',
  size: 'medium',
  items: () => [],
  onUpdate: undefined,
});

// ❌ 避免使用运行时声明 (不如 TS 类型安全)
// const props = defineProps({
//   title: String,
//   count: Number,
// });
</script>
```

### Emits 定义
```vue
<script setup lang="ts">
// ✅ 类型安全的 Emits
interface Emits {
  // 无参数事件
  (e: 'close'): void;
  
  // 单个参数
  (e: 'update', value: string): void;
  
  // 多个参数
  (e: 'change', id: string, value: number): void;
  
  // 对象参数
  (e: 'submit', data: FormData): void;
}

const emit = defineEmits<Emits>();

// 使用
const handleClick = () => {
  emit('update', 'new value');
};

// ✅ 验证事件参数
const emitWithValidation = defineEmits({
  update: (value: string) => {
    if (value.length > 0) {
      return true;
    }
    console.warn('Invalid value');
    return false;
  },
});
</script>
```

---

## 🎨 Composition API

### 响应式数据
```typescript
import { ref, reactive, readonly, shallowRef } from 'vue';

// ✅ 基础类型使用 ref
const count = ref(0);
const name = ref('');
const isActive = ref(false);

// 访问值
console.log(count.value);  // 0
count.value++;

// ✅ 对象使用 reactive
const state = reactive({
  user: null as User | null,
  loading: false,
  error: null as Error | null,
});

// 直接访问属性
console.log(state.loading);
state.loading = true;

// ✅ 只读数据
const readonlyState = readonly(state);

// ✅ 浅层响应式 (性能优化)
const shallowState = shallowRef({ nested: { count: 0 } });

// ❌ 避免解构 reactive 对象 (会失去响应性)
const { user } = state;  // user 不再是响应式

// ✅ 使用 toRefs
import { toRefs } from 'vue';
const { user, loading } = toRefs(state);
```

### 计算属性
```typescript
import { computed } from 'vue';

// ✅ 只读计算属性
const fullName = computed(() => {
  return `${firstName.value} ${lastName.value}`;
});

// ✅ 可写计算属性
const fullName = computed({
  get: () => `${firstName.value} ${lastName.value}`,
  set: (value) => {
    const [first, last] = value.split(' ');
    firstName.value = first;
    lastName.value = last;
  },
});

// ❌ 避免副作用
const badComputed = computed(() => {
  // 不要在计算属性中修改状态
  count.value++;  // ❌
  return count.value * 2;
});

// ✅ 缓存复杂计算
const expensiveValue = computed(() => {
  return items.value.reduce((sum, item) => sum + item.price, 0);
});
```

### 侦听器
```typescript
import { watch, watchEffect } from 'vue';

// ✅ 侦听单个 ref
watch(count, (newVal, oldVal) => {
  console.log(`Count changed from ${oldVal} to ${newVal}`);
});

// ✅ 侦听多个源
watch([count, name], ([newCount, newName], [oldCount, oldName]) => {
  console.log('Multiple values changed');
});

// ✅ 侦听 reactive 对象的属性
watch(
  () => state.user,
  (newUser, oldUser) => {
    console.log('User changed');
  }
);

// ✅ 深度侦听
watch(
  state,
  (newState) => {
    console.log('State changed deeply');
  },
  { deep: true }
);

// ✅ 立即执行
watch(
  userId,
  (id) => {
    fetchUser(id);
  },
  { immediate: true }
);

// ✅ watchEffect 自动追踪依赖
watchEffect(() => {
  console.log(`Count is: ${count.value}`);
  // 自动追踪 count 的变化
});

// ✅ 停止侦听
const stop = watch(count, () => {});
stop();  // 停止侦听

// ✅ 清理副作用
watchEffect((onCleanup) => {
  const timer = setInterval(() => {}, 1000);
  
  onCleanup(() => {
    clearInterval(timer);
  });
});
```

### 生命周期钩子
```typescript
import {
  onBeforeMount,
  onMounted,
  onBeforeUpdate,
  onUpdated,
  onBeforeUnmount,
  onUnmounted,
} from 'vue';

// ✅ 挂载时获取数据
onMounted(() => {
  fetchData();
});

// ✅ 卸载时清理资源
onUnmounted(() => {
  clearInterval(timer);
  websocket.close();
});

// ✅ 更新前保存滚动位置
onBeforeUpdate(() => {
  scrollPosition = window.scrollY;
});

// ⚠️ 注意: setup 中不能使用 beforeCreate 和 created
// setup 本身就相当于这两个钩子
```

---

## 🎣 Composables (组合式函数)

### 创建 Composable
```typescript
// composables/useUser.ts
import { ref, computed } from 'vue';
import type { User } from '@/types';

// ✅ 标准 Composable 结构
export const useUser = (userId: string) => {
  const user = ref<User | null>(null);
  const loading = ref(false);
  const error = ref<Error | null>(null);

  const isAdmin = computed(() => {
    return user.value?.role === 'admin';
  });

  const fetchUser = async () => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await fetch(`/api/users/${userId}`);
      user.value = await response.json();
    } catch (e) {
      error.value = e as Error;
    } finally {
      loading.value = false;
    }
  };

  const updateUser = async (updates: Partial<User>) => {
    if (!user.value) return;
    
    try {
      await fetch(`/api/users/${userId}`, {
        method: 'PUT',
        body: JSON.stringify(updates),
      });
      Object.assign(user.value, updates);
    } catch (e) {
      error.value = e as Error;
    }
  };

  // 自动加载
  fetchUser();

  return {
    user: readonly(user),
    loading: readonly(loading),
    error: readonly(error),
    isAdmin,
    updateUser,
    refetch: fetchUser,
  };
};

// 使用
const { user, loading, isAdmin, updateUser } = useUser('123');
```

### 常用 Composables 模式
```typescript
// 1. useLocalStorage
export const useLocalStorage = <T>(key: string, defaultValue: T) => {
  const data = ref<T>(defaultValue);

  const loadFromStorage = () => {
    const stored = localStorage.getItem(key);
    if (stored) {
      data.value = JSON.parse(stored);
    }
  };

  watch(
    data,
    (newValue) => {
      localStorage.setItem(key, JSON.stringify(newValue));
    },
    { deep: true }
  );

  onMounted(() => {
    loadFromStorage();
  });

  return data;
};

// 2. useDebounce
export const useDebounce = <T>(value: Ref<T>, delay: number = 300) => {
  const debouncedValue = ref(value.value) as Ref<T>;

  watch(value, (newValue) => {
    const timer = setTimeout(() => {
      debouncedValue.value = newValue;
    }, delay);

    return () => clearTimeout(timer);
  });

  return debouncedValue;
};

// 3. useEventListener
export const useEventListener = (
  target: Ref<EventTarget | null>,
  event: string,
  handler: (e: Event) => void
) => {
  onMounted(() => {
    target.value?.addEventListener(event, handler);
  });

  onUnmounted(() => {
    target.value?.removeEventListener(event, handler);
  });
};
```

---

## 🏪 Pinia 状态管理

### Store 定义
```typescript
// stores/user.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

// ✅ Setup Store (推荐 - 类似 Composition API)
export const useUserStore = defineStore('user', () => {
  // State
  const user = ref<User | null>(null);
  const token = ref<string | null>(null);
  
  // Getters
  const isLoggedIn = computed(() => !!user.value);
  const userName = computed(() => user.value?.name ?? 'Guest');
  
  // Actions
  const login = async (credentials: Credentials) => {
    const response = await authService.login(credentials);
    user.value = response.user;
    token.value = response.token;
  };
  
  const logout = () => {
    user.value = null;
    token.value = null;
  };
  
  return {
    // State
    user,
    token,
    // Getters
    isLoggedIn,
    userName,
    // Actions
    login,
    logout,
  };
});

// ✅ Option Store (传统方式)
export const useUserStore = defineStore('user', {
  state: () => ({
    user: null as User | null,
    token: null as string | null,
  }),
  
  getters: {
    isLoggedIn: (state) => !!state.user,
    userName: (state) => state.user?.name ?? 'Guest',
  },
  
  actions: {
    async login(credentials: Credentials) {
      const response = await authService.login(credentials);
      this.user = response.user;
      this.token = response.token;
    },
    
    logout() {
      this.user = null;
      this.token = null;
    },
  },
});
```

### Store 使用
```vue
<script setup lang="ts">
import { storeToRefs } from 'pinia';
import { useUserStore } from '@/stores/user';

const userStore = useUserStore();

// ✅ 使用 storeToRefs 保持响应性
const { user, isLoggedIn } = storeToRefs(userStore);

// ✅ Actions 可以直接解构
const { login, logout } = userStore;

// 或直接调用
const handleLogin = () => {
  userStore.login({ email, password });
};
</script>
```

---

## 🎨 模板语法

### 指令使用
```vue
<template>
  <!-- ✅ v-if / v-else-if / v-else -->
  <div v-if="loading">Loading...</div>
  <div v-else-if="error">Error: {{ error.message }}</div>
  <div v-else>Content</div>

  <!-- ✅ v-show (频繁切换时使用) -->
  <div v-show="isVisible">Toggle me</div>

  <!-- ✅ v-for with key -->
  <li v-for="item in items" :key="item.id">
    {{ item.name }}
  </li>

  <!-- ❌ 避免 v-if 与 v-for 同时使用 -->
  <!-- <div v-for="item in items" v-if="item.active"> -->

  <!-- ✅ 使用计算属性过滤 -->
  <div v-for="item in activeItems" :key="item.id">
    {{ item.name }}
  </div>

  <!-- ✅ v-model 双向绑定 -->
  <input v-model="name" />
  <input v-model.trim="name" />
  <input v-model.number="age" />

  <!-- ✅ 事件处理 -->
  <button @click="handleClick">Click</button>
  <button @click="count++">Increment</button>
  <form @submit.prevent="handleSubmit">Submit</form>

  <!-- ✅ 动态属性 -->
  <img :src="imageUrl" :alt="imageAlt" />
  <div :class="{ active: isActive, disabled: isDisabled }">
  <div :class="[baseClass, { active: isActive }]">
  <div :style="{ color: textColor, fontSize: fontSize + 'px' }">
</template>

<script setup lang="ts">
const activeItems = computed(() => {
  return items.value.filter(item => item.active);
});
</script>
```

### 插槽
```vue
<!-- 父组件 -->
<template>
  <Card>
    <!-- 默认插槽 -->
    <p>This is default content</p>
    
    <!-- 具名插槽 -->
    <template #header>
      <h1>Title</h1>
    </template>
    
    <template #footer>
      <button>Action</button>
    </template>
    
    <!-- 作用域插槽 -->
    <template #item="{ item, index }">
      <div>{{ index }}: {{ item.name }}</div>
    </template>
  </Card>
</template>

<!-- Card.vue 子组件 -->
<template>
  <div class="card">
    <header v-if="$slots.header">
      <slot name="header" />
    </header>
    
    <main>
      <slot />  <!-- 默认插槽 -->
    </main>
    
    <footer v-if="$slots.footer">
      <slot name="footer" />
    </footer>
    
    <!-- 作用域插槽 -->
    <div v-for="(item, index) in items" :key="item.id">
      <slot name="item" :item="item" :index="index" />
    </div>
  </div>
</template>
```

---

## 🛣️ Vue Router

### 路由配置
```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/Home.vue'),
    },
    {
      path: '/users/:id',
      name: 'user',
      component: () => import('@/views/User.vue'),
      props: true,  // 将路由参数作为 props 传递
    },
    {
      path: '/dashboard',
      component: () => import('@/layouts/DashboardLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'dashboard',
          component: () => import('@/views/Dashboard.vue'),
        },
        {
          path: 'settings',
          name: 'settings',
          component: () => import('@/views/Settings.vue'),
        },
      ],
    },
  ],
});

// 全局前置守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore();
  
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next({ name: 'login' });
  } else {
    next();
  }
});

export default router;
```

### 路由使用
```vue
<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

// 获取路由参数
const userId = computed(() => route.params.id);

// 编程式导航
const goToUser = (id: string) => {
  router.push({ name: 'user', params: { id } });
};

const goBack = () => {
  router.back();
};
</script>

<template>
  <!-- 声明式导航 -->
  <RouterLink :to="{ name: 'home' }">Home</RouterLink>
  <RouterLink :to="`/users/${userId}`">User Profile</RouterLink>
  
  <!-- 渲染路由组件 -->
  <RouterView />
</template>
```

---

## 🧪 测试规范

### 组件测试
```typescript
import { mount } from '@vue/test-utils';
import { describe, it, expect } from 'vitest';
import Button from './Button.vue';

describe('Button', () => {
  it('应该渲染按钮文本', () => {
    const wrapper = mount(Button, {
      slots: {
        default: 'Click me',
      },
    });
    
    expect(wrapper.text()).toBe('Click me');
  });

  it('应该在点击时触发事件', async () => {
    const wrapper = mount(Button);
    
    await wrapper.trigger('click');
    
    expect(wrapper.emitted('click')).toBeTruthy();
  });

  it('禁用状态不应该触发点击', async () => {
    const wrapper = mount(Button, {
      props: {
        disabled: true,
      },
    });
    
    await wrapper.trigger('click');
    
    expect(wrapper.emitted('click')).toBeFalsy();
  });
});
```

---

## ⚡ 性能优化

### 组件优化
```vue
<script setup lang="ts">
// ✅ 异步组件
import { defineAsyncComponent } from 'vue';

const HeavyComponent = defineAsyncComponent(() =>
  import('./HeavyComponent.vue')
);

// ✅ Keep-alive 缓存组件
<template>
  <KeepAlive>
    <component :is="currentView" />
  </KeepAlive>
</template>

// ✅ v-once 静态内容
<template>
  <div v-once>
    {{ expensiveComputation }}
  </div>
</template>

// ✅ v-memo 条件缓存 (Vue 3.2+)
<template>
  <div v-memo="[value1, value2]">
    <!-- 仅当 value1 或 value2 改变时更新 -->
  </div>
</template>
</script>
```

### 列表优化
```vue
<template>
  <!-- ✅ 使用 key -->
  <div v-for="item in items" :key="item.id">
    {{ item.name }}
  </div>

  <!-- ✅ 虚拟滚动 (大列表) -->
  <RecycleScroller
    :items="items"
    :item-size="50"
    key-field="id"
  >
    <template #default="{ item }">
      <div>{{ item.name }}</div>
    </template>
  </RecycleScroller>
</template>
```

---

**继承自**: [全局开发规范](./global.md)
**最后更新**: 2024-12-16