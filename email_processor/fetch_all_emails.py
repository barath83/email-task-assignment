from db.email import Session, Email

def fetch_all_emails(session):
    """
    Fetch all email records from the database and return them as a list of dictionaries.
    
    Args:
        session: The SQLAlchemy session to query the database.
    
    Returns:
        List[Dict]: A list of dictionaries representing each email record.
    """
    emails = session.query(Email).all()
    email_list = []

    for email in emails:
        email_dict = {
            "id": email.id,
            "message_id": email.message_id,
            "sender": email.sender,
            "recipient": email.recipient,
            "subject": email.subject,
            "body": email.body,
            "received_date": email.received_date.strftime('%Y-%m-%d %H:%M:%S') if email.received_date else None,
            "read_status": email.read_status,
            "label": email.label
        }
        email_list.append(email_dict)

    print("All the emails fetched from DB ------------")
    print(email_list)

    return email_list

if __name__ == "__main__":

    # Create a DB session to store data
    session = Session()

    fetch_all_emails(session)