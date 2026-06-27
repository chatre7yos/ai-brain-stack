# Command Boundaries

This document separates commands intended for humans from commands that are safe for agents and automation.

The default rule is:

```text
Humans choose scope. Agents report first. Implementation requires approval.
```

---

## Human-first commands

These are the commands a person should normally use day to day.

| Command | Purpose |
|---|---|
| `brain setup --domain <name> --path <path>` | Bootstrap a local brain root and first active project. Add `--create-project-dir` only when you want setup to create that directory. |
| `brain next` | Run one safe L1 loop for the first active project |
| `brain ทำต่อ` | Thai alias for `brain next` |
| `brain codex` | Print a ready-to-run Codex L1 command |
| `brain claude` | Print a ready-to-run Claude Code L1 command |
| `brain init-domain ...` | Create a new project/domain skeleton |
| `brain budget set ...` | Set or update the local budget file |

Use `brain next` first unless you already know you need a specific lower-level command.

---

## Agent-safe L1 commands

Agents and automation may run these as read-only/report-only commands.

| Command | Why it is safe |
|---|---|
| `brain projects --json` | Reads `ACTIVE.md` only |
| `brain audit --json` | Checks brain readiness |
| `brain triage --domain <domain> --json` | Reads domain Markdown files |
| `brain risk-scan --domain <domain> --project <path> --json` | Reads git diff and denied actions |
| `brain next --json` | Runs one L1 loop, writes only run-log in the brain root |
| `brain run-log summary --json` | Reads run-log totals |
| `brain budget status --json` | Reads budget status |

L1 commands must not edit target project files.

---

## Approval-required L2 actions

These require explicit human approval for the exact project, files, and commands.

- editing product/project code
- running destructive commands
- database migrations or data writes
- auth, billing, credentials, secrets, or production data
- starting services, public tunnels, daemons, or long-running processes
- commit, push, release, deploy, publish, or upload
- moving to another domain/project

Use this before L2 work:

```bash
brain approval-pack \
  --domain <domain> \
  --project <path> \
  --task "<small scoped task>"
```

---

## Not implemented / L3

These are intentionally not implemented as default behavior:

- autonomous multi-step implementation
- automatic commit/push/deploy
- provider API execution through `brain`
- background daemons/watchers
- cross-project task selection

If a future command adds any of these, it must be opt-in and approval-gated.

---

## Recommended agent handoff

For Codex:

```bash
brain codex
```

For Claude Code:

```bash
brain claude
```

For generic automation:

```bash
brain next --json
```
