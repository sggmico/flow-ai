---
name: blog-format
description: 处理 build-blog 文章索引与提交流程，适用于在 /Users/sggmico/ws/cc/build-blog/ 下新增技术文章时需要维护 README 与生成正式提交的场景。
---

# Blog Format

以 `/Users/sggmico/ws/cc/build-blog/` 为默认目录，辅助新增文章的索引更新与规范化提交。

## 工作目录

- 默认切到 `/Users/sggmico/ws/cc/build-blog/`（即 `build-blog/` 的 root）。
- 仅在必要时接受 `--workdir` 显式覆盖。

## 节点 1：定位新文章

1. **输入参数**：若提供 `文章路径`，使用该路径；否则默认：
   - 仅扫描当天新增的 `*.md` 文件；若大量文章，优先 `2026/`、`2025/` 等最新年份目录。
   - 跳过已在 README 中出现的编号。
2. 若未发现新文章，记录理由（名称/编号重复、文件未提交）并退出。
3. 解析出 `year`, `id`, `title`, `month` 用于后续流程。

## 节点 2：更新 README

1. 读取 `README.md`，锁定 `## {year}` 段。
2. 重建该段条目：按照 `ID` 降序排序。
3. 插入新条目（使用 `- [ID_Title](year/slug.md) —— MMM DD` 格式）。
4. 必要时自动创建该段落（若年份不存在）。
5. 写入前校验：确保该段 `ID` 递减、链接可访问并 URL 编码。
6. 变更数量有限（最多当前年份 50 条）以节约 token；避免遍历全 repo。

## 节点 3：Git 处理（不推送）

- **前提**：`README` 或文章有改动。
- 使用 `skills/code/code-ci` 执行标准 `git add`+`commit` 流程；提交消息由 `code-ci` 生成（如 `feat(blog): 新增XXX` 或 `chore(blog): 更新 README 索引`）。
- 不在本 skill 中执行 `git push`。

## 反馈

- 明确说明是否更新 README 与提交。
- 记录跳过理由（无新文章、重复编号、未提交文件）。
- 若使用自定义目录，反映实际 `--workdir`。
