import os
import sys
import tempfile
import textwrap
import unittest

SCRIPT_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, os.path.abspath(SCRIPT_DIR))

import fetch_trending  # noqa: E402


class SummaryFilterTests(unittest.TestCase):
    def test_load_summary_repo_set(self):
        content = textwrap.dedent(
            """
            | 日期 | 1 |
            | --- | --- |
            | **Jan 01, 2026** | [Demo](https://github.com/OwnerOne/RepoOne) |
            | **Jan 02, 2026** | [Demo2](https://github.com/ownerTwo/repo-two) |
            """
        ).strip()
        with tempfile.TemporaryDirectory() as tmp_dir:
            summary_path = os.path.join(tmp_dir, "summary.md")
            with open(summary_path, "w", encoding="utf-8") as f:
                f.write(content)

            result = fetch_trending.load_summary_repo_set(summary_path)

        self.assertIn("ownerone/repoone", result)
        self.assertIn("ownertwo/repo-two", result)

    def test_filter_repos_by_summary(self):
        repos = [
            {"full_name": "OwnerOne/RepoOne", "html_url": "https://github.com/OwnerOne/RepoOne"},
            {"full_name": "New/Repo", "html_url": "https://github.com/New/Repo"},
        ]
        excluded = {"ownerone/repoone"}

        filtered = fetch_trending.filter_repos_by_summary(repos, excluded)

        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["full_name"], "New/Repo")


if __name__ == "__main__":
    unittest.main()
