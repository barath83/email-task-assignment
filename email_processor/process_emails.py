import sys
import os
import json
from datetime import datetime
import traceback

from googleapiclient.discovery import build

# appending project root dir to sys path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from gmail_service.authenticate import authenticate
from db.email import Session, Email

def evaluate_predicate(email_value, predicate, condition_value):
    """
    Evaluate a single pre-requisite condition based on the predicate.
    """
    if predicate == "contains":
        return condition_value in email_value
    elif predicate == "does_not_contain":
        return condition_value not in email_value
    elif predicate == "equals":
        return email_value == condition_value
    elif predicate == "not_equals":
        return email_value != condition_value
    elif predicate == "less_than_days":
        return (datetime.now() - email_value).days < int(condition_value)
    elif predicate == "greater_than_days":
        return (datetime.now() - email_value).days > int(condition_value)
    # Add more predicates as needed
    return False
    
def check_rule(email, rule):
    """
    Check if an email satisfies all or any of the rule's pre-requisites based on rule_level_predicate.
    """
    rule_level_predicate = rule["rule_level_predicate"]
    pre_requisites = rule["pre_requisites"]

    results = []
    for condition in pre_requisites:
        field = condition["field"]
        predicate = condition["predicate"]
        condition_value = condition["value"]
        email_value = getattr(email, field)  # Fetch the respective value from the email object
        
        results.append(evaluate_predicate(email_value, predicate, condition_value))

    if rule_level_predicate == "all":
        return all(results)
    elif rule_level_predicate == "any":
        return any(results)

    return False

def get_label_id(service, label_name):
    """
    Retrieves the label ID for a given label name.
    
    Args:
        service: The Gmail API service instance.
        label_name: The name of the label to retrieve the ID for.
    
    Returns:
        The label ID if found, otherwise None.
    """
    try:
        # Fetch all labels
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        # Search for the label with the given name
        for label in labels:
            if label['name'].lower() == label_name.lower():
                return label['id']
        
        print(f"Label '{label_name}' not found.")
        return None

    except Exception as e:
        print(f"Gmail API error occurred while fetching label ID: {e}")
        return None


def apply_rule_to_gmail_and_db(service, email, actions, session):
    """
    Apply actions to both the Gmail account and the SQLite database for the provided email object.
    
    Args:
        service: The Gmail API service instance.
        email: The email object retrieved from the database.
        actions: The list of actions to apply based on the rules.
        session: The SQLAlchemy session to update the database.
    
    Returns:
        bool: True if actions were successfully applied, False otherwise.
    """
    try:
        for action in actions:
            action_type = action["action"]
            value = action["value"]

            if action_type == "move_label":
                # Update label in Gmail
                label_id = get_label_id(service, value)
                if label_id:
                    service.users().messages().modify(
                        userId="me",
                        id=email.message_id,
                        body={"addLabelIds": [label_id]}
                    ).execute()

                # Update label in DB
                email.label = value

            elif action_type == "change_read_status":
                # Update read status in Gmail
                if value == "read":
                    service.users().messages().modify(
                        userId="me",
                        id=email.message_id,
                        body={"removeLabelIds": ["UNREAD"]}
                    ).execute()
                elif value == "unread":
                    service.users().messages().modify(
                        userId="me",
                        id=email.message_id,
                        body={"addLabelIds": ["UNREAD"]}
                    ).execute()

                # Update read status in DB
                email.read_status = value

        # Commit changes to the DB
        session.commit()
        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
        return False
    

def process_emails(creds, session):
    """
        Function that will fetch mails from DB and process them according to rules
    """

    service = build('gmail', 'v1', credentials=creds)

    # fetch rules 
    rules_file_path = os.path.join(current_dir, 'rules.json')
    with open(rules_file_path, "r") as file:
        rules = json.load(file)

    report = {
        "total_emails": 0,
        "emails_passed_rules": [],
        "rule_results": {}
    }


    try:
        emails = session.query(Email).all()
        report["total_emails"] = len(emails)

        for email in emails:
            email_results = {"email_id": email.id, "subject": email.subject, "passed_rules": []}

            for rule in rules:
                rule_id = rule["id"]
                if check_rule(email, rule):
                    email_results["passed_rules"].append(rule_id)
                    apply_rule_to_gmail_and_db(service, email, rule["actions"], session)

            if email_results["passed_rules"]:
                report["emails_passed_rules"].append(email.id)
            
            report["rule_results"][email.id] = email_results

        print("the report -------")
        print(report)

    except Exception as e:
        print("Error in process emails function")
        print(traceback.format_exc())
            


if __name__ == "__main__":
    # Authenticate and obtain the Gmail service
    creds = authenticate()

    # Create a DB session to store data
    session = Session()

    process_emails(creds, session)
