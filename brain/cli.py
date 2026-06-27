"""Portable Markdown-first AI Brain CLI.

This CLI is intentionally stdlib-only so it can be used outside Hermes by
Claude Code, Codex, GitHub Actions, n8n shell steps, or plain terminal users.
"""

from __future__ import annotations

import argparse
import json
import re
import shlex
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

ARTIFACT_FOLDERS = ["signals", "tasks", "decisions", "bugs", "research", "content-ideas", "approval-packs"]
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


def verify_template(domain: str, project_path: str = "") -> str:
    scope = project_path or "TBD"
    return f"""# {domain} Verification Profile

Status: draft until Mike approves implementation scope.
Last updated: {utc_now()}

## Purpose
Define safe verification for future work in this domain.

## Scope

```text
{scope}
```

## Safe Default Verification

Start report-only. Before any implementation, define exact commands for this domain.

```bash
brain triage --domain {domain}
brain risk-scan --domain {domain} --project {scope if project_path else '<project-path>'}
```

## Required Gates
- Mike approval before implementation.
- Separate verifier before commit/push/deploy.
- No service starts, deploys, tunnels, DB/migrations, secrets, auth, billing, or external writes without explicit approval.

## Hard Stops
- Stop if scope is ambiguous.
- Stop if changes touch a product repo that is not the active approved scope.
- Stop if secrets or production data may be exposed.
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


def active_template() -> str:
    return """# ACTIVE

Updated: {now}

Default view for “ทำต่อ”. Only these domains are active operating brain by default.

## Rule

- Use this file first when Mike says “ทำต่อ” without naming a project.
- Read the domain `LOOP.md` and `STATE.md` before acting.
- Stay L1/report-only unless Mike explicitly requests implementation.

## Active Domains

| Domain | Path / Scope | Status | Default next safe action |
|---|---|---|---|

## Explicitly Not Active by Default

