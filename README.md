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

```bash
python3 -m brain.cli --root ./my-brain init --domains robbaan kliktan video-os
python3 -m brain.cli --root ./my-brain log --domain robbaan --message "Checked state"
python3 -m brain.cli --root ./my-brain signal add --domain video-os --title "Trend" --body "Observation" --priority high
python3 -m brain.cli --root ./my-brain task add --domain robbaan --title "Define LOOP" --body "Write allowed/denied actions" --priority high
python3 -m brain.cli --root ./my-brain status
python3 -m brain.cli --root ./my-brain triage --domain robbaan
```

## For other agents

Tell any agent:

```text
Read domains/<domain>/LOOP.md, STATE.md, backlog.md, timeline.md, then run L1 triage only. Do not edit code or perform external writes.
```
