# Agent Usage Examples

Use these examples when you want another AI coding agent to follow the AI Brain workflow before touching a project.

The key idea is simple:

```text
Read the brain first. Report L1 state. Run risk scan. Do not implement until approval.
```

Replace paths and domain names for your own setup.

---

## Shared prompt template

Use this prompt with Codex, Claude Code, agy, or any terminal-capable agent:

```text
You are working inside a repo that uses AI Brain Stack.

Brain root: /path/to/ai-brain
Domain: my-project
Project path: /path/to/my-project

First run:

brain --root /path/to/ai-brain projects
brain --root /path/to/ai-brain audit
brain --root /path/to/ai-brain triage --domain my-project
brain --root /path/to/ai-brain risk-scan --domain my-project --project /path/to/my-project

Optional one-command L1 loop:

brain --root /path/to/ai-brain next
# or
brain --root /path/to/ai-brain ทำต่อ
# explicit target
brain --root /path/to/ai-brain loop run --domain my-project --project /path/to/my-project --once

Rules:
- L1 only unless explicitly approved.
- Do not edit code yet.
- Do not commit, push, deploy, start services, or touch secrets.
- If risk-scan reports high risk, stop and explain.
- Return: active focus, blockers, denied actions, next safe action, and evidence from commands.
```

---

## Codex example

Simplest form:

```bash
brain codex
```

Copy and run the printed `codex exec ...` command from the project repo.

Manual form:

Good for one-shot terminal/repo checks.

From the project repo:

```bash
cd /path/to/my-project
codex exec "
Use AI Brain Stack before making changes.

Brain root: /path/to/ai-brain
Domain: my-project
Project path: /path/to/my-project

Run:
brain --root /path/to/ai-brain projects
brain --root /path/to/ai-brain audit
brain --root /path/to/ai-brain triage --domain my-project
brain --root /path/to/ai-brain risk-scan --domain my-project --project /path/to/my-project

Optional one-command L1 loop:

brain --root /path/to/ai-brain next
# or
brain --root /path/to/ai-brain ทำต่อ
# explicit target
brain --root /path/to/ai-brain loop run --domain my-project --project /path/to/my-project --once

Do L1 report-only. Do not edit files. Do not commit/push/deploy.
Summarize blockers, denied actions, next safe action, and exact command evidence.
"
```

If your Codex CLI uses a different non-interactive flag, keep the prompt but adapt the wrapper command.

---

## Claude Code example

Simplest form:

```bash
brain claude
```

Copy and run the printed `claude -p ...` command from the project repo.

Manual form:

Good for repo-aware analysis and longer implementation sessions.

Read-only/L1 pass:

```bash
cd /path/to/my-project
claude -p "
Use AI Brain Stack as the operating layer.

Brain root: /path/to/ai-brain
Domain: my-project
Project path: /path/to/my-project

Run first:
brain --root /path/to/ai-brain projects
brain --root /path/to/ai-brain audit
brain --root /path/to/ai-brain triage --domain my-project
brain --root /path/to/ai-brain risk-scan --domain my-project --project /path/to/my-project

Optional one-command L1 loop:

brain --root /path/to/ai-brain next
# or
brain --root /path/to/ai-brain ทำต่อ
# explicit target
brain --root /path/to/ai-brain loop run --domain my-project --project /path/to/my-project --once

Stay L1 report-only. Do not edit files. Do not commit, push, deploy, start services, or touch secrets.
Return a concise report with: current focus, blockers, denied actions, risk level, next safe action.
"
```

If you want Claude to implement after approval, give it an approval package first:

```bash
brain --root /path/to/ai-brain approval-pack \
  --domain my-project \
  --project /path/to/my-project \
  --task "small scoped task"
```

Then paste the approval package into Claude and explicitly say which writes are allowed.

---

## agy example

Good for Gemini-family summary/review handoffs when you want a non-interactive answer.

```bash
cd /path/to/my-project
agy --model gemini-2.5-flash --print-timeout 3m --print "
Use AI Brain Stack for a read-only L1 check.

Brain root: /path/to/ai-brain
Domain: my-project
Project path: /path/to/my-project

Run or reason from these commands:
brain --root /path/to/ai-brain projects
brain --root /path/to/ai-brain audit
brain --root /path/to/ai-brain triage --domain my-project
brain --root /path/to/ai-brain risk-scan --domain my-project --project /path/to/my-project

Optional one-command L1 loop:

brain --root /path/to/ai-brain next
# or
brain --root /path/to/ai-brain ทำต่อ
# explicit target
brain --root /path/to/ai-brain loop run --domain my-project --project /path/to/my-project --once

Do not edit files. Do not commit/push/deploy. Do not touch secrets.
Return a compact report: focus, blockers, denied actions, risk level, next safe action.
"
```

If your agy environment cannot run shell commands, run the `brain ... --json` commands yourself and paste the JSON into agy.

Example source bundle:

```bash
brain --root /path/to/ai-brain projects --json > /tmp/brain-projects.json
brain --root /path/to/ai-brain audit --json > /tmp/brain-audit.json
brain --root /path/to/ai-brain triage --domain my-project --json > /tmp/brain-triage.json
brain --root /path/to/ai-brain risk-scan --domain my-project --project /path/to/my-project --json > /tmp/brain-risk.json
brain --root /path/to/ai-brain loop run --domain my-project --project /path/to/my-project --once --json > /tmp/brain-loop.json
```

Then ask agy to summarize only those files.

---

## Implementation mode pattern

Only use this after a human approval gate.

1. Generate an approval pack:

```bash
brain --root /path/to/ai-brain approval-pack \
  --domain my-project \
  --project /path/to/my-project \
  --task "small scoped task" \
  --output artifacts
```

2. Give the approval pack to the agent.
3. Restrict allowed files and commands.
4. Verify yourself after the agent finishes:

```bash
git diff --check
python3 -m unittest discover -s tests -v
brain --root /path/to/ai-brain risk-scan --domain my-project --project /path/to/my-project
```

5. Record the run:

```bash
brain --root /path/to/ai-brain run-log add \
  --domain my-project \
  --summary "Agent completed approved small task" \
  --status success
```
