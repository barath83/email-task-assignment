import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.test_email import Base, TestEmail
from email_processor.fetch_all_emails import fetch_all_emails

# Create a test database engine and session
DATABASE_URL = "sqlite:///test_emails.db" 
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@pytest.fixture(scope='function')
def setup_database():
    # Create tables in the test database
    Base.metadata.create_all(engine)
    session = Session()
    
    # Add some test data
    test_emails = [
        TestEmail(message_id="1", sender="test1@example.com", recipient="recipient@example.com", subject="Test Email 1", body="This is a test email 1",),
        TestEmail(message_id="2", sender="test2@example.com", recipient="recipient@example.com", subject="Test Email 2", body="This is a test email 2",)
    ]
    session.add_all(test_emails)
    session.commit()
    
    yield session

    # Cleanup: delete all records after tests
    session.query(TestEmail).delete() 
    session.commit()
    
    # Cleanup after each test
    session.close()
    Base.metadata.drop_all(engine)

def test_fetch_all_emails(setup_database):
    session = setup_database
    emails = session.query(TestEmail).all()
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
    
    # Check if the number of fetched emails is greater than 2
    assert len(email_list) >= 2

    # Check the details of the fetched emails
    for email in email_list:
        assert email["message_id"] in ["1", "2"]
        assert email["sender"] in ["test1@example.com", "test2@example.com"]
        assert email["recipient"] == "recipient@example.com"
        assert email["subject"] in ["Test Email 1", "Test Email 2"]
        assert email["body"] in ["This is a test email 1", "This is a test email 2"]
