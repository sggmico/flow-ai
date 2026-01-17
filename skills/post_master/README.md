# Post Master - 技术文章生成完整工作流

## 概述

`post_master` 是技术文章生成、优化、发布与管理的统一入口，整合了原 `cc-post` 命令和 `post-content-writer` agent 的所有能力。

## 架构优势

**v3.0 架构** (当前):
```
用户 → post_master skill → post_*/fs_* skills
```

**v2.x 架构** (旧版):
```
用户 → cc-post command → post-content-writer agent → post_*/fs_* skills
```

**改进**:
- ✅ 减少一层抽象 (3层→2层)
- ✅ 降低认知负担
- ✅ 更清晰的错误反馈
- ✅ 更好的 token 优化
- ✅ 符合 Skills 扁平化趋势

---

## 使用场景

### 场景 1: 对话生成文章

```bash
# 基于当前对话上下文生成文章
/post_master
```

**流程**:
1. 自动提取对话内容
2. `post_prep` 预处理上下文
3. `post_write` 生成文章 (mode=0)
4. 写入草稿目录

**适用于**:
- 技术讨论总结
- 问题解决记录
- 学习笔记整理

---

### 场景 2: 优化已有文章

```bash
# 优化单篇文章
/post_master ~/docs/article.md

# 指定风格和长度
/post_master ~/docs/article.md --style=tutorial --length=long
```

**流程**:
1. 读取文章内容
2. `post_write` 优化文章 (mode=1)
3. 写入草稿目录

**适用于**:
- 文章润色
- 风格调整
- 质量提升

---

### 场景 3: 综合参考文献

```bash
# 综合多篇参考文章
/post_master --refs ~/docs/references/

# 综合单篇参考
/post_master --refs ~/docs/article1.md
```

**流程**:
1. 读取所有参考文章
2. `post_analyze` 深度分析
3. `post_write` 综合创作 (mode=2)
4. 写入草稿目录

**适用于**:
- 综述文章
- 技术对比
- 最佳实践总结

---

### 场景 4: 生成配套文档

```bash
# 生成文章 + 配套内容
/post_master --companion

# 优化文章 + 配套内容
/post_master ~/docs/article.md --companion
```

**配套内容包括**:
- 学习路径
- 常见问题 (FAQ)
- 参考资源
- 实战清单

**适用于**: 系统性技术教程

---

### 场景 5: 发布管理

```bash
# 发布最新草稿
/post_master --publish

# 发布指定草稿
/post_master --publish 001_文章标题.md

# 更新已发布文章
/post_master --update 001_文章标题.md

# 查看状态
/post_master --status

# 列出所有草稿
/post_master --list-drafts

# 列出已发布文章
/post_master --list-published
```

---

## 参数详解

### 内容参数

#### `--style`

文章风格选择:

| 值           | 说明   | 适用场景        |
| ----------- | ---- | ----------- |
| `tutorial`  | 教程风格 | 手把手教学，步骤详细  |
| `guide`     | 指南风格 | 概念讲解 + 实践建议 |
| `reference` | 参考风格 | API 文档，配置说明 |

#### `--level`

读者水平:

| 值 | 说明 | 特点 |
|----|------|------|
| `beginner` | 初学者 | 概念解释详细，示例简单 |
| `intermediate` | 中级 | 假设有基础，重点讲进阶 |
| `advanced` | 高级 | 深入原理，复杂场景 |

#### `--length`

文章长度:

| 值 | 字数范围 | Token 消耗 |
|----|---------|-----------|
| `short` | 800-1500 | 低 (~2K) |
| `medium` | 1500-3000 | 中 (~5K) |
| `long` | 3000-5000 | 高 (~10K) |

### 模型参数

#### `--model`

| 值 | 适用场景 | 成本 | 质量 |
|----|---------|------|------|
| `haiku` | 简单优化 | 💰 | ⭐⭐⭐ |
| `sonnet` | 常规创作 | 💰💰 | ⭐⭐⭐⭐ |
| `opus` | 高质量创作 | 💰💰💰 | ⭐⭐⭐⭐⭐ |

### 优化参数

#### `--companion`

生成配套扩展文档，包含:
- 📚 学习路径建议
- ❓ 常见问题解答
- 🔗 参考资源链接
- ✅ 实战检查清单

**Token 影响**: +3K~5K

#### `--no-preprocess`

跳过 `post_prep` 预处理。

**使用场景**:
- 输入已经是结构化内容
- 想要节省 token
- mode=1 或 mode=2 (自动跳过)

**Token 节省**: ~2K

---

## 完整示例

### 示例 1: 从零生成教程

```bash
/post_master --style=tutorial --level=beginner --length=medium --companion
```

**执行过程**:
1. 提取对话内容
2. `post_prep` 预处理 (~2K tokens)
3. `post_write` 生成教程 (~5K tokens)
4. `post_extra` 生成配套 (~3K tokens)
5. `fs_detect` + `fs_next-id` + `fs_write`

**总 Token**: ~10K
**输出文件**:
- `001_教程标题.md`
- `001_教程标题_扩展信息.md`

---

### 示例 2: 优化文章 (省钱模式)

