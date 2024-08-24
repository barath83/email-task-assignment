from datetime import datetime
import traceback

from gmail_service.authenticate import authenticate
from gmail_service.utils import list_all_emails, get_email_by_id
from email_processor.constants import COMMON_MAIL_LABELS
from email_processor.save_email import save_emails
from db.email import Session, Email

def fetch_emails(creds, session):

    """
        Function to fetch all emails available from the account
        
        Params:
            - creds : credentials from authentication function call
    """
    messages = list_all_emails(creds)
    email_list = []
    
    if not messages:
        print("No messages found.")
    else:
        print(f"Found {len(messages)} messages. Printing email details...\n")
        
        try:
            for message in messages:
                message_id = message['id']
                email_details = get_email_by_id(creds, message_id)

                # Extract relevant parts from the email details
                headers = email_details['payload']['headers']
                subject = next(header['value'] for header in headers if header['name'] == 'Subject')
                sender = next(header['value'] for header in headers if header['name'] == 'From')
                recipient = next(header['value'] for header in headers if header['name'] == 'To')
                received_date_str = next(header['value'] for header in headers if header['name'] == 'Date')
                body_snippet = email_details.get('snippet', '')
                labels = email_details.get('labelIds', [])
                read_status = 'read' if 'UNREAD' not in labels else 'unread'

                # date
                date_format = '%a, %d %b %Y %H:%M:%S %z'
                date_object = datetime.strptime(received_date_str, date_format)

                # Determine the label
                label = next((l for l in labels if l in COMMON_MAIL_LABELS), None)

                email_data = dict (
                    message_id = message_id,
                    subject = subject,
                    sender = sender,
                    recipient = recipient,
                    body = body_snippet,
                    label = label,
                    received_date= date_object,
                    read_status = read_status
                )

                email_list.append(email_data)

            print(email_list)
            # Save the email records in DB and commit
            ingested_count = save_emails(session, email_list, Email)
            saved_emails = session.query(Email).all()
            session.commit()

            if ingested_count == len(email_list):
                print("All emails have been saved to DB successfully")
                return True
            else:
                return False

        except Exception as e:
            print(traceback.format_exc())
            return False


if __name__ == "__main__":
    # Authenticate and obtain the Gmail service
    creds = authenticate()  

    # Create a DB session to store data
    session = Session()

    fetch_emails(creds, session)
