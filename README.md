# flow-ai

Engineering AI agents into real workflows.

## 简介

flow-ai 是一个工程化的 AI 工作流仓库, 以 skills 与可组合工作流为核心, 目标是让 Agent 能力可复用、可演进、可落地.

## 核心能力

- **Skills**: 可复用的能力模块, 以 `SKILL.md` 为主定义
- **Commands**: 统一的人机与 Agent 调用入口
- **Agents**: 角色化与协作化的智能体模型
- **Workflows**: 面向真实场景的自动化编排与执行

## 适用场景

- AI 驱动的软件开发流程
- 多 Agent 协作与任务编排
- 自动化研究与分析流水线
- AI 运维与知识系统
- Agent 化产品原型

## 快速开始

### 一键安装(推荐)

```bash
curl -fsSL https://raw.githubusercontent.com/sggmico/flow-ai/main/scripts/install-skills.sh | bash
```

可选参数示例:

```bash
# 安装到自定义目录
CODEX_SKILLS_DIR="$HOME/.codex/skills" bash scripts/install-skills.sh --install

# 安装指定版本
bash scripts/install-skills.sh --version v0.1.0

# 使用镜像或自定义下载源
bash scripts/install-skills.sh --mirror https://example.com/releases
```

### 手动安装(可审阅)

```bash
git clone https://github.com/sggmico/flow-ai.git
cd flow-ai
skills/skill/skill-multi-sync/scripts/sync_skills.sh
```

### 更新与回滚

```bash
# 更新(等同安装)
bash scripts/install-skills.sh --update

# 回滚到最近一次备份
bash scripts/install-skills.sh --rollback

# 卸载(会先备份)
bash scripts/install-skills.sh --uninstall
```

### 快速使用

```bash
~/.codex/superpowers/.codex/superpowers-codex use-skill post-radar
```

## Release 产物

```bash
# 生成 release 资产(打包 skills + 生成 sha256)
python3 scripts/gen-skills-manifest.py
bash scripts/release-skills.sh
```

### GitHub Actions 发布

```bash
# 打 tag 触发自动发布
git tag v1.0.0
git push origin v1.0.0
```

## 使用说明

- 默认安装到 `~/.codex/skills`, 可用 `CODEX_SKILLS_DIR` 覆盖.
- 安装过程会对 skills 扁平化, 保持原始命名, 与本地同步产出一致.
- 如遇同名冲突会中止并生成 `skills/sync_conflicts.txt`.

## 仓库结构

```text
flow-ai/
├─ skills/        # Agent 能力模块
├─ commands/      # 指令系统规范
├─ agents/        # Agent 角色与协作模型
├─ workflows/     # 自动化与编排模板
├─ patterns/      # 工程模式
├─ infra/         # MCP / API / Runtime 集成
├─ examples/      # 实战场景
├─ docs/          # 方法论与设计原则
└─ manifesto.md   # 项目宣言
```

## 参与共建

欢迎提交:

- 新的 skills / agents / workflows
- 工程模式与最佳实践
- 工具链、基础设施与运行时集成
- 文档与真实案例沉淀

## License

MIT
