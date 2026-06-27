# Agent Instructions

This repo is a small local CLI/control layer for safer AI-agent work.

Default posture: **L1 report-first**. Inspect, explain, and verify before changing behavior.

## Read first

Before making changes, read:

```text
README.md
docs/QUICKSTART.md
docs/MAP.md
CONTEXT.md
```

Use `docs/MAP.md` to decide where a new file belongs.

## Scope boundaries

Do not do these unless the user explicitly asks for them:

```text
- edit unrelated projects
- commit or push
- deploy or publish
- start services, tunnels, daemons, or watchers
- touch secrets, credentials, tokens, billing, production data, or private brain roots
- add autonomous agent execution
- add package/plugin/showcase surface area
```

Private brain roots such as `~/ai-brain` are user data. Do not copy them into this repo.

## Safe default commands

For repo status:

```bash
git status --short --branch
```

For tests:

```bash
python3 -m unittest discover -s tests -v
```

For setup smoke:

```bash
tmp="$(mktemp -d)"
python3 -m brain.cli --root "$tmp/brain" setup --domain demo --path "$tmp/project" --create-project-dir
python3 -m brain.cli --root "$tmp/brain" next
rm -rf "$tmp"
```

For GitHub CI status after pushing:

```bash
gh run list --repo chatre7yos/ai-brain-stack --workflow tests.yml --limit 1
```

## Change rules

### CLI behavior

If changing CLI behavior:

1. Add or update a test in `tests/test_cli.py` first.
2. Implement the smallest slice in `brain/cli.py`.
3. Update `README.md` or `docs/usage.md`.
4. Run tests and the setup smoke.

### Docs-only changes

If changing docs only:

1. Keep docs short and linked from `docs/MAP.md` when they add a new surface.
2. Avoid duplicating long instructions across many files.
3. Run tests anyway before claiming completion.

### Patterns and skills

Patterns and skills guide agent behavior. They should not add product behavior by themselves.

Use:

```text
docs/patterns/
skills/
```

Do not add a new skill/pattern unless it prevents scope drift, improves agent handoff, or clarifies a repeated workflow.

## Verification checklist

Before saying work is complete:

```text
- git status --short --branch
- python3 -m unittest discover -s tests -v
- setup smoke passes
- git diff --check
- no secrets in changed files
- if pushed: GitHub Actions tests workflow is success
```

## Output style

Report concise evidence:

```text
Summary:
Tests:
Smoke:
Commit:
CI:
Scope:
```

Do not claim success without real command output.
