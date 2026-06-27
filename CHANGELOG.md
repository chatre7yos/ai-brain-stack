# Changelog

All notable changes to AI Brain Stack will be documented in this file.

## v0.1.0 — First usable MVP

Initial public/local MVP for using AI Brain Stack as a small control layer before AI agents touch code.

### Added

- Local brain bootstrap with `brain setup`.
- Existing-project validation plus `--create-project-dir` for first-run setup.
- Safe L1 daily loop with `brain next` and Thai alias `brain ทำต่อ`.
- Explicit one-step loop runner with `brain loop run --once`.
- Active project discovery with `brain projects`.
- Brain health checks with `brain audit`.
- Domain triage with `brain triage`.
- Git diff scope guard with `brain risk-scan`.
- Approval package drafting with `brain approval-pack` before L2 implementation.
- Run logging and budget tracking with `brain run-log` and `brain budget`.
- Ready-to-copy agent handoff commands with `brain codex` and `brain claude`.
- JSON output for automation-friendly commands.
- Starter templates for `LOOP.md`, `STATE.md`, tasks, signals, and out-of-scope rules.
- Public docs for quickstart, command boundaries, daily usage, agent examples, and repo navigation.
- `CONTEXT.md` shared vocabulary for agents and contributors.
- `AGENTS.md` guardrails for agent/contributor work.
- `grill-with-docs` pattern and skill adaptation for sharpening fuzzy plans before implementation.
- GitHub Actions test workflow for Python 3.11 and 3.12.

### Safety posture

- L1/report-only flows do not edit target project files.
- No commit, push, deploy, service start, tunnel, secrets, DB, or external write by default.
- Private brain roots such as `~/ai-brain` remain outside the public tool repo.

### Verification

- Local test suite: `python3 -m unittest discover -s tests -v`.
- Setup smoke: `brain setup ... --create-project-dir` followed by `brain next`.
- GitHub Actions tests pass on Python 3.11 and 3.12.
