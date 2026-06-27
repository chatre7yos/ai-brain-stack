# Quickstart: 5 Minutes

Use this when you just cloned AI Brain Stack and want the shortest safe path from zero to `brain next`.

## What you will create

Two separate things:

```text
ai-brain-stack  = this public tool repo
~/ai-brain      = your private project memory folder
```

Keep the private brain folder out of public repos unless you intentionally scrub and publish it.

## 1. Clone and enter the repo

```bash
git clone https://github.com/chatre7yos/ai-brain-stack.git
cd ai-brain-stack
```

## 2. Run the test suite

```bash
python3 -m unittest discover -s tests -v
```

Expected result:

```text
OK
```

## 3. Install the local `brain` shortcut

```bash
mkdir -p ~/.local/bin
ln -sfn "$PWD/bin/brain" ~/.local/bin/brain
```

Make sure `~/.local/bin` is on your `PATH`.

Verify:

```bash
brain --help
```

If you do not want the shortcut, use module form instead:

```bash
python3 -m brain.cli --help
```

## 4. Connect your first project

If the project directory already exists:

```bash
brain --root ~/ai-brain setup \
  --domain my-project \
  --path /path/to/my-project
```

If the project directory does not exist and you want setup to create it:

```bash
brain --root ~/ai-brain setup \
  --domain my-project \
  --path /path/to/my-project \
  --create-project-dir
```

This creates safe local Markdown state under `~/ai-brain`, including:

```text
ACTIVE.md
domains/my-project/LOOP.md
domains/my-project/STATE.md
domains/my-project/backlog.md
domains/my-project/timeline.md
domains/my-project/verify.md
domains/my-project/out-of-scope.md
```

Existing files are not overwritten.

## 5. Run your first safe loop

```bash
brain --root ~/ai-brain next
```

Expected shape:

```text
# Loop Run — my-project
Status: ok
Audit: ok
Risk Level: none
```

This is L1/report-only. It does not edit project files, commit, push, deploy, start services, or touch secrets.

## Optional: make `~/ai-brain` the default

The `bin/brain` wrapper already defaults to `$HOME/ai-brain` when no `--root` is passed.

After setup, this should work:

```bash
brain next
```

## Optional: hand off to Codex or Claude

For Codex:

```bash
brain codex
```

For Claude Code:

```bash
brain claude
```

Copy and run the printed command from the project repo. The generated prompt keeps the agent in L1/report-only mode.

## Safety checklist

Before moving to implementation, confirm:

```text
- `brain next` is ok or the warnings are understood
- `domains/<project>/out-of-scope.md` lists hard stops
- verification is clear in `domains/<project>/verify.md`
- L2 work has explicit human approval
```

For implementation planning, create an approval pack:

```bash
brain approval-pack \
  --domain my-project \
  --project /path/to/my-project \
  --task "small scoped task"
```

## Where to go next

| Need | File |
|---|---|
| Repo navigation | `docs/MAP.md` |
| Command boundaries | `docs/commands.md` |
| Daily workflow | `docs/daily-usage.md` |
| Agent examples | `docs/agent-examples.md` |
| Fuzzy-plan grilling | `docs/patterns/grill-with-docs.md` |
