import json
import os
import sys
from classifier import classify
from github_client import GitHubClient

LABEL_COLORS = {"bug":"d73a4a","enhancement":"a2eeef","question":"d876e3","documentation":"0075ca","security":"b60205","priority: high":"e11d21","needs-triage":"ededed"}

def main() -> int:
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        print("GITHUB_EVENT_PATH not set — are you running inside Actions?", file=sys.stderr); return 1
    with open(event_path) as f: event = json.load(f)
    issue = event["issue"]; number = issue["number"]; title = issue.get("title", ""); body = issue.get("body", "") or ""
    result = classify(title, body)
    print(f"Issue #{number}: matched labels -> {result.labels}")
    client = GitHubClient()
    client.ensure_labels_exist({name: LABEL_COLORS.get(name, "cfd3d7") for name in result.labels})
    client.add_labels(number, result.labels)
    comment_lines = ["**Auto-triage**", "", f"Applied labels: {', '.join(result.labels)}"]
    if "needs-triage" not in result.labels: comment_lines.append("\nA maintainer will follow up. Thanks for the report!")
    client.comment(number, "\n".join(comment_lines)); return 0

if __name__ == "__main__": raise SystemExit(main())
