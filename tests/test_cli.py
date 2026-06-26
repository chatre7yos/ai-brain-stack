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


if __name__ == "__main__":
    unittest.main()