- Project inventory is reference, not the default working queue.
""".format(now=utc_now())


def active_row(domain: str, project_path: str, status: str, next_action: str) -> str:
    return f"| `{domain}` | {project_path or 'TBD'} | {status} | {next_action} |"


def add_active_domain(root: Path, domain: str, project_path: str, status: str, next_action: str) -> None:
    active_path = root / "ACTIVE.md"
    ensure_file(active_path, active_template())
    text = active_path.read_text(encoding="utf-8")
    if f"`{domain}`" in text:
        return
    row = active_row(domain, project_path, status, next_action)
    marker = "## Explicitly Not Active by Default"
    if marker in text:
        text = text.replace(marker, f"{row}\n\n{marker}", 1)
    else:
        text = text.rstrip() + "\n" + row + "\n"
    active_path.write_text(text, encoding="utf-8")


def init_domain(root: Path, domain: str, project_path: str = "", status: str = "L1-ready", next_action: str = "Run L1 triage.", active: bool = False) -> None:
    init_brain(root, [])
    domain_dir = root / "domains" / domain
    domain_dir.mkdir(parents=True, exist_ok=True)
    ensure_file(domain_dir / "LOOP.md", loop_template(domain))
    ensure_file(domain_dir / "STATE.md", state_template(domain))
    ensure_file(domain_dir / "backlog.md", backlog_template(domain))
    ensure_file(domain_dir / "timeline.md", timeline_template(domain))
    ensure_file(domain_dir / "verify.md", verify_template(domain, project_path))
    if active:
        add_active_domain(root, domain, project_path, status, next_action)


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


def status_data(root: Path) -> dict:
    return {
        "root": str(root),
        "domains": list_domains(root),
        "artifacts": {kind: artifact_count(root, kind) for kind in ARTIFACT_FOLDERS},
    }


def clean_table_cell(value: str) -> str:
    return value.strip().replace("`", "").strip()


def active_projects_data(root: Path) -> dict:
    active_path = root / "ACTIVE.md"
    projects: list[dict] = []
    if not active_path.exists():
        return {"root": str(root), "source": "ACTIVE.md", "count": 0, "projects": projects}
    in_table = False
    for line in active_path.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if stripped.startswith("| Domain |"):
            in_table = True
            continue
        if not in_table:
            continue
        if not stripped.startswith("|"):
            if projects:
                break
            continue
        if set(stripped.replace("|", "").replace("-", "").replace(" ", "")) == set():
            continue
        cells = [clean_table_cell(cell) for cell in stripped.strip("|").split("|")]
        if len(cells) < 4 or cells[0].lower() in {"domain", "---"} or cells[0].startswith("---"):
            continue
        projects.append({
            "domain": cells[0],
            "path_scope": cells[1],
            "status": cells[2],
            "next_safe_action": cells[3],
        })
    return {"root": str(root), "source": "ACTIVE.md", "count": len(projects), "projects": projects}


def print_projects(root: Path) -> None:
    data = active_projects_data(root)
    print("# Active Projects")
    print(f"Root: {root}")
    if not data["projects"]:
        print("- None")
        return
    for item in data["projects"]:
        print(f"- {item['domain']} — {item['path_scope']} — {item['status']} — {item['next_safe_action']}")


def first_path_from_scope(path_scope: str) -> str:
    return path_scope.split(" + ", 1)[0].strip()


def resolve_active_loop_target(root: Path, domain: str = "", project: str = "") -> tuple[str, Path]:
    projects = active_projects_data(root)["projects"]
    selected = None
    if domain:
        selected = next((item for item in projects if item["domain"] == domain), None)
    elif projects:
        selected = projects[0]
    resolved_domain = domain or (selected["domain"] if selected else "")
    resolved_project = project or (first_path_from_scope(selected["path_scope"]) if selected else "")
    if not resolved_domain:
        raise SystemExit("No active domain found. Run: brain init-domain --domain <name> --path <path> --active")
    if not resolved_project:
        raise SystemExit("No project path found. Pass --project <path> or update ACTIVE.md.")
    return resolved_domain, Path(resolved_project).expanduser().resolve()


def is_filesystem_path(value: str) -> bool:
    return value.startswith("/") or value.startswith("~/")


def audit_data(root: Path) -> dict:
    projects_data = active_projects_data(root)
    findings: list[dict] = []
    active_exists = (root / "ACTIVE.md").exists()
    if active_exists:
        findings.append({"level": "OK", "domain": "_brain", "message": "ACTIVE.md exists"})
    else:
        findings.append({"level": "ERROR", "domain": "_brain", "message": "ACTIVE.md missing"})

    missing_domain_files = 0
    missing_verify_profiles = 0
    missing_project_paths = 0
    for project in projects_data["projects"]:
        domain = project["domain"]
        domain_dir = root / "domains" / domain
        for filename in DOMAIN_FILES:
            if not (domain_dir / filename).exists():
                missing_domain_files += 1
                findings.append({"level": "WARN", "domain": domain, "message": f"{domain} missing {filename}"})
        if not (domain_dir / "verify.md").exists():
            missing_verify_profiles += 1
            findings.append({"level": "WARN", "domain": domain, "message": f"{domain} missing verify.md"})
        path_scope = project["path_scope"]
        if is_filesystem_path(path_scope):
            first_path = path_scope.split(" + ", 1)[0]
            project_path = Path(first_path).expanduser()
            if not project_path.exists():
                missing_project_paths += 1
                findings.append({"level": "WARN", "domain": domain, "message": f"{domain} project path missing: {first_path}"})
        if domain_dir.exists() and all((domain_dir / filename).exists() for filename in DOMAIN_FILES):
            findings.append({"level": "OK", "domain": domain, "message": f"{domain} has required domain files"})

    summary = {
        "active_projects": projects_data["count"],
        "missing_domain_files": missing_domain_files,
        "missing_verify_profiles": missing_verify_profiles,
        "missing_project_paths": missing_project_paths,
        "approval_packs": artifact_count(root, "approval-packs"),
    }
    active_focus = projects_data["projects"][0]["domain"] if projects_data["projects"] else ""
    return {
        "root": str(root),
        "active_focus": active_focus,
        "summary": summary,
        "findings": findings,
    }


def print_audit(root: Path) -> None:
    data = audit_data(root)
    summary = data["summary"]
    print("# Brain Audit")
    print(f"Root: {root}")
    print("\n## Summary")
    print(f"Active projects: {summary['active_projects']}")
    print(f"Active focus: {data['active_focus'] or 'none'}")
    print(f"Missing domain files: {summary['missing_domain_files']}")
    print(f"Missing verify profiles: {summary['missing_verify_profiles']}")
    print(f"Missing project paths: {summary['missing_project_paths']}")
    print(f"Approval packs: {summary['approval_packs']}")
    print("\n## Findings")
    for finding in data["findings"]:
        print(f"- {finding['level']}: {finding['message']}")


def print_json(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def write_run_log(root: Path, domain: str, summary: str, status: str = "success", cost: str = "0", tokens: str = "0") -> Path:
    path = root / "loop-run-log.md"
    ensure_file(path, "# Loop Run Log\n\n")
    cost_value = float(cost or 0)
    token_value = int(tokens or 0)
    with path.open("a", encoding="utf-8") as f:
        f.write(f"## {utc_now()}\n")
        f.write(f"- domain: {domain}\n")
        f.write(f"- status: {status}\n")
        f.write(f"- cost_usd: {cost_value:.2f}\n")
        f.write(f"- tokens: {token_value}\n")
        f.write(f"- summary: {summary}\n\n")
    return path


def run_log_summary_data(root: Path) -> dict:
    path = root / "loop-run-log.md"
    if not path.exists():
        return {"root": str(root), "runs": 0, "total_cost_usd": 0.0, "total_tokens": 0}
    runs = 0
    total_cost = 0.0
    total_tokens = 0
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            runs += 1
        elif stripped.startswith("- cost_usd:"):
            try:
                total_cost += float(stripped.split(":", 1)[1].strip())
            except ValueError:
                pass
        elif stripped.startswith("- tokens:"):
            try:
                total_tokens += int(float(stripped.split(":", 1)[1].strip()))
            except ValueError:
                pass
    return {"root": str(root), "runs": runs, "total_cost_usd": round(total_cost, 2), "total_tokens": total_tokens}


def print_run_log_summary(root: Path) -> None:
    data = run_log_summary_data(root)
    print("# Loop Run Log Summary")
    print(f"Root: {root}")
    print(f"Runs: {data['runs']}")
    print(f"Total cost USD: {data['total_cost_usd']:.2f}")
    print(f"Total tokens: {data['total_tokens']}")


def set_budget(root: Path, monthly_usd: str, notes: str = "") -> Path:
    path = root / "loop-budget.md"
    monthly = float(monthly_usd)
    content = f"""# Loop Budget

