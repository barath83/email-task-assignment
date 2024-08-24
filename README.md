## Installation

### Prerequisites

- **Python 3.x:** Ensure Python is installed on your machine.
- **Pip:** Make sure you have `pip` installed for managing Python packages.

### Clone the Repository

1. **Clone the repository**:
   ```bash
   git clone https://github.com/barath83/email-task-assignment.git
2. **Navigate to the project directory**:
   ```bash
   cd email-task-assignment
3. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt


### Setting up Google API Service and Credentials

1. Go to Google Cloud Console - [Here](https://console.cloud.google.com/)
2. Create a new project
3. Once a project is created, go to **API&Services** Section on the left side pane of your project
4. Select **Gmail service** and enable it
5. Again select **OAuth screen content** from the left pane and proceed to creating credentials
6. Select **OAuth Client ID** as type and on the next screen chose **Desktop App** as application type
7. Either publish the app in public mode with your domain and other details or you can use the credentials with a testing account as well
8. Once the OAuth client id is created, click on the download icon and store the file in **gmail_service/creds.json** path of the project
9. Run the file authenticate.py using the command
    ```bash
    python gmail_service/authenticate.py
10. This will open your browser and prompt the authentication confirmation, once done **gmail_service/token.json** which will be used from now on based on it's expiry limit


### Running scripts 

+ Fetching emails from Gmail and storing in local DB 
  ```bash
  python email_processor/fetch_store_emails.py

+ Apply rules and modify the emails in Gmail account and in local DB
  ```bash
  python email_processor/process_emails.py

These two scripts will run and execute the features that is required for the application, first command will run and fetch all the emails from the Gmail account and store them in local and the second command will iterate over each rule over each email and will check, apply the rules as per the conditions both in gmail account and in local DB