```bash
/post_master ~/article.md --model=haiku --length=short
```

**执行过程**:
1. 读取文章
2. `post_write` 优化 (mode=1, haiku)
3. `fs_write`

**总 Token**: ~1.5K
**成本**: 极低

---

### 示例 3: 综合高质量文章

```bash
/post_master --refs ~/refs/ --model=opus --length=long --companion
```

**执行过程**:
1. 读取所有参考
2. `post_analyze` 深度分析 (~8K tokens)
3. `post_write` 综合创作 (opus, ~12K tokens)
4. `post_extra` 生成配套 (~4K tokens)
5. `fs_write`

**总 Token**: ~24K
**质量**: 最高

---

## Token 优化策略

### 策略 1: 合理选择模型

| 任务类型 | 推荐模型 | 原因 |
|---------|---------|------|
| 简单润色 | haiku | 质量够用，成本低 |
| 日常创作 | sonnet | 平衡质量与成本 |
| 重要文章 | opus | 质量最高 |

### 策略 2: 控制文章长度

| 场景 | 推荐长度 | 原因 |
|------|---------|------|
| 快速笔记 | short | 节省 token |
| 常规教程 | medium | 适中 |
| 深度指南 | long | 完整性优先 |

### 策略 3: 按需生成配套

只在需要系统性教程时使用 `--companion`，可节省 ~3K tokens。

### 策略 4: 跳过预处理

mode=1 (优化文章) 和 mode=2 (综合参考) 自动跳过预处理，无需手动指定。

---

## 目录结构

### 草稿目录

**优先级**:
1. `docs/post_local/` (推荐 - 不提交到 Git)
2. `docs/post/` (备选)
3. `post/` (当前目录)

**自动创建**: 如果都不存在，自动创建 `docs/post_local/`

**建议配置** (`.gitignore`):
```
docs/post_local/
```

### 发布目录

**固定路径**: `/Users/sggmico/ws/cc/build-blog/{year}/`

**目录结构**:
```
build-blog/
├── 2025/
│   ├── 001_文章标题.md
│   └── 002_另一篇.md
└── 2026/
    └── 001_新年第一篇.md
```

### 文件命名

**格式**: `{ID}_{标题}.md`

**示例**:
- `001_Claude_Code_使用指南.md`
- `002_React_性能优化技巧.md`

**ID 规则**:
- 三位数字 (001-999)
- 自动递增
- 由 `fs_next-id` 计算

---

## 与旧版对比

| 功能 | v2.x (旧) | v3.0 (新) | 改进 |
|------|-----------|-----------|------|
| 调用方式 | `/cc-post` | `/post_master` | 更清晰 |
| 架构层级 | 3 层 | 2 层 | 更简洁 |
| 能力完整性 | ✅ | ✅ | 保持 |
| Token 优化 | ✅ | ✅✅ | 更优 |
| 错误反馈 | 间接 | 直接 | 更清晰 |
| 可维护性 | 中 | 高 | 更易维护 |

---

## 故障排除

### 问题 1: 草稿目录未找到

**错误**: `草稿目录不存在`

**解决**:
```bash
# 手动创建
mkdir -p docs/post_local/
```

### 问题 2: 文章 ID 冲突

**错误**: `文章 ID 001 已存在`

**解决**:
- 自动跳过已存在的 ID
- 使用下一个可用 ID

### 问题 3: 发布目录权限错误

**错误**: `无法写入发布目录`

**解决**:
```bash
# 检查目录权限
ls -la /Users/sggmico/ws/cc/build-blog/

# 修改权限
chmod -R 755 /Users/sggmico/ws/cc/build-blog/
```

---

## 常见问题 (FAQ)

**Q: 可以同时生成多篇文章吗？**
A: 不可以。每次调用生成一篇文章。如需多篇，多次调用。

**Q: 如何删除草稿？**
A: 直接删除文件即可，skill 不管理删除。

**Q: 可以修改已发布的文章吗？**
A: 使用 `--update` 参数更新已发布文章。

**Q: 配套文档可以单独生成吗？**
A: 不可以，必须和主文章一起生成。

**Q: 支持其他发布目录吗？**
A: 当前固定为 `/Users/sggmico/ws/cc/build-blog/`，如需修改需编辑 `publish_github-go` skill。

---

## 迁移指南

### 从 cc-post 迁移

**旧命令**:
```bash
/cc-post --refs ~/refs/ --style=tutorial
```

**新命令**:
```bash
/post_master --refs ~/refs/ --style=tutorial
```

**变更**:
- ✅ 命令名称: `/cc-post` → `/post_master`
- ✅ 参数完全兼容
- ✅ 功能完全一致

---

## 版本历史

### v3.0 (2026-01-12)
- 整合 cc-post 命令层
- 整合 post-content-writer agent 层
- 优化 token 使用
- 改进错误处理

### v2.x (2026-01-06)
- cc-post + post-content-writer 架构
- 分层设计

---

**维护者**: Sggmico
**最后更新**: 2026-01-12
**相关文档**:
- `post_write/SKILL.md` - 写作质量标准
- `fs_detect/SKILL.md` - 目录检测
- `publish_github-go/SKILL.md` - 发布流程
