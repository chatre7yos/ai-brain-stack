---
name: grill-with-docs
description: Run a focused grilling session to sharpen a plan/design and capture the result as domain docs, glossary terms, ADR candidates, and AI Brain next actions.
disable-model-invocation: true
source: Inspired by mattpocock/skills skills/engineering/grill-with-docs/SKILL.md (MIT)
---

# Grill With Docs

Use this when a plan, feature, architecture, or product loop feels fuzzy and needs hard questioning before implementation.

This is an AI Brain Stack-native adaptation of Matt Pocock's `grill-with-docs` idea: ask relentless clarifying questions, then write down the clarified model so future agents do not guess.

## Default safety level

L1 report/docs-first.

Do not edit product code, commit, push, deploy, start services, or touch secrets from this skill alone.

## Inputs

Ask for or infer:

- domain/project name
- project path
- current goal or plan
- constraints / denied actions
- target user flow
- evidence source: docs, code, backlog, current diff, or user statement

If scope is unclear, run:

```bash
brain next
```

or explicit:

```bash
brain triage --domain <domain>
brain risk-scan --domain <domain> --project <path>
```

## Grilling loop

Ask concrete questions until the plan is precise enough to either stop or create an approval pack.

Prefer questions like:

1. What exact user flow changes?
2. What is explicitly out of scope?
3. What file/module/data is the source of truth?
4. What would make this unsafe to automate?
5. What is the smallest useful slice?
6. What observable result proves this works?
7. What must not be changed even if nearby code looks tempting?
8. Which terms are overloaded or ambiguous?
9. What are the failure cases?
10. What approval gate is needed before L2 work?

## Capture docs as you go

When terms become clear, update or propose updates to:

```text
CONTEXT.md
domains/<domain>/STATE.md
domains/<domain>/backlog.md
domains/<domain>/verify.md
domains/<domain>/out-of-scope.md
```

For public repo docs, prefer:

```text
docs/patterns/<pattern>.md
docs/commands.md
docs/agent-examples.md
```

Keep `CONTEXT.md` glossary-like: terms and meanings only. Put implementation decisions in an ADR or approval pack.

## ADR rule

Only propose an ADR when all are true:

1. hard to reverse
2. surprising without context
3. real trade-off with rejected alternatives

If not, use a short note in `STATE.md`, `backlog.md`, or a pattern doc instead.

## Output format

Return:

```text
## Grilled summary
- Decision / sharpened plan:
- Out of scope:
- Open questions:
- Risks:
- Smallest next safe action:
- Docs to update:
- Approval needed before L2?: yes/no
```

## Stop conditions

Stop and ask if:

- user flow is still ambiguous
- scope conflicts with `out-of-scope.md`
- action implies product code edits, DB, secrets, deploy, or commit/push
- agent would need to choose between two product directions
- verification cannot be named concretely

## Attribution

Conceptually inspired by:

- `mattpocock/skills/skills/engineering/grill-with-docs/SKILL.md`
- `mattpocock/skills/skills/engineering/domain-modeling/SKILL.md`

Upstream repo: https://github.com/mattpocock/skills
License: MIT
