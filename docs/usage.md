# AI Brain CLI Usage

## Local shortcut

Install or symlink `bin/brain` into your PATH, then use:

```bash
brain setup --domain ai-brain-stack --path /home/mike/projects/ai-brain-stack
# If the project directory does not exist yet:
brain setup --domain new-project --path /home/mike/projects/new-project --create-project-dir
brain projects
brain next
brain ทำต่อ
brain codex
brain claude
brain audit
brain status
brain loop run --domain ai-brain-stack --project /home/mike/projects/ai-brain-stack --once
brain init-domain --domain new-project --path /home/mike/projects/new-project --active
brain run-log add --domain ai-brain-stack --summary "Finished audit" --cost 0.25 --tokens 1200
brain run-log summary
brain budget set --monthly-usd 20 --notes "MVP cap"
brain budget status
brain triage --domain ai-brain-stack
brain risk-scan --domain robbaan --project /home/mike/projects/robbaan
brain approval-pack --domain robbaan --project /home/mike/projects/robbaan --task "admin listing row"
```

By default the shortcut reads:

```bash
$HOME/ai-brain
```

Override the default brain root with either:

```bash
AI_BRAIN_ROOT=/home/mike/ai-brain brain projects
BRAIN_ROOT=/home/mike/ai-brain brain projects
```

Or pass an explicit root:

```bash
brain --root /home/mike/ai-brain projects
```

## Safety

`projects`, `status`, `triage`, and `risk-scan` are read/report oriented. `approval-pack --output artifacts` writes only under the AI Brain artifacts folder, not the target project.

`loop run --once` runs one safe L1 loop step: audit, triage, risk scan, and run-log entry. It does not edit target project files.

For day-to-day use, prefer `brain next` or `brain ทำต่อ`. Those shortcuts read the first active project from `ACTIVE.md` so you do not have to type `--domain` and `--project` every time.

For the day-to-day `ทำต่อ` workflow, see `docs/daily-usage.md`.
