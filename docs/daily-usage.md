# Daily AI Brain Workflow

Use this when Mike says `ทำต่อ`, when starting a work session, or when handing work to another agent.

## Rule

Default focus comes from:

```bash
brain next
# or
brain ทำต่อ
# manual check
brain projects
```

Do not jump into product app code from memory. Read the active domain first.

## 1. Start-of-session check

```bash
brain projects
brain audit
```

Expected for a healthy brain:

```text
Active focus: ai-brain-stack
Missing domain files: 0
Missing verify profiles: 0
Missing project paths: 0
```

If `brain audit` reports warnings, fix the brain/tooling issue before product implementation unless Mike explicitly switches scope.

## 2. Read the active focus

```bash
brain triage --domain ai-brain-stack
```

This answers:

- current focus
- blockers / needs Mike
- risks / denied actions
- next safe actions
- sources read

## 3. Before touching any project repo

Run a risk scan for the intended domain/project:

```bash
brain risk-scan --domain <domain> --project <project-path>
```

If the scan reports high risk, stop and ask Mike.

## 3b. One-command L1 loop

When the domain and project path are clear, run one full safe L1 loop step:

```bash
brain next
# or
brain ทำต่อ
# explicit target
brain loop run --domain <domain> --project <project-path> --once
```

This performs audit, triage, risk scan, writes a run-log entry, and stops. It does not edit target project files.

## 4. Before implementation

Create an approval package first:

```bash
brain approval-pack \
  --domain <domain> \
  --project <project-path> \
  --task "<small task>"
```

Save it only when appropriate:

```bash
brain approval-pack \
  --domain <domain> \
  --project <project-path> \
  --task "<small task>" \
  --output artifacts
```

## 5. Adding a new project/domain

```bash
brain init-domain \
  --domain <domain> \
  --path /home/mike/projects/<project> \
  --status "L1-ready" \
  --next "Run read-only discovery." \
  --active
```

Then run:

```bash
brain audit
brain triage --domain <domain>
```

## 6. Current Mike7 safety default

While `ai-brain-stack` is the active focus:

- do not edit Robbaan app code
- do not run Robbaan tests/build/services
- do not deploy/publish/start tunnels
- do not touch DB/migrations/secrets

## 7. Useful JSON commands for automation

```bash
brain projects --json
brain audit --json
brain next --json
brain triage --domain ai-brain-stack --json
brain risk-scan --domain <domain> --project <project-path> --json
brain loop run --domain <domain> --project <project-path> --once --json
brain approval-pack --domain <domain> --project <project-path> --task "<task>" --json
brain run-log summary --json
brain budget status --json
```

## 8. Track run cost / budget

After a meaningful loop run, append a simple run-log entry:

```bash
brain run-log add \
  --domain ai-brain-stack \
  --summary "Finished brain audit" \
  --status success \
  --cost 0.25 \
  --tokens 1200
```

Summarize usage:

```bash
brain run-log summary
brain run-log summary --json
```

Set/check a lightweight budget:

```bash
brain budget set --monthly-usd 20 --notes "MVP cap"
brain budget status
brain budget status --json
```

## 9. Minimal `ทำต่อ` loop

```text
brain projects
→ pick first active project
→ brain audit
→ brain triage --domain <active>
→ do only next safe action
→ verify
→ brain run-log add --domain <active> --summary "<what happened>"
→ commit tool/brain changes separately
→ report evidence
```

Equivalent one-command L1 version:

```text
brain next
# or
brain ทำต่อ
# explicit target
brain loop run --domain <active> --project <project-path> --once
→ inspect status/risk/next
→ stop unless implementation is explicitly approved
```
