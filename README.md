# AI Issue Triage Bot

An automated GitHub Actions workflow for issue triage and commit notifications.

## What it does

- Classifies new or edited GitHub issues using keyword/heuristic rules.
- Applies labels including `bug`, `enhancement`, `question`, `documentation`, `security`, `priority: high`, and `needs-triage`.
- Creates missing labels automatically and posts a short triage comment.
- Summarizes push commits and optionally posts them to a Discord webhook.
- Runs entirely through GitHub Actions, with no external server required.

## Architecture

- `bot/classifier.py`: pure, dependency-free classification logic.
- `bot/github_client.py`: thin GitHub REST API wrapper using the Actions token.
- `bot/label_issue.py`: issue-event entry point.
- `bot/notify_commits.py`: push-event notification entry point.
- `.github/workflows/triage.yml`: event triggers and minimal permissions.
- `tests/test_classifier.py`: unit tests for classification behavior.

## Setup

Add `DISCORD_WEBHOOK_URL` as an Actions secret if Discord notifications are required. GitHub provides `GITHUB_TOKEN` automatically.

## Scale and lessons

The automation is event-driven on GitHub Actions shared runners, so it requires no server to operate. The design emphasizes pure/testable classification logic, idempotent label creation, minimal permissions, secure secrets, and graceful behavior when optional secrets are unavailable.

> Note: This repository demonstrates a production-ready automation pattern. Any claim that it is currently used in a business production environment should be based on the actual deployment history of the project.
