# Issue Triage Bot

A small automation that runs inside GitHub Actions (no external server needed) and does two things on any repo it's installed in:

1. **Auto-labels new issues.** When an issue is opened or edited, a keyword/heuristic classifier (`bot/classifier.py`) reads the title and body and applies labels — `bug`, `enhancement`, `question`, `documentation`, `security`, plus a `priority: high` flag for urgent-sounding reports. If nothing matches, it falls back to `needs-triage` so nothing slips through unlabeled. It also leaves a short comment confirming what was applied.
2. **Posts commit notifications.** On every push, it summarizes the commits (author, short SHA, message) and posts them to a Discord webhook, so the team has a live feed of what shipped without watching the repo directly.

## Architecture

- `bot/classifier.py` — pure, dependency-free classification logic.
- `bot/github_client.py` — GitHub REST API wrapper using the Actions-provided `GITHUB_TOKEN`.
- `bot/label_issue.py` — issue-event entry point.
- `bot/notify_commits.py` — push-event notification entry point.
- `.github/workflows/triage.yml` — event triggers with minimal permissions.
- `tests/test_classifier.py` — unit tests for the classifier.

## Setup

1. Copy this repo's contents into your project (or fork it).
2. In **Settings → Secrets and variables → Actions**, add `DISCORD_WEBHOOK_URL` if you want commit notifications. `GITHUB_TOKEN` is provided automatically by Actions.
3. Push. Open a test issue with the word `bug` or `crash` and watch it get labeled.

## Scale / notes

This runs on GitHub's shared Actions runners, triggered per event, so there is no dedicated infrastructure to manage. It can handle a low-traffic personal repository or a busier repository through GitHub's event queueing and workflow execution.

## What I learned

Keeping the classifier pure and dependency-free made it easy to unit test. Idempotent label creation matters because a fresh repository may not have the labels yet. Graceful handling of missing optional secrets also prevents forks or contributor workflows from failing unnecessarily.
