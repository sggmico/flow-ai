---
name: post-master
description: 技术文章生成、发布与管理的完整工作流。用于用户要求生成文章、优化文章、综合参考文献、发布草稿或更新已发布文章时。
---

# Post Master

技术文章的生成、发布与版本管理统一入口。

## 快速开始

```bash
# 生成文章
/code-master                      # 基于对话生成
/code-master <文章路径>            # 优化单篇
/code-master --refs <路径>         # 综合参考

# 发布管理
/code-master --publish [草稿]      # 发布草稿
/code-master --update [草稿]       # 更新已发布
/code-master --status              # 查看状态
```

---

## 参数

| 参数                 | 默认值    | 说明                             |
| ------------------ | ------ | ------------------------------ |
| `--year`           | 当前年    | 发布年份                           |
| `--style`          | -      | tutorial/guide/reference       |
| `--level`          | -      | beginner/intermediate/advanced |
| `--model`          | sonnet | haiku/sonnet/opus              |
| `--length`         | medium | short/medium/long              |
| `--companion`      | false  | 生成配套文档                         |
| `--no-preprocess`  | false  | 跳过预处理                          |
| `--publish`        | -      | 发布草稿                           |
| `--update`         | -      | 更新已发布                          |
| `--status`         | -      | 查看状态                           |
| `--list-drafts`    | -      | 列出草稿                           |
| `--list-published` | -      | 列出已发布                          |

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
    IF user provided target output directory:
        一级目录 = user provided target output directory
    ELSE:
        先询问用户：使用默认草稿目录规则，还是临时指定目录（作为一级目录）
        IF 临时指定:
            一级目录 = user provided target output directory
        ELSE:
            fs-detect → 获取草稿目录 (作为一级目录)
    确认一级目录后，需询问用户是否再以当前使用的生成模型名创建子目录，作为最终草稿目录
    fs-next-id → 获取文章 ID

IF --publish:
    publish-github-go → 发布到正式目录

IF --update:
    fs-update → 更新已发布文章
```

### 3. 内容生成 (post_* skills)

**执行路径**：

```
mode=0:
    IF NOT --no-preprocess:
        post-prep(RAW_CONTENT) → processed_context
    ELSE:
        processed_context = RAW_CONTENT

    post-write(processed_context, mode=0, length, style, level) → {title, content}

mode=1:
    post-write(ARTICLE_PATH, mode=1, length, style, level) → {title, content}

mode=2:
    post-analyze(REFERENCE_ARTICLES) → analysis_report
    post-write(analysis_report, mode=2, length, style, level) → {title, content}
    IF --refs 是目录:
        post-analyze 按目录级输入处理(见 analyze/references/dir-ingest.md)

IF --companion:
    post-extra(content, processed_context) → companion_content
```

### 4. 写入文件

```
fs-write(
    dir = target_output_dir OR fs-detect 结果,
    article_id = fs-next-id 结果,
    title = post-write 输出的 title,
    content = post-write 输出的 content,
    companion_content = post-extra 输出 (可选)
)
```

---

## 风格稳定（低成本）

动作:
- 风格-锚点-应用
- 结构-模板-一致

规则:
- 仅在 post-write 阶段约束输出结构
- 读取 `../post-write/references/style-profile.md` 获取锚点与固定结构
- 不改动原有能力与流程

---

## 目录配置

**草稿目录**:
1. 先确认一级目录：使用默认草稿目录规则或临时指定目录
2. 默认草稿目录规则 (作为一级目录) 的优先级:
   - `docs/post_local/`
   - `docs/post/`
   - `post/` (当前目录)
   - 不存在时创建 `docs/post_local/`
3. 确认一级目录后，询问是否以当前使用的生成模型名创建子目录，作为最终草稿目录

**发布目录**:
`/Users/sggmico/ws/cc/build-blog/{year}/`

> ⚠️ 如果用户明确指定输出目录（例如 `/Users/.../post/...`），应直接写入该目录，避免在默认草稿目录中生成额外副本。

---

## Skills 依赖

**内容类**: post-prep, post-analyze, post-write, post-extra
**文件类**: fs-detect, fs-next-id, fs-write, publish-github-go, fs-update

---

## 输出

- **草稿**: `{草稿目录}/{ID}_{title}.md`
- **配套**: `{草稿目录}/{ID}_{title}_扩展信息.md` (--companion)
- **发布**: `/Users/sggmico/ws/cc/build-blog/{year}/{ID}_{title}.md`

> ⚠️ 若用户声明具体输出路径，则覆盖以上草稿目录定义，最终文件直接落在该目标目录而不再额外生成其它副本。

---

## Token 优化原则

1. **条件调用**:
   - `post-prep` 仅 mode=0 且未禁用时
   - `post-analyze` 仅 mode=2 时
   - `post-extra` 仅 --companion 时

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

文章质量由 `post-write` skill 保证:
- ✅ 三遍审校 (内容/风格/细节)
- ✅ AI 味降重
- ✅ 技术准确性
- ✅ 可运行代码示例

详见: `post-write`

---

**版本**: v3.1
**日期**: 2026-01-15
**说明**: 增加风格锚点引用，保持输出稳定
