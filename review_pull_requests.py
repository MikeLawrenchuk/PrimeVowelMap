"""Utility for summarizing recent merged pull requests.

This script inspects the local Git history for merge commits whose
messages follow the conventional "Merge pull request #<id>" format.
It collects useful metadata – author, date, commit message, and
diffstat information – and renders a concise Markdown report to
aid manual code review.

Run the script directly to generate a ``PR_REVIEW_SUMMARY.md`` file::

    python review_pull_requests.py --limit 5

Use ``--stdout`` to write the summary to standard output instead of
updating the Markdown file.  The script only requires the ``git`` CLI
to be available in the current repository.
"""

from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional


MERGE_LINE = re.compile(r"Merge pull request #(\d+)")
SUMMARY_LINE = re.compile(
    r"(?P<files>\d+) file[s]? changed(?:, (?P<insertions>\d+) insertion[s]?\(\+\))?"
    r"(?:, (?P<deletions>\d+) deletion[s]?\(-\))?"
)


class GitError(RuntimeError):
    """Wrap subprocess errors to provide clearer git context."""


def run_git_command(args: Iterable[str]) -> str:
    """Run a git command and return its standard output."""

    result = subprocess.run(
        ["git", *args],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        raise GitError(result.stderr.strip() or "git command failed")
    return result.stdout


@dataclass
class PullRequestSummary:
    commit: str
    title: str
    pr_number: Optional[int]
    author: str
    date: str
    body: str
    files_changed: int
    insertions: int
    deletions: int
    file_summaries: List[tuple[str, str]]

    @property
    def identifier(self) -> str:
        if self.pr_number is not None:
            return f"PR #{self.pr_number}"
        return self.commit[:7]


def get_merge_commits(limit: int) -> List[tuple[str, str, Optional[int]]]:
    """Return merge commit hashes, their titles, and PR numbers."""

    output = run_git_command(
        [
            "log",
            "--merges",
            f"--max-count={limit}",
            "--pretty=format:%H%x00%s",
        ]
    )
    commits: List[tuple[str, str, Optional[int]]] = []
    for line in output.strip().splitlines():
        if not line:
            continue
        commit, subject = line.split("\x00", 1)
        match = MERGE_LINE.search(subject)
        pr_number = int(match.group(1)) if match else None
        commits.append((commit, subject, pr_number))
    return commits


def extract_commit_details(commit: str) -> tuple[str, str, str]:
    """Return author, date, and commit body for a commit hash."""

    output = run_git_command(
        [
            "log",
            "-1",
            commit,
            "--pretty=format:%an%x00%ad%x00%B",
        ]
    )
    author, date, body = output.split("\x00", 2)
    return author.strip(), date.strip(), body.strip()


def parse_diffstat(commit: str) -> tuple[int, int, int, List[tuple[str, str]]]:
    """Return diffstat aggregates and per-file summaries for a commit."""

    output = run_git_command(["show", "--stat", "--pretty=format:", commit])
    lines = [line.rstrip() for line in output.splitlines() if line.strip()]
    if not lines:
        return 0, 0, 0, []

    summary_match = SUMMARY_LINE.search(lines[-1])
    files_changed = int(summary_match.group("files")) if summary_match else 0
    insertions = (
        int(summary_match.group("insertions")) if summary_match and summary_match.group("insertions") else 0
    )
    deletions = (
        int(summary_match.group("deletions")) if summary_match and summary_match.group("deletions") else 0
    )

    file_summaries: List[tuple[str, str]] = []
    for entry in lines[:-1]:
        if "|" not in entry:
            continue
        filename, stats = entry.split("|", 1)
        file_summaries.append((filename.strip(), stats.strip()))

    return files_changed, insertions, deletions, file_summaries


def build_summary(commit_info: tuple[str, str, Optional[int]]) -> PullRequestSummary:
    commit, subject, pr_number = commit_info
    author, date, body = extract_commit_details(commit)
    files_changed, insertions, deletions, file_summaries = parse_diffstat(commit)
    title = subject
    if "\n" in body:
        body = body.strip()
    return PullRequestSummary(
        commit=commit,
        title=title,
        pr_number=pr_number,
        author=author,
        date=date,
        body=body,
        files_changed=files_changed,
        insertions=insertions,
        deletions=deletions,
        file_summaries=file_summaries,
    )


def render_markdown(summaries: List[PullRequestSummary]) -> str:
    lines = ["# Pull Request Review Summary", ""]
    if not summaries:
        lines.append("No merge commits were found in this repository.")
        return "\n".join(lines)

    lines.append("Generated by `review_pull_requests.py`.\n")

    for summary in summaries:
        lines.append(f"## {summary.identifier}: {summary.title}")
        lines.append("")
        lines.append(f"- **Commit:** `{summary.commit}`")
        lines.append(f"- **Author:** {summary.author}")
        lines.append(f"- **Date:** {summary.date}")
        lines.append(
            f"- **Changes:** {summary.files_changed} file(s), "
            f"{summary.insertions} insertion(s), {summary.deletions} deletion(s)"
        )
        if summary.body:
            lines.append("")
            lines.append("**Commit message body:**")
            lines.append("")
            for body_line in summary.body.splitlines():
                lines.append(f"> {body_line}" if body_line else ">")

        if summary.file_summaries:
            lines.append("")
            lines.append("**Files changed:**")
            lines.append("")
            lines.append("| File | Diffstat |")
            lines.append("| --- | --- |")
            for filename, stats in summary.file_summaries:
                lines.append(f"| {filename} | {stats} |")

        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def write_markdown(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Number of recent merged pull requests to include (default: 5).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("PR_REVIEW_SUMMARY.md"),
        help="Where to write the Markdown summary (default: PR_REVIEW_SUMMARY.md).",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print the summary to stdout instead of writing to disk.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    merge_commits = get_merge_commits(args.limit)
    summaries = [build_summary(info) for info in merge_commits]
    markdown = render_markdown(summaries)

    if args.stdout:
        print(markdown)
    else:
        write_markdown(args.output, markdown)


if __name__ == "__main__":
    main()
