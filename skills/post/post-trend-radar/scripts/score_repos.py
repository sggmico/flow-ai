#!/usr/bin/env python3
"""
仓库评分与排序脚本

用法:
    python3 score_repos.py --input=repos.json --output=scored.json
    python3 score_repos.py --input=repos.json --top=10 --table

参数:
    --input: 输入文件 (fetch_trending.py 的输出)
    --output: 输出文件路径
    --top: 只输出 Top N
    --table: 打印表格
    --detail: 显示详细评分
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from typing import Optional


# 赛道权重 (来自 criteria.md)
DOMAIN_WEIGHTS = {
    "ai": 5,
    "web3": 4,
    "frontend": 4,
    "tools": 4,
    "infra": 3,
    "other": 1,
}

# 正向信号关键词
POSITIVE_SIGNALS = {
    "topics": [
        "hacktoberfest", "good-first-issue", "documentation",
        "actively-maintained", "production-ready"
    ],
    "license": ["MIT", "Apache-2.0", "BSD-3-Clause", "ISC"],
}

# 负向信号关键词
NEGATIVE_SIGNALS = {
    "name_keywords": [
        "awesome-", "list-", "collection", "curated",
        "interview", "cheatsheet", "tutorial"
    ],
    "description_keywords": [
        "airdrop", "free money", "hack tool", "crack",
        "star this", "give me star"
    ],
}

SUMMARY_PATH_DEFAULT = "/Users/sggmico/course/101/post/github-trend/summary.md"
SUMMARY_TABLE_HEADER = "| 日期  | 模型 | 1 | 2 | 3 | 4 | 5 |"
SUMMARY_TABLE_ALIGN = "| :-- | :-- | :-- | :-- | :-- | :-- | :-- |"
SUMMARY_ROW_PATTERN = re.compile(r"^\|\s*(\d{1,2})\s*\|")


def calculate_heat_score(repo: dict) -> float:
    """
    计算热度分 (0-10)
    基于 stars, forks, 增长趋势
    """
    stars = repo.get("stars", 0)
    forks = repo.get("forks", 0)

    # 基础热度 (对数缩放)
    import math
    if stars > 0:
        base_score = min(math.log10(stars) * 2, 8)
    else:
        base_score = 0

    # fork 比率加分
    if forks > 0 and stars > 0:
        fork_ratio = forks / stars
        if 0.05 <= fork_ratio <= 0.3:  # 健康比率
            base_score += 1

    # 活跃度加分
    activity = repo.get("activity_score", 0)
    base_score += activity * 0.1

    return min(base_score, 10)


def calculate_spread_value(repo: dict) -> dict:
    """
    计算传播价值 (1-5 每项)
    返回详细评分和平均分
    """
    scores = {}

    # 1. 痛点强度 - 基于 description 和 topics 判断
    desc = (repo.get("description", "") or "").lower()
    topics = [t.lower() for t in repo.get("topics", [])]

    pain_indicators = ["replace", "alternative", "faster", "simpler", "better", "solve"]
    pain_score = sum(1 for ind in pain_indicators if ind in desc)
    scores["pain_point"] = min(max(pain_score + 2, 1), 5)

    # 2. 颠覆性 - 新技术关键词
    disruptive_keywords = [
        "ai", "llm", "gpt", "agent", "autonomous", "zero-knowledge",
        "revolutionary", "next-gen", "breakthrough"
    ]
    disruptive_count = sum(1 for kw in disruptive_keywords if kw in desc or kw in topics)
    scores["disruption"] = min(max(disruptive_count + 1, 1), 5)

    # 3. 易理解 - description 长度和清晰度
    desc_len = len(repo.get("description", "") or "")
    if 50 <= desc_len <= 200:
        scores["understandable"] = 4
    elif 30 <= desc_len <= 250:
        scores["understandable"] = 3
    else:
        scores["understandable"] = 2

    # 有 topics 加分
    if len(topics) >= 3:
        scores["understandable"] = min(scores["understandable"] + 1, 5)

    # 4. 可试用 - 基于活跃度和 license
    activity = repo.get("activity_score", 0)
    license_type = repo.get("license", "")

    tryable_score = 2
    if license_type in POSITIVE_SIGNALS["license"]:
        tryable_score += 1
    if activity >= 5:
        tryable_score += 1
    if activity >= 8:
        tryable_score += 1
    scores["tryable"] = min(tryable_score, 5)

    # 计算平均分
    avg = sum(scores.values()) / len(scores)
    scores["average"] = round(avg, 2)

    return scores


def apply_signal_adjustments(repo: dict, base_score: float) -> tuple[float, list]:
    """
    应用正向/负向信号调整
    返回调整后的分数和信号列表
    """
    adjustments = []
    adjusted_score = base_score

    name = repo.get("name", "").lower()
    desc = (repo.get("description", "") or "").lower()
    topics = [t.lower() for t in repo.get("topics", [])]
    license_type = repo.get("license", "")

    # 正向信号
    for topic in POSITIVE_SIGNALS["topics"]:
        if topic in topics:
            adjusted_score += 0.3
            adjustments.append(f"+0.3 (topic: {topic})")

    if license_type in POSITIVE_SIGNALS["license"]:
        adjusted_score += 0.5
        adjustments.append(f"+0.5 (license: {license_type})")

    # 负向信号
    for kw in NEGATIVE_SIGNALS["name_keywords"]:
        if kw in name:
            adjusted_score -= 1.0
            adjustments.append(f"-1.0 (name: {kw})")
            break

    for kw in NEGATIVE_SIGNALS["description_keywords"]:
        if kw in desc:
            adjusted_score -= 2.0
            adjustments.append(f"-2.0 (desc: {kw})")
            break

    # stars 暴涨但活跃度低 (疑似刷量)
    stars = repo.get("stars", 0)
    activity = repo.get("activity_score", 0)
    if stars > 5000 and activity < 3:
        adjusted_score -= 1.5
        adjustments.append("-1.5 (high stars but low activity)")

    return max(adjusted_score, 0), adjustments


def calculate_final_score(repo: dict) -> dict:
    """计算最终评分"""
    # 热度分
    heat_score = calculate_heat_score(repo)

    # 赛道权重
    domain = repo.get("domain", "other")
    domain_weight = DOMAIN_WEIGHTS.get(domain, 1)

    # 传播价值
    spread_scores = calculate_spread_value(repo)
    spread_value = spread_scores["average"]

    # 原始综合分
    raw_score = heat_score * (domain_weight / 5) * spread_value

    # 信号调整
    final_score, adjustments = apply_signal_adjustments(repo, raw_score)

    return {
        "heat_score": round(heat_score, 2),
        "domain_weight": domain_weight,
        "spread_value": spread_value,
        "spread_detail": spread_scores,
        "raw_score": round(raw_score, 2),
        "adjustments": adjustments,
        "final_score": round(final_score, 2),
    }


def score_repos(repos: list) -> list:
    """对所有仓库评分并排序"""
    scored = []

    for repo in repos:
        score_detail = calculate_final_score(repo)
        repo["score_detail"] = score_detail
        repo["final_score"] = score_detail["final_score"]
        scored.append(repo)

    # 按最终分排序
    scored.sort(key=lambda x: x["final_score"], reverse=True)

    # 重新编号
    for i, repo in enumerate(scored):
        repo["rank"] = i + 1

    return scored


def print_table(repos: list, show_detail: bool = False):
    """打印表格"""
    print("\n" + "=" * 120)
    if show_detail:
        print(f"{'Rank':<5} {'Repo':<35} {'Stars':<8} {'Domain':<10} "
              f"{'Heat':<6} {'DW':<4} {'Spread':<7} {'Final':<7} {'Adjustments':<20}")
    else:
        print(f"{'Rank':<5} {'Repo':<40} {'Stars':<10} {'Domain':<12} "
              f"{'Final':<8} {'Description':<40}")
    print("=" * 120)

    for repo in repos:
        sd = repo.get("score_detail", {})

        if show_detail:
            adj_str = "; ".join(sd.get("adjustments", []))[:18]
            print(
                f"{repo['rank']:<5} "
                f"{repo['full_name']:<35} "
                f"{repo['stars']:<8} "
                f"{repo['domain']:<10} "
                f"{sd.get('heat_score', 0):<6.1f} "
                f"{sd.get('domain_weight', 1):<4} "
                f"{sd.get('spread_value', 0):<7.2f} "
                f"{repo['final_score']:<7.2f} "
                f"{adj_str:<20}"
            )
        else:
            desc = (repo.get("description", "") or "")[:38]
            print(
                f"{repo['rank']:<5} "
                f"{repo['full_name']:<40} "
                f"{repo['stars']:<10} "
                f"{repo['domain']:<12} "
                f"{repo['final_score']:<8.2f} "
                f"{desc:<40}"
            )

    print("=" * 120 + "\n")


def generate_one_liner(repo: dict) -> str:
    """生成一句话价值定位"""
    desc = repo.get("description", "") or ""
    domain = repo.get("domain", "")
    topics = repo.get("topics", [])

    # 简单截取或生成
    if len(desc) <= 50:
        return desc

    # 提取关键部分
    sentences = desc.split(".")
    if sentences:
        return sentences[0][:50]

    return desc[:50]


def format_output(repos: list, meta: dict) -> dict:
    """格式化输出"""
    for repo in repos:
        repo["one_liner"] = generate_one_liner(repo)

    return {
        "meta": {
            **meta,
            "scored_at": datetime.now().isoformat(),
            "count": len(repos),
        },
        "repos": repos,
    }


def format_summary_cells(repos: list) -> list[str]:
    cells = []
    for repo in repos[:5]:
        name = repo.get("name") or repo.get("full_name") or ""
        url = repo.get("url") or repo.get("html_url") or ""
        if name and url:
            cells.append(f"[{name}]({url})")
        elif name:
            cells.append(name)
        else:
            cells.append("")
    while len(cells) < 5:
        cells.append("")
    return cells


def build_summary_row(day: int, model: str, repos: list) -> str:
    cells = format_summary_cells(repos)
    return f"| {day:<2}  | `{model}` | " + " | ".join(cells) + " |"


def ensure_month_section(lines: list[str], month_title: str) -> int:
    for i, line in enumerate(lines):
        if line.strip() == month_title:
            return i
    lines.append("")
    lines.append(month_title)
    lines.append("")
    return len(lines) - 2


def find_or_create_table(lines: list[str], start_index: int) -> int:
    for i in range(start_index, len(lines)):
        if lines[i].strip().startswith("| 日期"):
            return i
        if lines[i].startswith("## ") and i != start_index:
            break

    insert_at = start_index + 1
    if insert_at < len(lines) and lines[insert_at].strip() != "":
        lines.insert(insert_at, "")
        insert_at += 1
    lines.insert(insert_at, SUMMARY_TABLE_HEADER)
    lines.insert(insert_at + 1, SUMMARY_TABLE_ALIGN)
    return insert_at


def update_summary_table(summary_path: str, model: str, repos: list, today: Optional[str] = None) -> None:
    if today:
        date_obj = datetime.strptime(today, "%Y-%m-%d")
    else:
        date_obj = datetime.now()

    month_title = f"## {date_obj.month}月"
    day = date_obj.day

    if os.path.exists(summary_path):
        with open(summary_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    else:
        lines = [
            "> 汇总规则如下：",
            "> 1. 以月份为二级标题维度",
            "> 2. 每个月份包含按天（使用的模型）为纵轴，以分析结果的仓库为横轴的表格",
            "> 3. 表格日期采用倒序：最新日期排在表格的前面",
            "",
        ]

    month_index = ensure_month_section(lines, month_title)
    table_index = find_or_create_table(lines, month_index)

    insert_at = table_index + 2
    row_text = build_summary_row(day, model, repos)

    for i in range(insert_at, len(lines)):
        line = lines[i]
        if line.startswith("## "):
            lines.insert(i, row_text)
            break
        if not line.startswith("|"):
            continue
        match = SUMMARY_ROW_PATTERN.match(line)
        if not match:
            continue
        existing_day = int(match.group(1))
        if existing_day == day:
            lines.insert(i, row_text)
            break
        if existing_day < day:
            lines.insert(i, row_text)
            break
    else:
        lines.append(row_text)

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip() + "\n")


def main():
    parser = argparse.ArgumentParser(description="Score and rank repos")
    parser.add_argument("--input", required=True, help="Input JSON file")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--top", type=int, default=5, help="Top N repos")
    parser.add_argument("--table", action="store_true", help="Print as table")
    parser.add_argument("--detail", action="store_true", help="Show score details")
    parser.add_argument("--summary", default=SUMMARY_PATH_DEFAULT, help="summary.md path")
    parser.add_argument("--model", help="Model name for summary.md update")
    parser.add_argument("--update-summary", action="store_true", help="Update summary.md")

    args = parser.parse_args()

    # 读取输入
    try:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"File not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        sys.exit(1)

    repos = data.get("repos", [])
    meta = data.get("meta", {})

    if not repos:
        print("No repos found in input", file=sys.stderr)
        sys.exit(1)

    print(f"Scoring {len(repos)} repos...", file=sys.stderr)

    # 评分
    scored = score_repos(repos)

    # 截取 Top N
    top_repos = scored[:args.top]

    # 输出
    if args.table:
        print_table(top_repos, args.detail)

    output = format_output(top_repos, meta)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"Saved to {args.output}", file=sys.stderr)
    elif not args.table:
        print(json.dumps(output, ensure_ascii=False, indent=2))

    if args.update_summary:
        if not args.model:
            print("--model is required when --update-summary is set", file=sys.stderr)
            sys.exit(1)
        update_summary_table(args.summary, args.model, top_repos)


if __name__ == "__main__":
    main()
