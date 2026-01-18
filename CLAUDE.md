# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

FlowAI 是一个 AI 工作流设计与演进仓库，提供可复用的 AI Skills、Agent 协作范式和工作流自动化能力。目标是让 AI 从"工具"进化为融入工程体系的工作流能力。

## 仓库结构

```
flow-ai/
├── skills/              # AI Skill 定义（Claude Code 技能）
│   ├── code_*          # 代码相关技能（ci, cr, git-wt, master 等）
│   ├── post_*          # 文章生成技能
│   ├── fs_*            # 文件系统操作技能
│   └── ui-ux-pro-max/  # UI/UX 设计智能技能
├── rules/              # 开发规范与模板
│   ├── global.md       # 全局开发规范
│   ├── stacks/         # 技术栈规范（react, vue, nodejs）
│   └── templates/      # 项目模板
```

## Skill 架构

每个 Skill 是自包含模块：
- `SKILL.md` - 主定义文件，含 frontmatter（name, description）和指令
- `scripts/` - Python 或 Bash 辅助脚本
- `references/` - 参考文档
- `README.md` - 可选的详细文档

### Skill 分类

**代码技能** (`code_*`):
- `code_ci` - 规范提交生成，支持自动拆分检测
- `code_cr` - 深度代码评审，按严重性排序
- `code_master` - 工程标准化流水线（5 步工作流）
- `code_git-wt` - Git worktree 管理
- `code_design-guard` - 架构边界守护
- `code_quality-gate` - 测试计划与风险评估
- `code_style-linter-guard` - 命名/格式/类型严谨性

**内容技能** (`post_*`):
- `post_master` - 文章生成编排器（mode 0/1/2）
- `post_write` - 文章正文写作，三遍审校
- `post_prep` - 内容摘要提取
- `post_analyze` - 多篇文章分析综合
- `post_extra` - 配套文档生成
- `publish_wx-assets` - 微信发布素材

**文件技能** (`fs_*`):
- `fs_detect` - 草稿目录检测/创建
- `fs_next-id` - 获取下一个文章 ID
- `fs_write` - 写入草稿与配套文件
- `publish_github-go` - 发布草稿到目标目录并更新映射
- `fs_update` - 更新已发布文章

### 脚本执行

技能使用 Python 3 脚本，执行模式：
```bash
python3 skills/<skill_name>/scripts/<script>.py [args]
```

UI/UX 技能搜索：
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<关键词>" --domain <domain>
```

## 核心工作流

### Code Master 流水线（5 步）
1. `spec_clarifier` - 定义验收标准与边界
2. `code_design-guard` - 检查架构合规性
3. `code_style-linter-guard` - 验证代码规范
4. `code_quality-gate` - 测试计划与风险评估
5. `delivery_packager` - 生成提交信息与 PR 描述

输出到 `docs/cr_local/`，序号递增。

### Post Master 模式
- **mode=0**: 基于对话/笔记生成
- **mode=1**: 优化已有文章
- **mode=2**: 基于分析报告综合创作

草稿目录优先级：`docs/post_local/` > `docs/post/` > `post/`

## 开发规范

`rules/` 目录包含分层规范体系：

1. **项目规范**（最高优先级）- `./claude.md`
2. **技术栈规范** - `rules/stacks/{react,vue,nodejs}.md`
3. **全局规范** - `rules/global.md`

核心标准：
- 4 空格缩进
- Conventional Commits 格式
- 文档中文优先，ASCII 标点
- 输出文档默认到 `docs/`

## 文档输出规范

遵循 `code_docs-creator` 标准：
- 格式：Markdown，标题层级清晰
- 命名：`001_主题.md` 格式
- 必须标注生成/更新日期
- 中文优先，必要时补充英文术语
