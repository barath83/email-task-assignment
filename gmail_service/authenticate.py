import os

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

CURRENT_BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# Define the scope that allows read and modify access to Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

CUR_TOKEN_PATH = os.path.join(CURRENT_BASE_PATH, "token.json")
CUR_CREDENTIALS_PATH = os.path.join(CURRENT_BASE_PATH, "google_creds.json")

def authenticate():
    
    creds = None
    
    # Check if token.json exists, which stores the user's access and refresh tokens
    if os.path.exists(CUR_TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(CUR_TOKEN_PATH, SCOPES)
    
    # If there are no (valid) credentials available, prompt the user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CUR_CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(CUR_TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
    
    return creds

if __name__ == "__main__":
    creds = authenticate()
    print("Authentication successful!")
