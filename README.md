# AI Brain Stack

Portable Markdown-first shared brain for agent loops.

## What this is

A local-first tools stack for keeping agent work portable across Hermes, Claude Code, Codex, n8n, GitHub Actions, and plain terminal scripts.

It stores operational knowledge as Markdown:

```text
worklog.md
inbox.md
artifacts/
  signals/
  tasks/
  decisions/
  bugs/
  research/
  content-ideas/
domains/
  <domain>/
    LOOP.md
    STATE.md
    backlog.md
    timeline.md
```

## Safety default

The MVP is **L1 report-only**.

It does not edit application code, commit, push, publish, open tunnels, or touch secrets.

## Usage

Short form after linking `bin/brain` into PATH:

```bash
brain projects
brain audit
brain status
brain init-domain --domain new-project --path /home/mike/projects/new-project --active
brain run-log add --domain ai-brain-stack --summary "Finished audit" --cost 0.25 --tokens 1200
brain run-log summary
brain budget set --monthly-usd 20 --notes "MVP cap"
brain budget status
brain triage --domain robbaan
brain risk-scan --domain robbaan --project /home/mike/projects/robbaan
brain approval-pack --domain robbaan --project /home/mike/projects/robbaan --task "admin listing row"
```

The shortcut defaults to `$HOME/ai-brain`; override with `AI_BRAIN_ROOT=/path/to/brain` or pass `--root` explicitly.

Module form still works everywhere:

```bash
python3 -m brain.cli --root ./my-brain init --domains robbaan kliktan video-os
python3 -m brain.cli --root ./my-brain log --domain robbaan --message "Checked state"
python3 -m brain.cli --root ./my-brain signal add --domain video-os --title "Trend" --body "Observation" --priority high
python3 -m brain.cli --root ./my-brain task add --domain robbaan --title "Define LOOP" --body "Write allowed/denied actions" --priority high
python3 -m brain.cli --root ./my-brain status
python3 -m brain.cli --root ./my-brain triage --domain robbaan
```

See:

- `docs/usage.md` for shortcut installation and examples.
- `docs/daily-usage.md` for the daily `ทำต่อ` workflow.

## For other agents

Tell any agent:

```text
Read domains/<domain>/LOOP.md, STATE.md, backlog.md, timeline.md, then run L1 triage only. Do not edit code or perform external writes.
```
