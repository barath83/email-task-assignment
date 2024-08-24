import requests

def list_all_emails(creds):
    """
        Function to fetch the details of all email records
    """
    headers = {
        'Authorization': f"Bearer {creds.token}",
        'Accept': 'application/json'
    }
    response = requests.get(
        'https://gmail.googleapis.com/gmail/v1/users/me/messages', 
        headers=headers)

    messages = response.json().get('messages', [])

    return messages

def get_email_by_id(creds, message_id):
    """
        Function to fetch the details of an email record
    """
    headers = {
        'Authorization': f"Bearer {creds.token}",
        'Accept': 'application/json'
    }
    msg_response = requests.get(
        f'https://gmail.googleapis.com/gmail/v1/users/me/messages/{message_id}', 
        headers=headers)

    msg = msg_response.json()

    return msg
