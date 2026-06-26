"""Portable Markdown-first AI Brain CLI.

This CLI is intentionally stdlib-only so it can be used outside Hermes by
Claude Code, Codex, GitHub Actions, n8n shell steps, or plain terminal users.
"""

from __future__ import annotations

import argparse
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

ARTIFACT_FOLDERS = ["signals", "tasks", "decisions", "bugs", "research", "content-ideas"]
DOMAIN_FILES = ["LOOP.md", "STATE.md", "backlog.md", "timeline.md"]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9ก-๙]+", "-", value.strip().lower()).strip("-")
    return slug[:60] or "item"


def ensure_file(path: Path, content: str) -> None:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def loop_template(domain: str) -> str:
    return f"""# {domain} Loop

## Goal
Keep this domain understandable, safe, and ready for the next L1 triage run.

## Level
L1 — report-only by default.

## Allowed Actions
- Read this domain's state, backlog, timeline, and relevant artifacts.
- Summarize priorities and blockers.
- Create draft signals/tasks under `artifacts/`.
- Update worklog/state only when explicitly running a write command.

## Denied Actions
- No code edits from this loop contract alone.
- No commits, pushes, publishing, service starts, or public tunnels.
- No secrets, credentials, production data, auth, billing, infra, or migrations.

## Human Handoff
Ask Mike before any L2 action, external write, risky file change, or ambiguous decision.

## Verification
L1 reports must cite source files/artifacts read. L2 work requires separate verifier.
"""


def state_template(domain: str) -> str:
    return f"""# {domain} State

Last run: never
Level: L1 report-only

## Current Focus
- None yet.

## Blocked / Needs Mike
- None yet.

## Watch List
- None yet.

## Recent Outcomes
- None yet.
"""


def backlog_template(domain: str) -> str:
    return f"""# {domain} Backlog

## Next Safe Actions
- [ ] Define first concrete L1 triage question.

## Later / L2 Candidates
- None yet.
"""


def timeline_template(domain: str) -> str:
    return f"""# {domain} Timeline

## {utc_now()}
- Domain initialized.
"""


def init_brain(root: Path, domains: Iterable[str]) -> None:
    root.mkdir(parents=True, exist_ok=True)
    ensure_file(root / "README.md", "# AI Brain\n\nPortable Markdown-first shared brain for agent loops.\n")
    ensure_file(root / "inbox.md", "# Inbox\n\nDrop untriaged notes here.\n")
    ensure_file(root / "worklog.md", "# Worklog\n\nAppend-only run history.\n")
    for folder in ARTIFACT_FOLDERS:
        (root / "artifacts" / folder).mkdir(parents=True, exist_ok=True)
        ensure_file(root / "artifacts" / folder / ".gitkeep", "")
    for domain in domains:
        d = root / "domains" / domain
        d.mkdir(parents=True, exist_ok=True)
        ensure_file(d / "LOOP.md", loop_template(domain))
        ensure_file(d / "STATE.md", state_template(domain))
        ensure_file(d / "backlog.md", backlog_template(domain))
        ensure_file(d / "timeline.md", timeline_template(domain))


def append_worklog(root: Path, domain: str, message: str, agent: str = "manual") -> None:
    ensure_file(root / "worklog.md", "# Worklog\n\nAppend-only run history.\n")
    entry = f"""
## {utc_now()}
Domain: {domain}
Agent: {agent}
Action: log
Result: {message}
"""
    with (root / "worklog.md").open("a", encoding="utf-8") as fh:
        fh.write(entry)


def artifact_path(root: Path, kind: str, title: str) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return root / "artifacts" / kind / f"{stamp}-{slugify(title)}.md"


