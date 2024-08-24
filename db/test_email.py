from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean 
)

Base = declarative_base()

class TestEmail(Base):
    
    __tablename__ = "test_emails"
    id = Column(Integer, primary_key=True)  
    message_id = Column(String, unique=True)
    sender = Column(String)
    recipient = Column(String)
    subject = Column(String)
    body = Column(Text)
    received_date = Column(DateTime)
    read_status = Column(String, default="unread")
    label = Column(String, default="inbox")
    is_test = Column(Boolean, default=False)
