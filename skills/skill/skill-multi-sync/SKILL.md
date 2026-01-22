---
name: skill-multi-sync
description: 同步当前仓库的 skills 目录到多个预设的本地目录，以保持能力与文件一致。同步前会将各命名空间目录下的 skill 子目录扁平化为平级结构并检测同名冲突。用于需要批量同步/更新本仓库技能到默认目录、避免手动复制或遗漏更新时使用。
---

# Skill Multi Sync

## 快速使用

- 在仓库根目录执行：`skills/skill/skill-multi-sync/scripts/sync_skills.sh`
- 只做预览：`SYNC_DRY_RUN=1 skills/skill/skill-multi-sync/scripts/sync_skills.sh`
- 指定自定义目标目录（逗号或冒号分隔）：`SYNC_TARGETS="$HOME/foo,$HOME/bar" skills/skill/skill-multi-sync/scripts/sync_skills.sh`

## 约定

- 同步前会将各命名空间目录下的 skill 子目录扁平化为平级结构再同步到目标目录
- 扁平化时如出现同名冲突会终止并提示冲突清单
- 默认同步当前目录下的 `skills/` 到六个目标目录
- 可通过 `SYNC_TARGETS` 覆盖默认目标目录列表
- 会覆盖目标目录中同名文件并删除多余文件
- 目标目录不存在时自动创建
- 不会删除或变动目标目录中的隐藏文件（例如以 `.` 开头的文件）

## 排查

- 如果没有 `rsync`，先安装，或临时用 `cp -a skills/. ~/.claude/skills/` 方式手动同步
