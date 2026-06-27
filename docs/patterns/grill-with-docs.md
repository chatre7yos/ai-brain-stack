# Pattern: Grill With Docs

Use this pattern when a plan is too fuzzy for implementation.

Goal:

```text
Ask hard questions first, then capture the clarified result as docs so the next agent does not guess.
```

Inspired by Matt Pocock's `grill-with-docs` skill, adapted for AI Brain Stack's scope-control workflow.

## When to use

Use it before L2 implementation when:

- the user says an idea but not the exact scope
- terms are ambiguous
- the next action could touch product code
- multiple projects/modules are nearby
- the agent might overbuild
- verification is not clear yet

Do not use it to stall obvious small L1 checks. If the task is simply “show current status”, run `brain next`.

## Safe command flow

Start with the active project:

```bash
brain next
```

Or explicit target:

```bash
brain triage --domain <domain>
brain risk-scan --domain <domain> --project <path>
```

Then run the grilling conversation manually with the user or through an agent using the skill file:

```text
skills/engineering/grill-with-docs/SKILL.md
```

## Question set

Ask concrete questions:

1. What exact user flow changes?
2. What is explicitly out of scope?
3. What is the smallest useful slice?
4. What files or docs are the source of truth?
5. What failure case would make this unsafe?
6. What should the agent not touch even if related?
7. What output proves the work is done?
8. Does this need approval before L2 implementation?

## Documentation output

Capture the result in the right place:

| Result | File |
|---|---|
| stable vocabulary | `CONTEXT.md` or domain `CONTEXT.md` |
| current project state | `domains/<domain>/STATE.md` |
| next safe action | `domains/<domain>/backlog.md` |
| denied actions | `domains/<domain>/out-of-scope.md` |
| verification command | `domains/<domain>/verify.md` |
| L2 implementation boundary | `brain approval-pack ...` |

## Output shape

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

## Example

User says:

```text
Make the CLI easier to use.
```

Do not jump straight to code. Grill first:

```text
- Easier for whom: Mike daily use, public GitHub user, or Codex/Claude handoff?
- Is the target one command or fewer flags?
- Should setup create missing project dirs or refuse?
- What should remain impossible without approval?
- What test proves the new flow works?
```

Result might become:

```text
Smallest next safe action:
Add `brain setup --domain <name> --path <path> --create-project-dir` with tests and docs.
```

Then implement only that slice.

## Attribution

Conceptually inspired by Matt Pocock's MIT-licensed skills repo:

- https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md
- https://github.com/mattpocock/skills/blob/main/skills/engineering/domain-modeling/SKILL.md
