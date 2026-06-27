# Out of Scope

Use this file to make scope boundaries explicit before an agent starts work.

Copy this template into a domain when needed, for example:

```text
domains/<domain>/out-of-scope.md
```

## Always denied unless explicitly approved

- Do not edit unrelated projects or domains.
- Do not commit, push, deploy, publish, release, or upload.
- Do not start services, public tunnels, daemons, queues, or long-running processes.
- Do not touch secrets, tokens, credentials, auth, billing, production data, or migrations.
- Do not overwrite user files or generated artifacts without an explicit approval gate.
- Do not convert L1 report-only work into L2 implementation without approval.

## Project-specific denied actions

Add concrete project-specific rules here.

Example:

```text
- Do not edit the main app code while the active focus is tooling/docs.
- Do not run production migrations.
- Do not change deployment config.
```

## Allowed in L1

- Read Markdown brain files.
- Run `brain projects`, `brain audit`, `brain triage`, `brain risk-scan`, or `brain next`.
- Read git status/diff.
- Report blockers, risk, and next safe action.

## Requires L2 approval

- Editing project files.
- Running tests that start services or touch external systems.
- Creating commits or pushing branches.
- Writing approval-pack artifacts.

## Stop condition

If a requested action conflicts with this file, stop and ask for approval before continuing.
