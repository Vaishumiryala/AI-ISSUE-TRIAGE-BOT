from __future__ import annotations
import os
import requests

GITHUB_API = "https://api.github.com"

class GitHubClient:
    def __init__(self, token: str | None = None, repo: str | None = None):
        self.token = token or os.environ["GITHUB_TOKEN"]
        self.repo = repo or os.environ["GITHUB_REPOSITORY"]
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.token}", "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"})
    def add_labels(self, issue_number: int, labels: list[str]) -> requests.Response:
        resp = self.session.post(f"{GITHUB_API}/repos/{self.repo}/issues/{issue_number}/labels", json={"labels": labels})
        resp.raise_for_status(); return resp
    def comment(self, issue_number: int, body: str) -> requests.Response:
        resp = self.session.post(f"{GITHUB_API}/repos/{self.repo}/issues/{issue_number}/comments", json={"body": body})
        resp.raise_for_status(); return resp
    def ensure_labels_exist(self, labels: dict[str, str]) -> None:
        url = f"{GITHUB_API}/repos/{self.repo}/labels"
        existing = {l["name"] for l in self.session.get(url).json()}
        for name, color in labels.items():
            if name not in existing:
                self.session.post(url, json={"name": name, "color": color})
