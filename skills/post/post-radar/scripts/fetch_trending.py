#!/usr/bin/env python3
"""
GitHub Trending 数据获取脚本

用法:
    python3 fetch_trending.py --window=past_week --domain=ai
    python3 fetch_trending.py --window=past_month --domain=all --output=repos.json

参数:
    --window: past_24_hours | past_week | past_month | past_3_months
    --domain: ai | web3 | frontend | tools | infra | all
    --output: 输出文件路径 (默认输出到 stdout)
    --limit: 返回数量 (默认 30)
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta
from typing import Optional


# 时间窗口配置
WINDOW_DAYS = {
    "past_24_hours": 1,
    "past_week": 7,
    "past_month": 30,
    "past_3_months": 90,
}

# 赛道关键词配置
DOMAIN_KEYWORDS = {
    "ai": [
        "llm", "gpt", "agent", "langchain", "openai", "anthropic",
        "transformer", "neural", "machine-learning", "deep-learning",
        "chatbot", "embedding", "rag", "fine-tuning", "inference"
    ],
    "web3": [
        "blockchain", "ethereum", "solidity", "web3", "defi", "nft",
        "smart-contract", "crypto", "solana", "zk", "zero-knowledge"
    ],
    "frontend": [
        "react", "vue", "svelte", "nextjs", "nuxt", "tailwind",
        "typescript", "javascript", "css", "ui-components", "design-system"
    ],
    "tools": [
        "cli", "developer-tools", "productivity", "automation",
        "devtools", "utility", "terminal", "shell", "dotfiles"
    ],
    "infra": [
        "kubernetes", "docker", "terraform", "devops", "ci-cd",
        "monitoring", "observability", "cloud", "serverless"
    ],
}

# 赛道对应的编程语言倾向
DOMAIN_LANGUAGES = {
    "ai": ["Python", "Jupyter Notebook"],
    "web3": ["Solidity", "Rust", "TypeScript"],
    "frontend": ["TypeScript", "JavaScript"],
    "tools": ["Rust", "Go", "Python"],
    "infra": ["Go", "Python", "Shell"],
}

SUMMARY_PATH_DEFAULT = "/Users/sggmico/course/101/post/github-trend/summary.md"
SUMMARY_REPO_PATTERN = re.compile(
    r"https?://github\.com/([^/\s]+)/([^\)\s]+)",
    re.IGNORECASE,
)


def get_date_threshold(window: str) -> str:
    """计算时间阈值"""
    days = WINDOW_DAYS.get(window, 7)
    threshold = datetime.now() - timedelta(days=days)
    return threshold.strftime("%Y-%m-%d")


def build_search_query(domain: str, date_threshold: str, min_stars: int = 100) -> str:
    """构建 GitHub 搜索查询"""
    base_query = f"stars:>{min_stars} pushed:>{date_threshold}"

    if domain == "all":
        # 全部赛道，使用通用过滤
        return base_query

    # 添加赛道关键词 - 使用 in:name,description,readme 方式
    keywords = DOMAIN_KEYWORDS.get(domain, [])
    if keywords:
        # 简化查询，避免复杂语法
        keyword_query = " ".join(keywords[:3])
        return f"{base_query} {keyword_query}"

    return base_query


def load_summary_repo_set(summary_path: str) -> set[str]:
    """从 summary.md 提取历史仓库 full_name 集合"""
    try:
        with open(summary_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"summary.md not found: {summary_path}", file=sys.stderr)
        return set()
    except OSError as e:
        print(f"summary.md read error: {e}", file=sys.stderr)
        return set()

    repos = set()
    for match in SUMMARY_REPO_PATTERN.finditer(content):
        owner = match.group(1).strip().lower()
        repo = match.group(2).strip().lower().rstrip("/")
        if repo.endswith(".git"):
            repo = repo[:-4]
        if owner and repo:
            repos.add(f"{owner}/{repo}")

    return repos


def filter_repos_by_summary(repos: list, excluded: set[str]) -> list:
    """过滤 summary.md 已出现过的仓库"""
    if not excluded:
        return repos

    filtered = []
    for repo in repos:
        full_name = (repo.get("full_name") or "").lower()
        html_url = repo.get("html_url") or ""

        if full_name in excluded:
            continue

        url_match = SUMMARY_REPO_PATTERN.search(html_url)
        if url_match:
            owner = url_match.group(1).strip().lower()
            name = url_match.group(2).strip().lower().rstrip("/")
            if name.endswith(".git"):
                name = name[:-4]
            if f"{owner}/{name}" in excluded:
                continue

        filtered.append(repo)

    return filtered


def fetch_via_gh_cli(query: str, limit: int = 30) -> Optional[list]:
    """使用 gh CLI 获取数据"""
    try:
        cmd = [
            "gh", "api", "search/repositories",
            "--method", "GET",
            "-f", f"q={query}",
            "-f", "sort=stars",
            "-f", "order=desc",
            "-f", f"per_page={limit}",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            print(f"gh CLI error: {result.stderr}", file=sys.stderr)
            return None

        data = json.loads(result.stdout)
        return data.get("items", [])

    except subprocess.TimeoutExpired:
        print("gh CLI timeout", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        return None
    except FileNotFoundError:
        print("gh CLI not found, please install GitHub CLI", file=sys.stderr)
        return None


def process_repos(repos: list, domain: str) -> list:
    """处理和丰富仓库数据"""
    processed = []

    for repo in repos:
        # 基础信息
        item = {
            "rank": len(processed) + 1,
            "full_name": repo.get("full_name", ""),
            "name": repo.get("name", ""),
            "owner": repo.get("owner", {}).get("login", ""),
            "url": repo.get("html_url", ""),
            "description": repo.get("description", "") or "",
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "open_issues": repo.get("open_issues_count", 0),
            "language": repo.get("language", ""),
            "license": repo.get("license", {}).get("spdx_id", "") if repo.get("license") else "",
            "topics": repo.get("topics", []),
            "created_at": repo.get("created_at", ""),
            "updated_at": repo.get("updated_at", ""),
            "pushed_at": repo.get("pushed_at", ""),
        }

        # 推断赛道
        item["domain"] = infer_domain(item, domain)

        # 计算活跃度指标
        item["activity_score"] = calculate_activity_score(item)

        processed.append(item)

    return processed


def infer_domain(repo: dict, default_domain: str) -> str:
    """推断仓库所属赛道"""
    if default_domain != "all":
        return default_domain

    # 基于 topics 和 description 推断
    topics = set(t.lower() for t in repo.get("topics", []))
    desc = (repo.get("description", "") or "").lower()

    for domain, keywords in DOMAIN_KEYWORDS.items():
        matches = sum(1 for kw in keywords if kw in topics or kw in desc)
        if matches >= 2:
            return domain

    # 基于语言推断
    lang = repo.get("language", "")
    for domain, langs in DOMAIN_LANGUAGES.items():
        if lang in langs:
            return domain

    return "other"


def calculate_activity_score(repo: dict) -> float:
    """计算活跃度评分 (0-10)"""
    score = 0.0

    # 有 license 加分
    if repo.get("license"):
        score += 1.5

    # topics 数量
    topics_count = len(repo.get("topics", []))
    score += min(topics_count * 0.3, 2.0)

    # 最近更新
    pushed_at = repo.get("pushed_at", "")
    if pushed_at:
        try:
            pushed_date = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
            days_ago = (datetime.now(pushed_date.tzinfo) - pushed_date).days
            if days_ago <= 1:
                score += 3.0
            elif days_ago <= 7:
                score += 2.0
            elif days_ago <= 30:
                score += 1.0
        except (ValueError, TypeError):
            pass

    # star/fork 比率
    stars = repo.get("stars", 0)
    forks = repo.get("forks", 0)
    if forks > 0:
        ratio = stars / forks
        if 5 <= ratio <= 50:  # 健康比率
            score += 1.5

    # issues 数量 (适中为佳)
    issues = repo.get("open_issues", 0)
    if 5 <= issues <= 100:
        score += 1.0

    return min(score, 10.0)


def format_output(repos: list, window: str, domain: str) -> dict:
    """格式化输出"""
    return {
        "meta": {
            "generated_at": datetime.now().isoformat(),
            "window": window,
            "domain": domain,
            "count": len(repos),
        },
        "repos": repos,
    }


def print_table(repos: list):
    """打印表格格式输出"""
    print("\n" + "=" * 100)
    print(f"{'Rank':<5} {'Repo':<40} {'Stars':<10} {'Domain':<12} {'Activity':<10} {'Description':<30}")
    print("=" * 100)

    for repo in repos[:10]:
        desc = repo.get("description", "")[:28]
        print(
            f"{repo['rank']:<5} "
            f"{repo['full_name']:<40} "
            f"{repo['stars']:<10} "
            f"{repo['domain']:<12} "
            f"{repo['activity_score']:<10.1f} "
            f"{desc:<30}"
        )

    print("=" * 100 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Fetch GitHub trending repos")
    parser.add_argument("--window", default="past_week",
                        choices=list(WINDOW_DAYS.keys()),
                        help="Time window")
    parser.add_argument("--domain", default="all",
                        choices=list(DOMAIN_KEYWORDS.keys()) + ["all"],
                        help="Tech domain")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--limit", type=int, default=50, help="Number of repos")
    parser.add_argument("--min-stars", type=int, default=100, help="Minimum stars")
    parser.add_argument("--table", action="store_true", help="Print as table")
    parser.add_argument("--summary", default=SUMMARY_PATH_DEFAULT,
                        help="summary.md path for duplicate filtering")

    args = parser.parse_args()

    # 构建查询
    date_threshold = get_date_threshold(args.window)
    query = build_search_query(args.domain, date_threshold, args.min_stars)

    print(f"Fetching: window={args.window}, domain={args.domain}", file=sys.stderr)
    print(f"Query: {query}", file=sys.stderr)

    # 获取数据
    repos = fetch_via_gh_cli(query, args.limit)

    if repos is None:
        print("Failed to fetch repos", file=sys.stderr)
        sys.exit(1)

    # 排除 summary.md 中的历史仓库
    excluded = load_summary_repo_set(args.summary)
    filtered = filter_repos_by_summary(repos, excluded)
    if excluded:
        removed = len(repos) - len(filtered)
        print(f"Filtered {removed} repos from summary.md", file=sys.stderr)

    # 处理数据
    processed = process_repos(filtered, args.domain)

    # 按活跃度排序
    processed.sort(key=lambda x: (x["activity_score"], x["stars"]), reverse=True)

    # 重新编号
    for i, repo in enumerate(processed):
        repo["rank"] = i + 1

    # 输出
    output = format_output(processed, args.window, args.domain)

    if args.table:
        print_table(processed)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"Saved to {args.output}", file=sys.stderr)
    else:
        print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
