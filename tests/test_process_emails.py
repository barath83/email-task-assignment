import pytest
from datetime import datetime, timedelta
from db.test_email import TestEmail
from email_processor.process_emails import check_predicate, evaluate_predicate, check_rule

# Mock function to simulate Gmail API
def mock_get_label_id(service, label_name):
    return "LABEL_ID" if label_name == "inbox" else None

@pytest.fixture
def mock_email():
    return TestEmail(
        message_id="test_message_id",
        sender="sender@example.com",
        recipient="recipient@example.com",
        subject="Test Subject",
        body="This is a test email body.",
        received_date=datetime.now() - timedelta(days=10),
        label="inbox",
        read_status="unread"
    )

@pytest.fixture
def mock_rules():
    return [
        {
            "id": "1",
            "pre_requisites": [
                {"field": "subject", "predicate": "contains", "value": "Test"},
                {"field": "received_date", "predicate": "less_than_days", "value": "30"}
            ],
            "rule_level_predicate": "all",
            "actions": [
                {"action": "move_label", "value": "inbox"},
                {"action": "change_read_status", "value": "read"}
            ]
        }
    ]

# Test for check_predicate
def test_check_predicate(mock_email):
    condition = {"field": "subject", "predicate": "contains", "value": "Test"}
    assert check_predicate(mock_email, condition) == True

    condition = {"field": "subject", "predicate": "does_not_contain", "value": "Hello"}
    assert check_predicate(mock_email, condition) == True

# Test for evaluate_predicate
def test_evaluate_predicate():
    assert evaluate_predicate("Test Subject", "contains", "Test") == True
    assert evaluate_predicate("Test Subject", "does_not_contain", "Hello") == True
    assert evaluate_predicate(datetime.now() - timedelta(days=10), "less_than_days", "30") == True

# Test for check_rule
def test_check_rule(mock_email, mock_rules):
    rule = mock_rules[0]
    assert check_rule(mock_email, rule) == True