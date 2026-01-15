---
name: post_master
description: 技术文章生成、发布与管理的完整工作流。用于用户要求生成文章、优化文章、综合参考文献、发布草稿或更新已发布文章时。
---

# Post Master

技术文章的生成、发布与版本管理统一入口。

## 快速开始

```bash
# 生成文章
/post_master                      # 基于对话生成
/post_master <文章路径>            # 优化单篇
/post_master --refs <路径>         # 综合参考

# 发布管理
/post_master --publish [草稿]      # 发布草稿
/post_master --update [草稿]       # 更新已发布
/post_master --status              # 查看状态
```

---

## 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--year` | 当前年 | 发布年份 |
| `--style` | - | tutorial/guide/reference |
| `--level` | - | beginner/intermediate/advanced |
| `--model` | sonnet | haiku/sonnet/opus |
| `--length` | medium | short/medium/long |
| `--companion` | false | 生成配套文档 |
| `--no-preprocess` | false | 跳过预处理 |
| `--publish` | - | 发布草稿 |
| `--update` | - | 更新已发布 |
| `--status` | - | 查看状态 |
| `--list-drafts` | - | 列出草稿 |
| `--list-published` | - | 列出已发布 |

---

## 核心流程

### 1. 参数解析

```
确定模式:
- 默认输入 → mode=0 (对话生成)
- 单篇路径 → mode=1 (优化文章)
- --refs → mode=2 (综合参考)

提取参数: style, level, length, companion, no_preprocess
```

### 2. 文件操作 (fs_* skills)

```
IF 生成模式:
    fs_detect → 获取草稿目录
    fs_next-id → 获取文章 ID

IF --publish:
    fs_publish → 发布到正式目录

IF --update:
    fs_update → 更新已发布文章
```

### 3. 内容生成 (post_* skills)

**执行路径**：

```
mode=0:
    IF NOT --no-preprocess:
        post_prep(RAW_CONTENT) → processed_context
    ELSE:
        processed_context = RAW_CONTENT

    post_write(processed_context, mode=0, length, style, level) → {title, content}

mode=1:
    post_write(ARTICLE_PATH, mode=1, length, style, level) → {title, content}

mode=2:
    post_analyze(REFERENCE_ARTICLES) → analysis_report
    post_write(analysis_report, mode=2, length, style, level) → {title, content}

IF --companion:
    post_extra(content, processed_context) → companion_content
```

### 4. 写入文件

```
fs_write(
    draft_dir = fs_detect 结果,
    article_id = fs_next-id 结果,
    title = post_write 输出的 title,
    content = post_write 输出的 content,
    companion_content = post_extra 输出 (可选)
)
```

---

## 目录配置

**草稿目录** (优先级):
1. `docs/post_local/`
2. `docs/post/`
3. `post/` (当前目录)
4. 不存在时创建 `docs/post_local/`

**发布目录**:
`/Users/sggmico/ws/cc/build-blog/{year}/`

---

## Skills 依赖

**内容类**: post_prep, post_analyze, post_write, post_extra
**文件类**: fs_detect, fs_next-id, fs_write, fs_publish, fs_update

---

## 输出

- **草稿**: `{草稿目录}/{ID}_{title}.md`
- **配套**: `{草稿目录}/{ID}_{title}_扩展信息.md` (--companion)
- **发布**: `/Users/sggmico/ws/cc/build-blog/{year}/{ID}_{title}.md`

---

## Token 优化原则

1. **条件调用**:
   - `post_prep` 仅 mode=0 且未禁用时
   - `post_analyze` 仅 mode=2 时
   - `post_extra` 仅 --companion 时

2. **模型选择**:
   - 默认 sonnet (平衡质量与成本)
   - 简单优化用 haiku (--model=haiku)
   - 高质量创作用 opus (--model=opus)

3. **长度控制**:
   - short: 800-1500 字
   - medium: 1500-3000 字
   - long: 3000-5000 字

---

## 错误处理

如果 skill 调用失败:
1. 记录错误到日志
2. 返回部分结果 (如果可能)
3. 向用户说明失败原因和建议

---

## 质量保证

文章质量由 `post_write` skill 保证:
- ✅ 三遍审校 (内容/风格/细节)
- ✅ AI 味降重
- ✅ 技术准确性
- ✅ 可运行代码示例

详见: `post_write/SKILL.md`

---

**版本**: v3.0
**日期**: 2026-01-12
**说明**: 整合 cc-post 命令层与 post-content-writer agent 层