def write_artifact(root: Path, kind: str, domain: str, title: str, body: str, priority: str, source: str = "manual") -> Path:
    folder = root / "artifacts" / kind
    folder.mkdir(parents=True, exist_ok=True)
    now = utc_now()
    singular = kind[:-1] if kind.endswith("s") else kind
    status = "new" if singular == "signal" else "open"
    content = f"""---
id: {singular}-{now.replace(':', '').replace('-', '')}-{slugify(title)}
type: {singular}
domain: {domain}
priority: {priority}
status: {status}
source: {source}
created_at: {now}
---

# {title}

## Summary
{body}

## Suggested next action
- Review in next L1 triage.
"""
    path = artifact_path(root, kind, title)
    path.write_text(content, encoding="utf-8")
    return path


def list_domains(root: Path) -> list[str]:
    domains_dir = root / "domains"
    if not domains_dir.exists():
        return []
    return sorted(p.name for p in domains_dir.iterdir() if p.is_dir())


def artifact_count(root: Path, kind: str) -> int:
    folder = root / "artifacts" / kind
    if not folder.exists():
        return 0
    return len([p for p in folder.glob("*.md") if p.name != ".gitkeep"])


def read_title(path: Path) -> str:
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def artifact_status(text: str) -> str | None:
    for line in text.splitlines():
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip().lower()
    return None


def artifacts_for_domain(root: Path, domain: str, kind: str) -> list[Path]:
    folder = root / "artifacts" / kind
    if not folder.exists():
        return []
    matches = []
    needle = f"domain: {domain}"
    for path in sorted(folder.glob("*.md")):
        if path.name == ".gitkeep":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if needle not in text:
            continue
        if kind == "tasks" and artifact_status(text) not in {"open", "new", "pending", "in_progress", None}:
            continue
        matches.append(path)
    return matches


