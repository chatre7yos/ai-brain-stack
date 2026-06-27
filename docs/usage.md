# AI Brain CLI Usage

## Local shortcut

Install or symlink `bin/brain` into your PATH, then use:

```bash
brain projects
brain audit
brain status
brain init-domain --domain new-project --path /home/mike/projects/new-project --active
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
