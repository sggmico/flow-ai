---
name: post-trend-radar
description: Use when 需要查看 GitHub 热门项目或生成趋势文章.
---
# Post Trend Radar v3.1

GitHub 趋势捕获 + 单文档输出。

## 硬规则

- 真实性: 仅基于真实 GitHub 数据
- 口径标注: Star/更新时间必须注明截止日期
- Token 优先: 单次查询, 不做多轮交互
- 输出规范: 遵循 code-docs-creator

---

## 执行流程 (4 步)

### Step 1: 快速确认 (单次交互)

一次性确认: 时间窗口 + 赛道 + 输出数量

默认值: past_week / AI-Agent / Top 5

### Step 2: 数据获取 (单次查询)

先扫描历史 summary.md, 排除已出现仓库, 再做单次 gh 查询。

**优先使用 gh CLI**:

```bash
gh api search/repositories \
  -f q="stars:>1000 pushed:>$(date -v-7d +%Y-%m-%d) topic:{domain}" \
  -f sort=stars -f per_page=15 \
  --jq '.items[] | {name:.full_name, stars:.stargazers_count, desc:.description, lang:.language, license:.license.spdx_id, updated:.pushed_at}'
```

**禁止**: 多次查询、WebFetch、额外 API 调用

### Step 3: 筛选 Top N

基于返回数据直接筛选, 标准: Stars + 更新时间 + 描述清晰度

去重规则:

- summary.md 中已出现过的仓库必须排除
- 排除后仍需输出 5 个, 按权重从高到低顺位补足

### Step 4: 生成文档

调用 code-docs-creator 规范输出。

### Step 5: 更新 summary.md (单次写入)

文档输出后, 立即把本次 5 个仓库写入 summary.md。
同一天不替换旧行, 直接插入新行, 保持倒序。

---

## 文档模板

```markdown
# {时间} {赛道} 趋势观察

> 数据截止: {日期} | 时间窗口: {window}

---

## 01 {项目名}

- **GitHub**: {url}
- **Stars**: {count} | **语言**: {lang} | **许可**: {license}
- **定位**: {一句话说明}
- **亮点**: {核心特性, 2-3 个}
- **适合**: {目标用户}

---

## 02 {项目名}
...

---

## 趋势信号

- {信号1}
- {信号2}
- **最值得关注**: {项目} - {原因}
```

---

## 输出配置

- 目录: `/Users/sggmico/course/101/post/github-trend/[当前月份，月份格式如：1月]/[当前日期， 日期格式 01]/`
- 命名: `{NNN}_{赛道}-trend.md` (如: `003_ai-agent-trend.md`)
- 单文档输出

---

## 参考资料

- 赛道权重与传播价值: `references/criteria.md`
- 文章模板: `references/templates.md`
- summary: `/Users/sggmico/course/101/post/github-trend/summary.md`
 - 更新: `scripts/score_repos.py --update-summary --model <model>`

---

## Quick Reference

- 入口: `scripts/fetch_trending.py` + `scripts/score_repos.py`
- 单次查询: gh search, `--limit` 建议 >= 50
- 去重: 读取 summary.md, 过滤已出现仓库
- Top 5: 评分后取前 5, 不足则从低到高补足
- 汇总: `--update-summary --model <model>`
- 同日: 只插入, 不替换

## Common Mistakes

- 忘记读取 summary.md 导致重复仓库
- 过滤后未补足 5 个输出
- 为补足数量进行二次 API 查询 (禁止)
- 忘记在输出后更新 summary.md
- 同一天误替换旧行

## Rationalization Table

| Excuse                 | Reality                              |
| ---------------------- | ------------------------------------ |
| "先出结果, 之后再去重" | 去重必须在评分前完成, 否则排序被污染 |
| "数量不够就再请求一次" | 违反单次查询规则                     |

## Red Flags

- "先写, 后过滤"
- "不够 5 个就加一次查询"
- "summary.md 可能过期, 先跳过"

**版本**: v3.1
**更新日期**: 2026-01-28
**变更**: 精简为单文档输出, 去除多平台适配, 固定命名 {赛道}-trend