monthly_usd: {monthly:.2f}
notes: {notes}
updated_at: {utc_now()}
"""
    path.write_text(content, encoding="utf-8")
    return path


def read_budget(root: Path) -> dict:
    path = root / "loop-budget.md"
    monthly = 0.0
    notes = ""
    if path.exists():
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("monthly_usd:"):
                try:
                    monthly = float(line.split(":", 1)[1].strip())
                except ValueError:
                    monthly = 0.0
            elif line.startswith("notes:"):
                notes = line.split(":", 1)[1].strip()
    spent = run_log_summary_data(root)["total_cost_usd"]
    remaining = round(monthly - spent, 2)
    return {
        "root": str(root),
        "monthly_budget_usd": round(monthly, 2),
        "spent_usd": round(spent, 2),
        "remaining_usd": remaining,
        "notes": notes,
    }


def print_budget_status(root: Path) -> None:
    data = read_budget(root)
    print("# Loop Budget Status")
    print(f"Root: {root}")
    print(f"Monthly budget USD: {data['monthly_budget_usd']:.2f}")
    print(f"Spent USD: {data['spent_usd']:.2f}")
    print(f"Remaining USD: {data['remaining_usd']:.2f}")
    if data["notes"]:
        print(f"Notes: {data['notes']}")


def audit_status(data: dict) -> str:
    summary = data["summary"]
    if summary["active_projects"] <= 0:
        return "blocked"
    if summary["missing_domain_files"] or summary["missing_verify_profiles"] or summary["missing_project_paths"]:
        return "warn"
    return "ok"


def loop_run_once_data(root: Path, domain: str, project: Path, diff_text: str = "", write_log: bool = True) -> dict:
    audit = audit_data(root)
    triage = domain_triage_data(root, domain)
    risk = risk_scan_data(root, domain, project, diff_text)
    status = "blocked" if risk["risk_level"] == "high" else audit_status(audit)
    if risk["risk_level"] == "high":
        next_action = "stop and request approval"
    elif status == "warn":
        next_action = "fix audit warnings before implementation"
    else:
        next_action = "human/agent may choose the next safe action from triage"
    summary = f"loop run once: audit={audit_status(audit)} risk={risk['risk_level']} next={next_action}"
    run_log_path = ""
    if write_log:
        run_log_path = str(write_run_log(root, domain, summary, status=status))
    return {
        "root": str(root),
        "domain": domain,
        "project": str(project),
        "mode": "once",
        "audit_status": audit_status(audit),
        "status": status,
        "risk": risk,
        "triage": {
            "current_focus": triage.get("current_focus", []),
            "blocked_needs_mike": triage.get("blocked_needs_mike", []),
            "next_safe_actions": triage.get("next_safe_actions", []),
            "denied_actions": triage.get("denied_actions", []),
        },
        "next": next_action,
        "run_log": run_log_path,
        "safety": [
            "L1 loop run only.",
            "No project files modified.",
            "No commit, push, deploy, service start, tunnel, secrets, DB, or external write.",
        ],
    }


def print_loop_run_once(data: dict) -> None:
    print(f"# Loop Run — {data['domain']}")
    print(f"Root: {data['root']}")
    print(f"Project: {data['project']}")
    print("Mode: once")
    print(f"Status: {data['status']}")
    print(f"Audit: {data['audit_status']}")
    print(f"Risk Level: {data['risk']['risk_level']}")
    print(f"Next: {data['next']}")
    print("\n## Blockers / Needs Mike")
    print_lines(data["triage"]["blocked_needs_mike"], limit=10)
    print("\n## Next Safe Actions")
    print_lines(data["triage"]["next_safe_actions"], limit=10)
    print("\n## Safety")
    print_lines(data["safety"], limit=10)
    if data["run_log"]:
        print(f"\nRun log: {data['run_log']}")


def agent_l1_prompt(root: Path) -> str:
    return (
        "Use AI Brain Stack as the operating layer. "
        f"Run: brain --root {shlex.quote(str(root))} next. "
        "Stay L1 report-only. Do not edit files, commit, push, deploy, start services, or touch secrets. "
        "Return focus, blockers, denied actions, risk level, next safe action, and command evidence."
    )


def print_agent_command(root: Path, agent: str) -> None:
    prompt = agent_l1_prompt(root)
    if agent == "codex":
        print(f"codex exec {shlex.quote(prompt)}")
    elif agent == "claude":
        print(f"claude -p {shlex.quote(prompt)}")
    else:
        raise SystemExit(f"Unsupported agent: {agent}")


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


def project_git_diff(project: Path) -> str:
    import subprocess

    try:
        result = subprocess.run(
            ["git", "diff", "--", "."],
            cwd=project,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
            check=False,
        )
    except Exception:
        return ""
    return result.stdout


def risk_keywords_for_denied_action(action: str) -> set[str]:
    text = action.lower()
    keywords: set[str] = set()
    mapping = {
        "database schema/data": ["db/", "database", "schema", "drizzle", "migration", "migrate", "seed", "sql"],
        "package model": ["package", "packages", "pricing", "free30", "premium", "boost"],
        "credit": ["credit", "credit_transactions", "ledger"],
        "checkout": ["checkout", "pending", "purchase"],
        "auth/payment/billing": ["auth", "payment", "billing", "session", "otp"],
        "member-admin": ["member-admin", "member admin", "member"],
        "public tunnel": ["cloudflared", "tunnel", "vercel", "deploy", "publish"],
        "service starts": ["dev server", "next dev", "docker", "compose", "webserver"],
        "secrets": ["secret", ".env", "credential", "token", "key"],
    }
    for label, values in mapping.items():
        if label in text:
            keywords.update(values)
    words = re.findall(r"[a-zA-Z_/-]{4,}", text)
    keywords.update(words[:8])
    return keywords


def risk_scan_report(root: Path, domain: str, project: Path, diff_text: str = "") -> tuple[str, list[str], str]:
    loop_text = read_text_if_exists(root / "domains" / domain / "LOOP.md")
    denied = extract_section(loop_text, "Denied Actions")
    diff = diff_text if diff_text else project_git_diff(project)
    haystack = diff.lower()
    hits: list[str] = []
    for action in denied:
        keywords = risk_keywords_for_denied_action(action)
        if any(keyword and keyword.lower() in haystack for keyword in keywords):
            hits.append(action)
    level = "high" if hits else ("low" if diff.strip() else "none")
    return level, hits, diff


def risk_scan_data(root: Path, domain: str, project: Path, diff_text: str = "") -> dict:
    level, hits, diff = risk_scan_report(root, domain, project, diff_text)
    return {
        "domain": domain,
        "project": str(project),
        "risk_level": level,
        "matched_denied_actions": hits,
        "diff_source": "provided" if diff_text else "git_diff",
        "has_diff": bool(diff.strip()),
        "project_write_safety": {
            "project_files_modified": False,
            "commands_executed": "read-only git diff only when needed",
        },
    }


def print_risk_scan(root: Path, domain: str, project: Path, diff_text: str = "") -> None:
    data = risk_scan_data(root, domain, project, diff_text)
    print(f"# Risk Scan — {domain}")
    print(f"Project: {project}")
    print(f"Risk Level: {data['risk_level']}")
    print("\n## Matched Denied Actions")
    print_lines(data["matched_denied_actions"], limit=20)
    print("\n## Diff Source")
    print("- Provided diff text" if diff_text else "- git diff from project")
    print("\n## Project Write Safety")
    print("- No project files modified.")
    print("- No commands executed inside project except read-only git diff when needed.")


def extract_fenced_commands(markdown: str, heading: str | None = None) -> list[str]:
    commands: list[str] = []
    in_code = False
    in_heading = heading is None
    target = f"## {heading}".lower() if heading else ""
    for line in markdown.splitlines():
        stripped = line.strip()
        if heading and stripped.startswith("## "):
            if in_heading and stripped.lower() != target:
                break
            in_heading = stripped.lower() == target
            continue
        if not in_heading:
            continue
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code and stripped and not stripped.startswith("#"):
            commands.append(stripped)
    return commands


def render_approval_pack(root: Path, domain: str, project: Path, task: str, test_output: str = "not run", diff_text: str = "") -> str:
    verify_text = read_text_if_exists(root / "domains" / domain / "verify.md")
    level, hits, diff = risk_scan_report(root, domain, project, diff_text)
    commands = extract_fenced_commands(verify_text, "Recommended Future L2 Default Verification") or extract_fenced_commands(verify_text)
    lines = [
        f"# L2 Approval Package — {domain}",
        f"Project: {project}",
        f"Task: {task}",
        "",
        "## Verification Commands From Profile",
    ]
    command_lines = [f"- `{command}`" for command in commands[:10]]
    lines.extend(command_lines or ["- None"])
    lines.extend([
        "",
        "## Risk Scan",
        f"- Risk Level: {level}",
    ])
    if hits:
        lines.extend(hits)
    else:
        lines.append("- No denied-action keywords matched current diff.")
    lines.extend([
        "",
        "## Test / Build Output",
        f"- {test_output}",
        "",
        "## Required Gates",
        "- Separate verifier required.",
        "- No auto-merge.",
        "- No push/deploy/publish/service start without approval.",
        "- Mike approval required.",
        "",
        "## Project Write Safety",
        "- No project files modified by approval-pack.",
    ])
    return "\n".join(lines) + "\n"


def approval_pack_data(root: Path, domain: str, project: Path, task: str, test_output: str = "not run", diff_text: str = "") -> dict:
    verify_text = read_text_if_exists(root / "domains" / domain / "verify.md")
    level, hits, diff = risk_scan_report(root, domain, project, diff_text)
    commands = extract_fenced_commands(verify_text, "Recommended Future L2 Default Verification") or extract_fenced_commands(verify_text)
    return {
        "domain": domain,
        "project": str(project),
        "task": task,
        "verification_commands": commands[:10],
        "risk_scan": {
            "risk_level": level,
            "matched_denied_actions": hits,
            "has_diff": bool(diff.strip()),
        },
        "test_output": test_output,
        "required_gates": [
            "Separate verifier required.",
            "No auto-merge.",
            "No push/deploy/publish/service start without approval.",
            "Mike approval required.",
        ],
        "project_write_safety": {"project_files_modified": False},
    }


def write_approval_pack(root: Path, domain: str, body: str, task: str) -> Path:
    folder = root / "artifacts" / "approval-packs"
    folder.mkdir(parents=True, exist_ok=True)
    now = utc_now()
    path = folder / f"{now.replace(':', '').replace('-', '')}-{slugify(domain)}-{slugify(task)}.md"
    content = f"""---
