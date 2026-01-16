# Skill Multi Sync

用于将当前仓库的 `skills/` 同步到默认或自定义技能目录。

## 快速使用

- 正常同步：`skills/skill_multi-sync/scripts/sync_skills.sh`
- 预览模式：`SYNC_DRY_RUN=1 skills/skill_multi-sync/scripts/sync_skills.sh`

## 自定义目标目录

通过 `SYNC_TARGETS` 指定目标目录（逗号或冒号分隔）：

```bash
SYNC_TARGETS="$HOME/foo,$HOME/bar" skills/skill_multi-sync/scripts/sync_skills.sh
SYNC_DRY_RUN=1 SYNC_TARGETS="$HOME/foo:$HOME/bar" skills/skill_multi-sync/scripts/sync_skills.sh
```

## 自然语言示例

1. "把这个仓库的 skills 同步到我的 ~/.claude/skills、~/.codex/skills、~/.gemini/skills。"
2. "我更新了 skills 目录，帮我一键同步到三个默认目录。"
3. "避免手动复制技能文件，请把当前仓库 skills 同步到所有默认位置。"
4. "同步本仓库 skills 到 Claude/Codex/Gemini 的默认技能目录。"
5. "我需要保持 ~/.claude/skills 和仓库的 skills 一致，请执行同步。"
6. "请把 skills 目录更新到所有默认技能路径，确保一致。"
7. "把当前仓库的 skills 同步到 /Users/sggmico/skills-a 和 /Users/sggmico/skills-b。"
8. "同步本仓库 skills 到 /opt/skills/custom 和 ~/tmp/skills。"
9. "只同步到这两个目录：/data/skills、/backup/skills。"
10. "同步 skills 到 /Users/sggmico/dev/skills（不要默认目录）。"

## 注意事项

- 默认同步到 `~/.claude/skills`、`~/.codex/skills`、`~/.gemini/skills`、`/Users/sggmico/ws/cc/learn-flow/.gemini/skills`、`/Users/sggmico/ws/cc/agent-flow-ws/.gemini/skills`
- 目标目录不存在时会自动创建
- 会覆盖同名文件并删除多余文件
- 不会删除或变动目标目录中的隐藏文件（例如以 `.` 开头的文件）
