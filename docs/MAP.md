# AI Brain Stack Map

Use this file to decide where to read or write next. It keeps the repo from turning into a pile of docs.

## Start here

| Need | File |
|---|---|
| Set up in 5 minutes | `docs/QUICKSTART.md` |
| Agent/contributor guardrails | `AGENTS.md` |
| Understand what this repo is | `README.md` |
| Understand the shared vocabulary | `CONTEXT.md` |
| Know where things live | `docs/MAP.md` |

## Human daily use

| Need | File / command |
|---|---|
| Start or continue the active project | `brain next` / `brain ทำต่อ` |
| First-time setup | `docs/QUICKSTART.md` |
| Create a first brain/project link | `brain setup --domain <name> --path <path>` |
| Daily workflow guide | `docs/daily-usage.md` |
| Full command boundary guide | `docs/commands.md` |
| Command examples | `docs/usage.md` |

## Agent handoff

| Need | File / command |
|---|---|
| Give Codex a safe L1 prompt | `brain codex` |
| Give Claude Code a safe L1 prompt | `brain claude` |
| Agent examples for Codex/Claude/agy | `docs/agent-examples.md` |
| Machine-readable current state | `brain next --json` |
| Agent vocabulary / safety levels | `CONTEXT.md` |

## Patterns and skills

| Need | File |
|---|---|
| Sharpen a fuzzy plan before implementation | `docs/patterns/grill-with-docs.md` |
| Agent skill version of that pattern | `skills/engineering/grill-with-docs/SKILL.md` |

Rule: patterns and skills should not add product behavior. They guide how an agent asks questions or writes docs. CLI behavior belongs in `brain/cli.py` with tests.

## CLI source

| Need | File |
|---|---|
| CLI implementation | `brain/cli.py` |
| Shell wrapper | `bin/brain` |
| Test suite | `tests/test_cli.py` |
| Python/package metadata | `pyproject.toml` |

Rule: every new CLI command should have a test in `tests/test_cli.py` and docs in `README.md` or `docs/usage.md`.

## Templates

| Need | File |
|---|---|
| Domain loop contract starter | `templates/LOOP.md` |
| Domain state starter | `templates/STATE.md` |
| Scope guard starter | `templates/out-of-scope.md` |
| Signal artifact starter | `templates/signal.md` |
| Task artifact starter | `templates/task.md` |

Rule: templates are public starters only. Private project data belongs in the user's brain root, not this repo.

## Planning history

| Need | File |
|---|---|
| MVP plan / historical implementation context | `docs/plans/2026-06-26-portable-ai-brain-stack-mvp.md` |

Rule: planning docs are historical context. Current usage should stay in README and `docs/` guides.

## Private brain root, not this repo

A user's actual brain root normally lives outside this repo, for example:

```text
~/ai-brain
```

It may contain:

```text
ACTIVE.md
domains/<project>/LOOP.md
domains/<project>/STATE.md
domains/<project>/backlog.md
domains/<project>/timeline.md
domains/<project>/verify.md
domains/<project>/out-of-scope.md
loop-run-log.md
loop-budget.md
worklog.md
artifacts/
```

Do not publish private brain roots by default.

## Add-new-file rule

Before adding a new file, choose one bucket:

1. **CLI behavior** → `brain/cli.py` + `tests/test_cli.py` + docs
2. **Human usage doc** → `docs/*.md`
3. **Agent handoff / pattern** → `docs/patterns/` or `skills/`
4. **Starter file** → `templates/`
5. **Historical plan** → `docs/plans/`

If it does not fit a bucket, do not add it yet.
