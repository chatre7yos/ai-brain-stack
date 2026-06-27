# Daily AI Brain Workflow

Use this when Mike says `ทำต่อ`, when starting a work session, or when handing work to another agent.

## Rule

Default focus comes from:

```bash
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
brain triage --domain ai-brain-stack --json
brain risk-scan --domain <domain> --project <project-path> --json
brain approval-pack --domain <domain> --project <project-path> --task "<task>" --json
```

## 8. Minimal `ทำต่อ` loop

```text
brain projects
→ pick first active project
→ brain audit
→ brain triage --domain <active>
→ do only next safe action
→ verify
→ commit tool/brain changes separately
→ report evidence
```
