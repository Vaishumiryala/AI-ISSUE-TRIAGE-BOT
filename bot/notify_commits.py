import json
import os
import sys
import requests

def build_message(event: dict) -> str:
    pusher = event.get("pusher", {}).get("name", "someone")
    repo = event.get("repository", {}).get("full_name", "the repo")
    commits = event.get("commits", [])
    if not commits: return f"{pusher} pushed to {repo} (no new commits — likely a tag or branch delete)."
    lines = [f"**{pusher}** pushed {len(commits)} commit(s) to `{repo}`:"]
    for c in commits[:10]:
        lines.append(f"- `{c['id'][:7]}` {c['message'].splitlines()[0]} ({c['author']['name']})")
    if len(commits) > 10: lines.append(f"...and {len(commits) - 10} more.")
    return "\n".join(lines)

def main() -> int:
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL"); event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        print("GITHUB_EVENT_PATH not set — are you running inside Actions?", file=sys.stderr); return 1
    with open(event_path) as f: event = json.load(f)
    message = build_message(event); print(message)
    if not webhook_url:
        print("DISCORD_WEBHOOK_URL not set — skipping webhook post (this is fine for forks/PRs)."); return 0
    resp = requests.post(webhook_url, json={"content": message}); resp.raise_for_status(); return 0

if __name__ == "__main__": raise SystemExit(main())
