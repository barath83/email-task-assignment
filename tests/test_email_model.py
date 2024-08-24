import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.test_email import Base, TestEmail
import uuid

# Fixture to set up the test database session
@pytest.fixture(scope="module")
def test_db():
    DATABASE_URL = "sqlite:///test_emails.db" 
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)  # Ensure the schema is created
    Session = sessionmaker(bind=engine)
    session = Session()

    # Yield the session to be used by tests
    yield session

    # Cleanup: delete all records after tests
    session.query(TestEmail).delete()  # Delete all records from the TestEmail table
    session.commit()

    session.close()
    engine.dispose()  # Dispose the engine to clean up resources

@pytest.fixture
def new_email():
    return TestEmail(
        message_id=str(uuid.uuid4()),  # Ensure a unique message ID
        sender="sender@example.com",
        recipient="recipient@example.com",
        subject="Test Subject",
        body="This is a test email body.",
    )

def test_save_email(test_db, new_email):
    # Add the new email to the database session
    test_db.add(new_email)
    test_db.commit()

    # Query the email back to assert it was saved
    saved_email = test_db.query(TestEmail).filter_by(message_id=new_email.message_id).first()

    # Assert that the email was saved correctly
    assert saved_email is not None
    assert saved_email.sender == "sender@example.com"
    assert saved_email.recipient == "recipient@example.com"
    assert saved_email.subject == "Test Subject"
    assert saved_email.body == "This is a test email body."