def read_text_if_exists(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def extract_section(markdown: str, heading: str) -> list[str]:
    """Return non-empty content lines under a level-2 markdown heading."""
    lines = markdown.splitlines()
    capture = False
    captured: list[str] = []
    target = f"## {heading}".strip().lower()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            if capture:
                break
            capture = stripped.lower() == target
            continue
        if capture and stripped:
            captured.append(stripped)
    return captured


def print_lines(lines: list[str], limit: int = 8) -> None:
    visible = [line for line in lines if line not in {"- None yet.", "- None", "None yet."}]
    if not visible:
        print("- None")
        return
    for line in visible[:limit]:
        print(line)
    if len(visible) > limit:
        print(f"- ... {len(visible) - limit} more")


def print_artifact_titles(root: Path, paths: list[Path], limit: int = 10) -> None:
    if not paths:
        print("- None")
        return
    for path in paths[:limit]:
        print(f"- {read_title(path)} ({path.relative_to(root)})")
    if len(paths) > limit:
        print(f"- ... {len(paths) - limit} more")


def print_domain_triage(root: Path, domain: str) -> None:
    domain_dir = root / "domains" / domain
    loop_path = domain_dir / "LOOP.md"
    state_path = domain_dir / "STATE.md"
    backlog_path = domain_dir / "backlog.md"
    timeline_path = domain_dir / "timeline.md"

    loop_text = read_text_if_exists(loop_path)
    state_text = read_text_if_exists(state_path)
    backlog_text = read_text_if_exists(backlog_path)
    timeline_text = read_text_if_exists(timeline_path)
    tasks = artifacts_for_domain(root, domain, "tasks")
    signals = artifacts_for_domain(root, domain, "signals")

    print(f"# L1 Triage Report — {domain}")
    print(f"Root: {root}")

    print("\n## Goal")
    print_lines(extract_section(loop_text, "Goal"), limit=4)

    print("\n## Current Focus")
    print_lines(extract_section(state_text, "Current Focus"), limit=8)

    print("\n## Blocked / Needs Mike")
    print_lines(extract_section(state_text, "Blocked / Needs Mike"), limit=8)

    print("\n## Watch List / Risks")
    watch = extract_section(state_text, "Watch List")
    denied = extract_section(loop_text, "Denied Actions")
    print_lines(watch or denied, limit=8)

    print("\n## Next Safe Actions")
    next_actions = extract_section(backlog_text, "Next Safe L1 Actions") or extract_section(backlog_text, "Next Safe Actions")
    print_lines(next_actions, limit=10)

    print("\n## Open Tasks")
    print_artifact_titles(root, tasks)

    print("\n## Signals")
    print_artifact_titles(root, signals)

    print("\n## Denied Actions")
    print_lines(denied, limit=10)

    print("\n## Recent Timeline")
    timeline_entries = [line for line in timeline_text.splitlines() if line.startswith("## ") or line.startswith("- ")]
    print_lines(timeline_entries[-8:], limit=8)

    print("\n## Sources Read")
    for path in [loop_path, state_path, backlog_path, timeline_path]:
        if path.exists():
            print(f"- {path.relative_to(root)}")
    for path in tasks[:5] + signals[:5]:
        print(f"- {path.relative_to(root)}")

    print("\n## Safety")
    print("- No auto-actions taken. L1 report-only.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="brain", description="Portable Markdown-first AI Brain stack")
    parser.add_argument("--root", default=".", help="AI Brain root folder")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Create brain skeleton")
    p_init.add_argument("--domains", nargs="*", default=[])

    p_status = sub.add_parser("status", help="Show domains and artifact counts")

    p_log = sub.add_parser("log", help="Append to worklog")
    p_log.add_argument("--domain", required=True)
    p_log.add_argument("--message", required=True)
    p_log.add_argument("--agent", default="manual")

    p_signal = sub.add_parser("signal", help="Manage signal artifacts")
    signal_sub = p_signal.add_subparsers(dest="signal_command", required=True)
    p_signal_add = signal_sub.add_parser("add", help="Create signal")
    p_signal_add.add_argument("--domain", required=True)
    p_signal_add.add_argument("--title", required=True)
    p_signal_add.add_argument("--body", required=True)
    p_signal_add.add_argument("--priority", default="medium")
    p_signal_add.add_argument("--source", default="manual")

    p_task = sub.add_parser("task", help="Manage task artifacts")
    task_sub = p_task.add_subparsers(dest="task_command", required=True)
    p_task_add = task_sub.add_parser("add", help="Create task")
    p_task_add.add_argument("--domain", required=True)
    p_task_add.add_argument("--title", required=True)
    p_task_add.add_argument("--body", required=True)
    p_task_add.add_argument("--priority", default="medium")
    p_task_add.add_argument("--source", default="manual")

    p_triage = sub.add_parser("triage", help="Print L1 report for a domain")
    p_triage.add_argument("--domain", required=True)
    return parser


def main(argv=None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = Path(args.root).expanduser().resolve()

    if args.command == "init":
        init_brain(root, args.domains)
        domains = ", ".join(args.domains) if args.domains else "none"
        print(f"Initialized AI Brain at {root}")
        print(f"Domains: {domains}")
        return

    if args.command == "log":
        append_worklog(root, args.domain, args.message, args.agent)
        print(f"Logged work for {args.domain}")
        return

    if args.command == "signal" and args.signal_command == "add":
        path = write_artifact(root, "signals", args.domain, args.title, args.body, args.priority, args.source)
        print(f"Created signal: {path}")
        return

    if args.command == "task" and args.task_command == "add":
        path = write_artifact(root, "tasks", args.domain, args.title, args.body, args.priority, args.source)
        print(f"Created task: {path}")
        return

    if args.command == "status":
        domains = list_domains(root)
        print(f"AI Brain: {root}")
        print("Domains: " + (", ".join(domains) if domains else "none"))
        for kind in ["signals", "tasks", "decisions", "bugs", "research", "content-ideas"]:
            print(f"{kind}: {artifact_count(root, kind)}")
        return

    if args.command == "triage":
        print_domain_triage(root, args.domain)
        return

    parser.error("Unhandled command")


if __name__ == "__main__":
    main()
