import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from brain.cli import main


class BrainCliTests(unittest.TestCase):
    def run_cli(self, root: Path, *args: str) -> str:
        buf = io.StringIO()
        with redirect_stdout(buf):
            main(["--root", str(root), *args])
        return buf.getvalue()

    def test_init_creates_skeleton_for_domains(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out = self.run_cli(root, "init", "--domains", "robbaan", "video-os")
            self.assertIn("Initialized AI Brain", out)
            self.assertTrue((root / "worklog.md").exists())
            self.assertTrue((root / "inbox.md").exists())
            for folder in ["signals", "tasks", "decisions", "bugs", "research", "content-ideas"]:
                self.assertTrue((root / "artifacts" / folder).is_dir())
            for domain in ["robbaan", "video-os"]:
                for name in ["LOOP.md", "STATE.md", "backlog.md", "timeline.md"]:
                    self.assertTrue((root / "domains" / domain / name).exists())

    def test_log_appends_worklog_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.run_cli(root, "init", "--domains", "robbaan")
            self.run_cli(root, "log", "--domain", "robbaan", "--message", "Checked state")
            text = (root / "worklog.md").read_text(encoding="utf-8")
            self.assertIn("Domain: robbaan", text)
            self.assertIn("Checked state", text)

    def test_signal_add_creates_markdown_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.run_cli(root, "init", "--domains", "video-os")
            out = self.run_cli(root, "signal", "add", "--domain", "video-os", "--title", "Loop source reviewed", "--body", "Start L1", "--priority", "high", "--source", "youtube")
            self.assertIn("Created signal", out)
            files = list((root / "artifacts" / "signals").glob("*.md"))
            self.assertEqual(1, len(files))
            text = files[0].read_text(encoding="utf-8")
            self.assertIn("type: signal", text)
            self.assertIn("domain: video-os", text)
            self.assertIn("priority: high", text)
            self.assertIn("# Loop source reviewed", text)

    def test_task_add_creates_markdown_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.run_cli(root, "init", "--domains", "robbaan")
            out = self.run_cli(root, "task", "add", "--domain", "robbaan", "--title", "Define LOOP", "--body", "Write contract", "--priority", "medium")
            self.assertIn("Created task", out)
            files = list((root / "artifacts" / "tasks").glob("*.md"))
            self.assertEqual(1, len(files))
            text = files[0].read_text(encoding="utf-8")
            self.assertIn("type: task", text)
            self.assertIn("status: open", text)
            self.assertIn("# Define LOOP", text)

    def test_status_lists_domains_and_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.run_cli(root, "init", "--domains", "robbaan", "kliktan")
            self.run_cli(root, "signal", "add", "--domain", "robbaan", "--title", "A", "--body", "B")
            out = self.run_cli(root, "status")
            self.assertIn("Domains: kliktan, robbaan", out)
            self.assertIn("signals: 1", out)
            self.assertIn("tasks: 0", out)

    def test_triage_prints_l1_report_without_creating_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.run_cli(root, "init", "--domains", "robbaan")
            self.run_cli(root, "task", "add", "--domain", "robbaan", "--title", "Verify checkout", "--body", "Check pending", "--priority", "high")
            before = sorted(str(p.relative_to(root)) for p in root.rglob("*"))
            out = self.run_cli(root, "triage", "--domain", "robbaan")
            after = sorted(str(p.relative_to(root)) for p in root.rglob("*"))
            self.assertEqual(before, after)
            self.assertIn("L1 Triage Report", out)
            self.assertIn("Verify checkout", out)
            self.assertIn("No auto-actions taken", out)

    def test_triage_does_not_list_done_tasks_as_open(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.run_cli(root, "init", "--domains", "robbaan")
            done_task = root / "artifacts" / "tasks" / "done-task.md"
            done_task.write_text("""---
type: task
domain: robbaan
priority: high
status: done
---

# Already closed
""", encoding="utf-8")
            open_task = root / "artifacts" / "tasks" / "open-task.md"
            open_task.write_text("""---
type: task
domain: robbaan
priority: high
status: open
---

# Still open
""", encoding="utf-8")
            out = self.run_cli(root, "triage", "--domain", "robbaan")
            self.assertIn("Still open", out)
            self.assertNotIn("Already closed", out)

    def test_risk_scan_flags_project_diff_against_denied_actions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            project.mkdir()
            self.run_cli(root, "init", "--domains", "robbaan")
            (root / "domains" / "robbaan" / "LOOP.md").write_text("""# Robbaan Loop

## Denied Actions
- No database schema/data changes.
- No package model changes.
- No public tunnel or external write.
""", encoding="utf-8")
            out = self.run_cli(root, "risk-scan", "--domain", "robbaan", "--project", str(project), "--diff", "diff --git a/db/schema.ts b/db/schema.ts\n+ package table change")
            self.assertIn("# Risk Scan — robbaan", out)
            self.assertIn("Risk Level: high", out)
            self.assertIn("database schema/data", out)
            self.assertIn("No project files modified", out)

    def test_approval_pack_prints_package_without_writing_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            project.mkdir()
            self.run_cli(root, "init", "--domains", "robbaan")
            (root / "domains" / "robbaan" / "verify.md").write_text("""# Robbaan Verification Profile

## Recommended Future L2 Default Verification
```bash
npm test
npm run build
```

## DB / migration / write checks — require explicit approval
```bash
npm run db:migrate
```
""", encoding="utf-8")
            before = sorted(str(p.relative_to(project)) for p in project.rglob("*"))
            out = self.run_cli(root, "approval-pack", "--domain", "robbaan", "--project", str(project), "--task", "Small UI copy", "--test-output", "not run")
            after = sorted(str(p.relative_to(project)) for p in project.rglob("*"))
            self.assertEqual(before, after)
            self.assertIn("# L2 Approval Package — robbaan", out)
            self.assertIn("Small UI copy", out)
            self.assertIn("npm test", out)
            self.assertNotIn("db:migrate", out)
            self.assertIn("No auto-merge", out)
            self.assertIn("Mike approval required", out)

    def test_approval_pack_output_writes_artifact_without_writing_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            project.mkdir()
            self.run_cli(root, "init", "--domains", "robbaan")
            (root / "domains" / "robbaan" / "verify.md").write_text("""# Robbaan Verification Profile

## Recommended Future L2 Default Verification
```bash
npm test
npm run build
```
""", encoding="utf-8")
            before_project = sorted(str(p.relative_to(project)) for p in project.rglob("*"))
            out = self.run_cli(root, "approval-pack", "--domain", "robbaan", "--project", str(project), "--task", "Small UI copy", "--test-output", "not run", "--output", "artifacts")
            after_project = sorted(str(p.relative_to(project)) for p in project.rglob("*"))
            self.assertEqual(before_project, after_project)
            self.assertIn("Saved approval package:", out)
            files = list((root / "artifacts" / "approval-packs").glob("*.md"))
            self.assertEqual(1, len(files))
            text = files[0].read_text(encoding="utf-8")
            self.assertIn("type: approval-pack", text)
            self.assertIn("domain: robbaan", text)
            self.assertIn("Small UI copy", text)
            self.assertIn("No auto-merge", text)

    def test_triage_reads_domain_contract_state_backlog_and_timeline(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.run_cli(root, "init", "--domains", "robbaan")
            domain = root / "domains" / "robbaan"
            (domain / "LOOP.md").write_text("""# Robbaan Loop

## Goal
Protect Robbaan decisions.

## Denied Actions
- No package model changes.
- No member-admin feature creation.
""", encoding="utf-8")
            (domain / "STATE.md").write_text("""# Robbaan State

## Current Focus
- Preserve checkout pending flow.

## Blocked / Needs Mike
- Approve L2 pilot.

## Watch List
- Credit semantics must not drift.
""", encoding="utf-8")
            (domain / "backlog.md").write_text("""# Robbaan Backlog

## Next Safe L1 Actions
- [ ] Draft verification profile.
- [ ] Run read-only repo inspection.
""", encoding="utf-8")
            (domain / "timeline.md").write_text("""# Robbaan Timeline

## 2026-06-26T00:00:00Z
- Contract initialized.
""", encoding="utf-8")
            before = sorted(str(p.relative_to(root)) for p in root.rglob("*"))
            out = self.run_cli(root, "triage", "--domain", "robbaan")
            after = sorted(str(p.relative_to(root)) for p in root.rglob("*"))
            self.assertEqual(before, after)
            self.assertIn("## Goal", out)
            self.assertIn("Protect Robbaan decisions.", out)
            self.assertIn("## Current Focus", out)
            self.assertIn("Preserve checkout pending flow", out)
            self.assertIn("## Blocked / Needs Mike", out)
            self.assertIn("Approve L2 pilot", out)
            self.assertIn("## Watch List / Risks", out)
            self.assertIn("Credit semantics must not drift", out)
            self.assertIn("## Next Safe Actions", out)
            self.assertIn("Draft verification profile", out)
            self.assertIn("## Denied Actions", out)
            self.assertIn("No package model changes", out)
            self.assertIn("## Sources Read", out)
            self.assertIn("domains/robbaan/LOOP.md", out)
            self.assertIn("domains/robbaan/STATE.md", out)
    def test_projects_lists_active_domains_from_active_md(self):
        with tempfile.TemporaryDirectory() as tmp:
            import json

            root = Path(tmp)
            self.run_cli(root, "init", "--domains", "robbaan", "kliktan")
            (root / "ACTIVE.md").write_text("""# ACTIVE

## Active Domains

| Domain | Path / Scope | Status | Default next safe action |
|---|---|---|---|
| `robbaan` | `/home/mike/projects/robbaan` | L1-ready | Draft pilot. |
| `kliktan` | `/home/mike/projects/kliktan` | L1-ready | Viewport discovery. |

## Explicitly Not Active by Default
- NEXT only.
""", encoding="utf-8")
            out = self.run_cli(root, "projects")
            self.assertIn("# Active Projects", out)
            self.assertIn("robbaan", out)
            self.assertIn("/home/mike/projects/robbaan", out)
            self.assertIn("kliktan", out)
            data = json.loads(self.run_cli(root, "projects", "--json"))
            self.assertEqual(2, data["count"])
            self.assertEqual("robbaan", data["projects"][0]["domain"])
            self.assertEqual("Draft pilot.", data["projects"][0]["next_safe_action"])

    def test_machine_readable_json_outputs_for_loop_automation(self):
        with tempfile.TemporaryDirectory() as tmp:
            import json

            root = Path(tmp)
            project = root / "project"
            project.mkdir()
            self.run_cli(root, "init", "--domains", "robbaan")
            (root / "domains" / "robbaan" / "LOOP.md").write_text("""# Robbaan Loop

## Goal
Protect scope.

## Denied Actions
- No database schema/data changes.
""", encoding="utf-8")
            (root / "domains" / "robbaan" / "STATE.md").write_text("""# Robbaan State

## Current Focus
- L2-ready only.
""", encoding="utf-8")
            (root / "domains" / "robbaan" / "backlog.md").write_text("""# Robbaan Backlog

## Next Safe Actions
- [ ] Draft pilot.
""", encoding="utf-8")
            (root / "domains" / "robbaan" / "verify.md").write_text("""# Verify

## Recommended Future L2 Default Verification
```bash
npm test
```
""", encoding="utf-8")
            status = json.loads(self.run_cli(root, "status", "--json"))
            self.assertEqual(["robbaan"], status["domains"])
            self.assertIn("tasks", status["artifacts"])
            triage = json.loads(self.run_cli(root, "triage", "--domain", "robbaan", "--json"))
            self.assertEqual("robbaan", triage["domain"])
            self.assertIn("Protect scope.", triage["goal"])
            self.assertEqual([], triage["open_tasks"])
            risk = json.loads(self.run_cli(root, "risk-scan", "--domain", "robbaan", "--project", str(project), "--diff", "+ db/schema.ts", "--json"))
            self.assertEqual("high", risk["risk_level"])
            self.assertFalse(risk["project_write_safety"]["project_files_modified"])
            pack = json.loads(self.run_cli(root, "approval-pack", "--domain", "robbaan", "--project", str(project), "--task", "Pilot", "--test-output", "not run", "--json"))
            self.assertEqual("Pilot", pack["task"])
            self.assertIn("npm test", pack["verification_commands"])
            self.assertIn("Mike approval required.", pack["required_gates"])


if __name__ == "__main__":
    unittest.main()
