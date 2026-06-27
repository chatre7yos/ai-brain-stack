# AI Brain Stack

A small local CLI for keeping AI-agent work organized and safe.

It gives an agent a simple operating system before it touches code:

```text
Which project are we working on?
What is the current state?
What is allowed?
What is blocked?
What should be verified first?
What needs approval before implementation?
```

The main command is `brain`.

---

## Why this exists

AI coding agents often fail in boring but expensive ways:

- they forget project context
- they jump into the wrong repo
- they keep working outside the requested scope
- they make changes before checking risk
- they do not leave a useful handoff for the next run

AI Brain Stack solves that by storing project memory as Markdown files and exposing a small CLI around them.

It is not another chat app. It is not an autonomous agent by itself.

It is the **control layer** an agent reads before acting.

---

## Mental model

```text
ai-brain-stack  = the tool / CLI / templates
my-brain-folder = your private project memory and run logs
```

This repo is the tool.

Your actual project state lives in a separate folder, for example:

```text
~/ai-brain
```

That private brain folder can contain sensitive project notes, so it should usually stay private.

---

## What the CLI does

| Command | Purpose |
|---|---|
| `brain projects` | List active projects from `ACTIVE.md` |
| `brain audit` | Check whether the brain folder is healthy |
| `brain triage --domain <name>` | Read a project/domain and print a safe L1 report |
| `brain risk-scan --domain <name> --project <path>` | Check current git diff against denied actions |
| `brain approval-pack ...` | Draft an approval package before L2 implementation |
| `brain init-domain ...` | Create a new project/domain skeleton |
| `brain run-log ...` | Track loop runs, cost, and tokens |
| `brain budget ...` | Track a lightweight monthly budget |

Most commands also support `--json` for automation.

Agent examples:

- `docs/agent-examples.md` shows how to use AI Brain Stack with Codex, Claude Code, and agy.

---

## Install / local setup

Clone the repo:

```bash
git clone https://github.com/chatre7yos/ai-brain-stack.git
cd ai-brain-stack
```

Run tests:

```bash
python3 -m unittest discover -s tests -v
```

Use module form without installing anything:

```bash
python3 -m brain.cli --root ~/ai-brain init
python3 -m brain.cli --root ~/ai-brain status
```

Optional shortcut:

```bash
mkdir -p ~/.local/bin
ln -sfn "$PWD/bin/brain" ~/.local/bin/brain
```

Then:

```bash
brain --root ~/ai-brain status
```

By default, `bin/brain` uses:

```text
$HOME/ai-brain
```

Override it with:

```bash
AI_BRAIN_ROOT=/path/to/brain brain projects
```

---

## Quickstart

Create a private brain folder:

```bash
brain --root ~/ai-brain init
```

Create your first project/domain:

```bash
brain --root ~/ai-brain init-domain \
  --domain my-project \
  --path /path/to/my-project \
  --active
```

Check the brain:

```bash
brain --root ~/ai-brain audit
```

Start a safe read-only loop:

```bash
brain --root ~/ai-brain projects
brain --root ~/ai-brain triage --domain my-project
brain --root ~/ai-brain risk-scan --domain my-project --project /path/to/my-project
```

Record the run:

```bash
brain --root ~/ai-brain run-log add \
  --domain my-project \
  --summary "First read-only check" \
  --status success
```

---

## Folder structure created by a brain

A brain folder is Markdown-first:

```text
~/ai-brain/
  ACTIVE.md
  worklog.md
  loop-run-log.md
  loop-budget.md
  artifacts/
    signals/
    tasks/
    decisions/
    bugs/
    research/
    content-ideas/
    approval-packs/
  domains/
    my-project/
      LOOP.md
      STATE.md
      backlog.md
      timeline.md
      verify.md
```

The important files are:

| File | Meaning |
|---|---|
| `ACTIVE.md` | Which projects are currently active |
| `LOOP.md` | Goal, allowed actions, denied actions |
| `STATE.md` | Current focus and blockers |
| `backlog.md` | Next safe actions |
| `timeline.md` | Recent history |
| `verify.md` | How to verify safely |

---

## Safety levels

AI Brain Stack is designed around safety gates:

```text
L1 = read-only report / triage / risk scan
L2 = assisted implementation only after approval package
L3 = unattended automation; not recommended by default
```

The default is L1.

That means the agent should read, report, and verify before writing code.

---

## Example daily workflow

When you say “continue this project” to an agent, the intended flow is:

```bash
brain projects
brain audit
brain triage --domain <active-project>
brain risk-scan --domain <active-project> --project <project-path>
```

Only after that should the agent propose or execute the next safe action.

If implementation is needed, create an approval package first:

```bash
brain approval-pack \
  --domain <active-project> \
  --project <project-path> \
  --task "small scoped task"
```

---

## JSON automation

Use JSON output for cron jobs, n8n, CI, or other agents:

```bash
brain projects --json
brain audit --json
brain triage --domain my-project --json
brain risk-scan --domain my-project --project /path/to/my-project --json
brain approval-pack --domain my-project --project /path/to/my-project --task "small task" --json
brain run-log summary --json
brain budget status --json
```

---

## Compatibility

Tested in this repo:

| Area | Status |
|---|---|
| Python | Requires Python 3.11+ (`pyproject.toml`) |
| Current test runtime | Python 3.11.15 |
| OS / shell | Linux/WSL with Bash |
| Git projects | Works with local Git working trees for `risk-scan` |
| Brain storage | Plain Markdown folders and files |
| Automation | JSON output for scripts, cron, n8n, CI, or other agents |

Should also work with minimal or no changes:

- macOS with Python 3.11+, Bash, and Git
- Linux servers or dev containers with Python 3.11+
- WSL on Windows
- any AI coding agent that can read files and run shell commands

Not packaged/tested yet:

- native Windows `cmd.exe` / PowerShell wrapper
- pip package release
- npm package release
- Docker image
- hosted web UI
- GitHub Actions templates

Compatible agent workflows:

- Hermes Agent
- Claude Code
- Codex-style terminal agents
- Cursor/IDE agents that can read Markdown project state
- n8n/cron/CI flows via `--json`

Important: the public repo is only the tool. Your private brain folder, project notes, run logs, and domain state should normally stay outside the repo.

---

## What this is not

AI Brain Stack is not:

- a hosted SaaS
- a vector database
- an autonomous agent runtime
- a replacement for GitHub Issues or Linear
- a tool that magically understands your project without Markdown state

It is a small local control layer for safer agent loops.

---

## Repository contents

```text
bin/brain             CLI wrapper
brain/cli.py          Main Python CLI
docs/usage.md         CLI examples
docs/daily-usage.md   Daily workflow guide
docs/agent-examples.md Agent handoff examples for Codex, Claude Code, and agy
templates/            Starter Markdown templates
tests/test_cli.py     Test suite
```

---

## Current status

This is an MVP.

It is ready for local/private use as a project-control layer. Public packaging, hosted docs, and broader starter templates can come later.