id: approval-pack-{now.replace(':', '').replace('-', '')}-{slugify(task)}
type: approval-pack
domain: {domain}
status: draft
source: brain approval-pack
created_at: {now}
---

{body}"""
    path.write_text(content, encoding="utf-8")
    return path


def print_approval_pack(root: Path, domain: str, project: Path, task: str, test_output: str = "not run", diff_text: str = "", output: str = "") -> None:
    body = render_approval_pack(root, domain, project, task, test_output, diff_text)
    if output:
        if output != "artifacts":
            path = Path(output).expanduser()
            if not path.is_absolute():
                path = root / path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")
        else:
            path = write_approval_pack(root, domain, body, task)
        print(f"Saved approval package: {path}")
        return
    print(body, end="")


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


def domain_triage_data(root: Path, domain: str) -> dict:
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
    sources = [path.relative_to(root).as_posix() for path in [loop_path, state_path, backlog_path, timeline_path] if path.exists()]
    return {
        "domain": domain,
        "root": str(root),
        "goal": extract_section(loop_text, "Goal"),
        "current_focus": extract_section(state_text, "Current Focus"),
        "blocked_needs_mike": extract_section(state_text, "Blocked / Needs Mike"),
        "watch_list_risks": extract_section(state_text, "Watch List") or extract_section(loop_text, "Denied Actions"),
        "next_safe_actions": extract_section(backlog_text, "Next Safe L1 Actions") or extract_section(backlog_text, "Next Safe Actions"),
        "open_tasks": [{"title": read_title(path), "path": path.relative_to(root).as_posix()} for path in tasks],
        "signals": [{"title": read_title(path), "path": path.relative_to(root).as_posix()} for path in signals],
        "denied_actions": extract_section(loop_text, "Denied Actions"),
        "recent_timeline": [line for line in timeline_text.splitlines() if line.startswith("## ") or line.startswith("- ")][-8:],
        "sources_read": sources,
        "safety": "No auto-actions taken. L1 report-only.",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="brain", description="Portable Markdown-first AI Brain stack")
    parser.add_argument("--root", default=".", help="AI Brain root folder")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Create brain skeleton")
    p_init.add_argument("--domains", nargs="*", default=[])

    p_init_domain = sub.add_parser("init-domain", help="Create one domain with LOOP/STATE/backlog/timeline/verify")
    p_init_domain.add_argument("--domain", required=True)
    p_init_domain.add_argument("--path", default="", help="Project path or scope label")
    p_init_domain.add_argument("--status", default="L1-ready")
    p_init_domain.add_argument("--next", default="Run L1 triage.", help="Default next safe action for ACTIVE.md")
    p_init_domain.add_argument("--active", action="store_true", help="Add this domain to ACTIVE.md if missing")

    p_status = sub.add_parser("status", help="Show domains and artifact counts")
    p_status.add_argument("--json", action="store_true", help="Print machine-readable JSON")

    p_projects = sub.add_parser("projects", help="List active projects from ACTIVE.md")
    p_projects.add_argument("--json", action="store_true", help="Print machine-readable JSON")

    p_audit = sub.add_parser("audit", help="Audit active brain readiness")
    p_audit.add_argument("--json", action="store_true", help="Print machine-readable JSON")

    p_loop = sub.add_parser("loop", help="Run safe loop orchestration")
    loop_sub = p_loop.add_subparsers(dest="loop_command", required=True)
    p_loop_run = loop_sub.add_parser("run", help="Run one safe L1 loop step")
    p_loop_run.add_argument("--domain", required=True)
    p_loop_run.add_argument("--project", required=True)
    p_loop_run.add_argument("--once", action="store_true", help="Run one L1 loop step")
    p_loop_run.add_argument("--diff", default="", help="Optional diff text. If omitted, reads git diff from project.")
    p_loop_run.add_argument("--json", action="store_true", help="Print machine-readable JSON")

    for shortcut_name in ["next", "ทำต่อ"]:
        p_shortcut = sub.add_parser(shortcut_name, help="Run one safe L1 loop for the first active project")
        p_shortcut.add_argument("--domain", default="", help="Optional active domain override")
        p_shortcut.add_argument("--project", default="", help="Optional project path override")
        p_shortcut.add_argument("--diff", default="", help="Optional diff text. If omitted, reads git diff from project.")
        p_shortcut.add_argument("--json", action="store_true", help="Print machine-readable JSON")

    sub.add_parser("codex", help="Print a ready-to-run Codex L1 command")
    sub.add_parser("claude", help="Print a ready-to-run Claude Code L1 command")

    p_run_log = sub.add_parser("run-log", help="Manage loop run log")
    run_log_sub = p_run_log.add_subparsers(dest="run_log_command", required=True)
    p_run_log_add = run_log_sub.add_parser("add", help="Append a loop run entry")
    p_run_log_add.add_argument("--domain", required=True)
    p_run_log_add.add_argument("--summary", required=True)
    p_run_log_add.add_argument("--status", default="success")
    p_run_log_add.add_argument("--cost", default="0")
    p_run_log_add.add_argument("--tokens", default="0")
    p_run_log_summary = run_log_sub.add_parser("summary", help="Summarize loop runs")
    p_run_log_summary.add_argument("--json", action="store_true", help="Print machine-readable JSON")

    p_budget = sub.add_parser("budget", help="Manage loop budget")
    budget_sub = p_budget.add_subparsers(dest="budget_command", required=True)
    p_budget_set = budget_sub.add_parser("set", help="Set monthly budget")
    p_budget_set.add_argument("--monthly-usd", required=True)
    p_budget_set.add_argument("--notes", default="")
    p_budget_status = budget_sub.add_parser("status", help="Show budget status")
    p_budget_status.add_argument("--json", action="store_true", help="Print machine-readable JSON")

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
    p_triage.add_argument("--json", action="store_true", help="Print machine-readable JSON")

    p_risk = sub.add_parser("risk-scan", help="Scan diff against domain denied actions")
    p_risk.add_argument("--domain", required=True)
    p_risk.add_argument("--project", required=True)
    p_risk.add_argument("--diff", default="", help="Optional diff text. If omitted, reads git diff from project.")
    p_risk.add_argument("--json", action="store_true", help="Print machine-readable JSON")

    p_pack = sub.add_parser("approval-pack", help="Print L2 approval package draft")
    p_pack.add_argument("--domain", required=True)
    p_pack.add_argument("--project", required=True)
    p_pack.add_argument("--task", required=True)
    p_pack.add_argument("--test-output", default="not run")
    p_pack.add_argument("--diff", default="", help="Optional diff text. If omitted, reads git diff from project.")
    p_pack.add_argument("--output", default="", help="Optional path to save package, or 'artifacts' for artifacts/approval-packs/.")
    p_pack.add_argument("--json", action="store_true", help="Print machine-readable JSON; cannot be combined with --output")
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

    if args.command == "init-domain":
        init_domain(root, args.domain, args.path, args.status, args.next, args.active)
        print(f"Initialized domain: {args.domain}")
        print(f"Path / Scope: {args.path or 'TBD'}")
        print(f"Active: {'yes' if args.active else 'no'}")
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
        data = status_data(root)
        if args.json:
            print_json(data)
            return
        print(f"AI Brain: {root}")
        print("Domains: " + (", ".join(data["domains"]) if data["domains"] else "none"))
        for kind in ARTIFACT_FOLDERS:
            print(f"{kind}: {data['artifacts'][kind]}")
        return

    if args.command == "projects":
        if args.json:
            print_json(active_projects_data(root))
            return
        print_projects(root)
        return

    if args.command == "audit":
        if args.json:
            print_json(audit_data(root))
            return
        print_audit(root)
        return

    if args.command == "loop" and args.loop_command == "run":
        project = Path(args.project).expanduser().resolve()
        data = loop_run_once_data(root, args.domain, project, args.diff, write_log=True)
        if args.json:
            print_json(data)
            return
        print_loop_run_once(data)
        return

    if args.command in {"next", "ทำต่อ"}:
        domain, project = resolve_active_loop_target(root, args.domain, args.project)
        data = loop_run_once_data(root, domain, project, args.diff, write_log=True)
        if args.json:
            print_json(data)
            return
        print_loop_run_once(data)
        return

    if args.command in {"codex", "claude"}:
        print_agent_command(root, args.command)
        return

    if args.command == "run-log":
        if args.run_log_command == "add":
            path = write_run_log(root, args.domain, args.summary, args.status, args.cost, args.tokens)
            print(f"Logged run: {path}")
            return
        if args.run_log_command == "summary":
            if args.json:
                print_json(run_log_summary_data(root))
                return
            print_run_log_summary(root)
            return

    if args.command == "budget":
        if args.budget_command == "set":
            path = set_budget(root, args.monthly_usd, args.notes)
            print(f"Set budget: {path}")
            return
        if args.budget_command == "status":
            if args.json:
                print_json(read_budget(root))
                return
            print_budget_status(root)
            return

    if args.command == "triage":
        if args.json:
            print_json(domain_triage_data(root, args.domain))
            return
        print_domain_triage(root, args.domain)
        return

    if args.command == "risk-scan":
        project = Path(args.project).expanduser().resolve()
        if args.json:
            print_json(risk_scan_data(root, args.domain, project, args.diff))
            return
        print_risk_scan(root, args.domain, project, args.diff)
        return

    if args.command == "approval-pack":
        if args.json and args.output:
            parser.error("approval-pack --json cannot be combined with --output")
        project = Path(args.project).expanduser().resolve()
        if args.json:
            print_json(approval_pack_data(root, args.domain, project, args.task, args.test_output, args.diff))
            return
        print_approval_pack(root, args.domain, project, args.task, args.test_output, args.diff, args.output)
        return

    parser.error("Unhandled command")


if __name__ == "__main__":
    main()
