import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "bot"))
from classifier import classify

def test_bug_report(): assert "bug" in classify("App crashes on login", "Getting a stack trace every time I click submit.").labels
def test_feature_request(): assert "enhancement" in classify("Please add dark mode", "Would be nice to support a dark theme.").labels
def test_question(): assert "question" in classify("How do I configure the webhook?", "").labels
def test_docs_issue(): assert "documentation" in classify("README has a typo", "The install section is unclear.").labels
def test_security_issue(): assert "security" in classify("Potential SQL injection", "Found a vulnerability in the login form.").labels
def test_priority_flag_added_alongside_type_label():
    r = classify("URGENT: production down", "Critical bug, data loss occurring.")
    assert "priority: high" in r.labels and "bug" in r.labels
def test_fallback_needs_triage(): assert classify("hey", "just saying hi").labels == ["needs-triage"]
def test_multiple_labels_possible():
    r = classify("Bug: docs example is broken", "The README example throws an error.")
    assert "bug" in r.labels and "documentation" in r.labels
