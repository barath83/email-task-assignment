import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.email import Base, Email
from email_processor.fetch_store_emails import fetch_emails
from gmail_service.authenticate import authenticate

DATABASE_URL = "sqlite:///test_emails.db"  # Use a separate test database

@pytest.fixture(scope='function')
def test_db():
    # Create engine for test database
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture
def session(test_db):
    Session = sessionmaker(bind=test_db)
    session = Session()
    yield session
    session.close()

def test_fetch_emails(session):
    # Mock or set up credentials as needed
    creds = authenticate()
    
    # Fetch emails and check result
    result = fetch_emails(creds, session)
    
    # Verify that fetch_emails returned True
    assert result is True, "fetch_emails should return True if successful"
    
    # Verify that the email was saved in the database
    saved_emails = session.query(Email).all()
    assert len(saved_emails) > 0, "No emails found in the database"
    
    # Further assertions to check the content of the saved emails
    for email in saved_emails:
        assert email.subject is not None, "Email subject should not be None"
        assert email.sender is not None, "Email sender should not be None"
        assert email.recipient is not None, "Email recipient should not be None"
        assert email.received_date is not None, "Email received_date should not be None"
        assert email.body is not None, "Email body should not be None"
