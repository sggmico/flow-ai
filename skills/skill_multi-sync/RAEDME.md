# Skill Multi Sync 使用场景示例
以下是自然语言请求的常见场景示例（用于触发或说明该技能）：
1. "把这个仓库的 skills 同步到我的 ~/.claude/skills、~/.codex/skills、~/.gemini/skills。"
2. "我更新了 skills 目录，帮我一键同步到三个默认目录。"
3. "避免手动复制技能文件，请把当前仓库 skills 同步到所有默认位置。"
4. "同步本仓库 skills 到 Claude/Codex/Gemini 的默认技能目录。"
5. "我需要保持 ~/.claude/skills 和仓库的 skills 一致，请执行同步。"
6. "请把 skills 目录更新到所有默认技能路径，确保一致。"
提示：
- 预览模式：`SYNC_DRY_RUN=1 skills/skill_multi-sync/scripts/sync_skills.sh`
- 正常同步：`skills/skill_multi-sync/scripts/sync_skills.sh`
- 不会删除或变动目标目录中的隐藏文件（例如以 `.` 开头的文件）
