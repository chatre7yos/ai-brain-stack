# AI Brain Stack Context

This file defines the shared language for agents working in this repository.

Use these terms consistently. If an agent is unsure, it should ask or run a read-only `brain` command instead of guessing.

## Core terms

**AI Brain Stack**
: The public tool repo. It contains the `brain` CLI, templates, docs, and tests.

**Brain root**
: A private Markdown folder that stores project state. Example: `~/ai-brain`. This is not the same as this public repo.

**Domain**
: One project or work area inside a brain root. Each domain should have files like `LOOP.md`, `STATE.md`, `backlog.md`, `timeline.md`, and `verify.md`.

**Active project**
: A row in `ACTIVE.md` that tells the agent what project is currently in scope.

**Loop**
: A safe operating cycle: read state, audit, triage, scan risk, report next action, record the run, then stop.

**L1**
: Read-only/report-only mode. L1 commands may inspect state and diffs, but must not edit project files or perform external writes.

**L2**
: Assisted implementation mode. L2 requires explicit human approval and should normally start from an approval pack.

**L3**
: Autonomous/multi-step execution. Not implemented in this repo.

**Risk scan**
: A check of the current diff against denied actions and scope boundaries.

**Approval pack**
: A structured package that explains the task, risk, allowed files/commands, verification, and required human gates before L2 work.

**Run log**
: A lightweight record of loop runs, status, cost, and tokens.

**Budget**
: A lightweight monthly cap for loop/agent usage. It is informational; it does not call a provider API by itself.

**Out of scope**
: Anything explicitly denied for a domain or current run. If a requested action conflicts with out-of-scope rules, stop and ask.

## Human commands

Use these first:

```bash
brain setup --domain <name> --path <path>
brain next
brain ทำต่อ
brain codex
brain claude
```

## Agent-safe L1 commands

Agents may run these in read-only/report-only mode:

```bash
brain projects --json
brain audit --json
brain triage --domain <domain> --json
brain risk-scan --domain <domain> --project <path> --json
brain next --json
```

## Approval-required actions

Do not do these unless the user explicitly approves the exact scope:

- edit product/project code
- commit or push
- deploy or publish
- start services, tunnels, or daemons
- touch secrets, credentials, billing, production data, migrations, or auth
- operate outside the active domain

## Default behavior

When asked to continue work, prefer:

```bash
brain next
```

or, in Thai:

```bash
brain ทำต่อ
```

Then report the result and stop unless implementation is explicitly approved.
