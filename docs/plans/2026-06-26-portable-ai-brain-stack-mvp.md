# Portable AI Brain Stack MVP Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Build a portable Markdown-first AI Brain stack that Hermes, Claude Code, Codex, n8n, GitHub Actions, and local scripts can all use.

**Architecture:** A small Python stdlib CLI (`brain`) manages a repo/folder of Markdown files: global worklog, artifact folders, and per-domain loop/state/backlog/timeline files. The MVP is local-first, Git-friendly, no DB, no secrets, and L1/report-only by default.

**Tech Stack:** Python 3.11 stdlib, `unittest`, Markdown/YAML-like frontmatter, shell wrapper.

---

## Scope for first slice

Build Version 1 only:

- Create reusable folder skeleton.
- Add Markdown templates for loop contracts and state.
- Add CLI commands: `init`, `status`, `log`, `signal add`, `task add`, `triage`.
- Add tests for all core commands.
- Verify with real commands against a temporary brain folder.

Deferred:

- SQLite index.
- Dashboard.
- Background cron jobs.
- Any auto-fix / auto-commit logic.
- Connectors to GitHub/n8n/Obsidian.

---

### Task 1: Create project shell and failing CLI tests

**Objective:** Establish project files and RED tests for the intended behavior.

**Files:**
- Create: `pyproject.toml`
- Create: `brain/__init__.py`
- Create: `brain/cli.py`
- Create: `tests/test_cli.py`

**Step 1: Write failing tests**

Tests cover:
- `init` creates global folders/files and requested domains.
- `log` appends to `worklog.md`.
- `signal add` creates a signal artifact with frontmatter.
- `task add` creates a task artifact with frontmatter.
- `status` prints domains and open artifacts.
- `triage` prints a concise report and never modifies files.

**Step 2: Run tests to verify failure**

Run:

```bash
cd /home/mike/projects/ai-brain-stack
python3 -m unittest discover -s tests -v
```

Expected: FAIL because implementation is not present.

---

### Task 2: Implement minimal CLI

**Objective:** Make the RED tests pass with stdlib-only code.

**Files:**
- Modify: `brain/cli.py`
- Modify: `pyproject.toml`

**Commands:**

```bash
python3 -m brain.cli --root /tmp/demo-brain init --domains robbaan kliktan video-os
python3 -m brain.cli --root /tmp/demo-brain log --domain robbaan --message "Initialized Robbaan L1 loop"
python3 -m brain.cli --root /tmp/demo-brain signal add --domain video-os --title "Trend signal" --body "Thai AI tools topic rising" --priority medium --source manual
python3 -m brain.cli --root /tmp/demo-brain task add --domain robbaan --title "Verify checkout pending" --body "Check operator flow" --priority high
python3 -m brain.cli --root /tmp/demo-brain status
python3 -m brain.cli --root /tmp/demo-brain triage --domain robbaan
```

Expected: commands exit 0 and write Markdown files under `/tmp/demo-brain` only.

---

### Task 3: Add templates and docs

**Objective:** Make the stack understandable outside Hermes.

**Files:**
- Create: `README.md`
- Create: `templates/LOOP.md`
- Create: `templates/STATE.md`
- Create: `templates/signal.md`
- Create: `templates/task.md`

**Verification:**

Run:

```bash
python3 -m unittest discover -s tests -v
python3 -m brain.cli --help
```

Expected: tests pass and help text documents commands.

---

### Task 4: Verify demo brain artifact

**Objective:** Prove this is usable as a portable stack.

**Commands:**

```bash
rm -rf /tmp/mike7-ai-brain-demo
python3 -m brain.cli --root /tmp/mike7-ai-brain-demo init --domains robbaan kliktan autopost-hub video-os ai-workforce-os
python3 -m brain.cli --root /tmp/mike7-ai-brain-demo log --domain system --message "Brain stack demo initialized"
python3 -m brain.cli --root /tmp/mike7-ai-brain-demo signal add --domain video-os --title "Loop Engineering source reviewed" --body "Use L1 report-only before auto-actions" --priority high --source youtube+github
python3 -m brain.cli --root /tmp/mike7-ai-brain-demo task add --domain robbaan --title "Define Robbaan LOOP.md" --body "Lock allowed/denied actions before automation" --priority high
python3 -m brain.cli --root /tmp/mike7-ai-brain-demo status
python3 -m brain.cli --root /tmp/mike7-ai-brain-demo triage --domain robbaan
```

Expected: real output lists domains, artifacts, and a triage report.

---

### Task 5: Commit initial MVP

**Objective:** Save a clean checkpoint.

**Commands:**

```bash
git init
python3 -m unittest discover -s tests -v
git add .
git commit -m "feat: add portable ai brain stack mvp"
```

Expected: commit succeeds after tests pass.
