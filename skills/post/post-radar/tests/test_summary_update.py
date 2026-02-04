import os
import sys
import tempfile
import textwrap
import unittest

SCRIPT_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, os.path.abspath(SCRIPT_DIR))

import score_repos  # noqa: E402


class SummaryUpdateTests(unittest.TestCase):
    def test_insert_row_into_month_table_in_reverse_order(self):
        content = textwrap.dedent(
            """
            > 汇总规则如下：
            > 1. 以月份为二级标题维度
            > 2. 每个月份包含按天（使用的模型）为纵轴，以分析结果的仓库为横轴的表格
            > 3. 表格日期采用倒序：最新日期排在表格的前面

            ## 1月

            | 日期  | 模型 | 1 | 2 | 3 | 4 | 5 |
            | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
            | 29  | `gpt-5` | [ocrbase](https://github.com/majcheradam/ocrbase) |  |  |  |  |
            | 28  | `gemini` | [gemini-cli](https://github.com/google-gemini/gemini-cli) |  |  |  |  |
            """
        ).strip()

        repos = [
            {"name": "repo-a", "url": "https://github.com/foo/repo-a"},
            {"name": "repo-b", "url": "https://github.com/foo/repo-b"},
        ]

        with tempfile.TemporaryDirectory() as tmp_dir:
            summary_path = os.path.join(tmp_dir, "summary.md")
            with open(summary_path, "w", encoding="utf-8") as f:
                f.write(content)

            score_repos.update_summary_table(
                summary_path=summary_path,
                model="gpt-5.2",
                repos=repos,
                today="2026-01-30",
            )

            with open(summary_path, "r", encoding="utf-8") as f:
                updated = f.read()

        # 确保 30 号插入在 29 号之前
        self.assertIn("| 30  | `gpt-5.2` | [repo-a](https://github.com/foo/repo-a) | [repo-b](https://github.com/foo/repo-b)", updated)
        self.assertLess(updated.index("| 30  |"), updated.index("| 29  |"))

    def test_insert_duplicate_day_row(self):
        content = textwrap.dedent(
            """
            ## 1月

            | 日期  | 模型 | 1 | 2 | 3 | 4 | 5 |
            | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
            | 30  | `gpt-5` | [old](https://github.com/foo/old) |  |  |  |  |
            """
        ).strip()

        repos = [
            {"name": "repo-new", "url": "https://github.com/foo/repo-new"},
        ]

        with tempfile.TemporaryDirectory() as tmp_dir:
            summary_path = os.path.join(tmp_dir, "summary.md")
            with open(summary_path, "w", encoding="utf-8") as f:
                f.write(content)

            score_repos.update_summary_table(
                summary_path=summary_path,
                model="gpt-5.2",
                repos=repos,
                today="2026-01-30",
            )

            with open(summary_path, "r", encoding="utf-8") as f:
                updated = f.read()

        self.assertIn("| 30  | `gpt-5.2` | [repo-new](https://github.com/foo/repo-new)", updated)
        self.assertIn("| 30  | `gpt-5` | [old](https://github.com/foo/old)", updated)


if __name__ == "__main__":
    unittest.main()
