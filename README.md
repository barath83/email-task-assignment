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


*** Rules explained

```json

[
    {
        "id": 1,
        "case": "rule_1",
        "rule_level_predicate": "all",
        "pre_requisites": [
            {"field":"sender", "predicate": "contains", "value": "barath"},
            {"field":"subject", "predicate": "contains", "value": "Interview"},
            {"field":"read_status", "predicate": "equals", "value": "unread"},
            {"field":"received_date", "predicate": "less_than_days", "value": "2"}
        ],
        "actions": [
            {"action": "move_label", "value": "inbox"},
            {"action": "change_read_status", "value": "read"}
        ]
    },
    {
        "id": 2,
        "case": "rule_2",
        "rule_level_predicate": "any",
        "pre_requisites": [
            {"field":"sender", "predicate": "contains", "value": "hdfc_sales@gmail.com"},
            {"field":"body", "predicate": "contains", "value": "credit card"},
            {"field":"received_date", "predicate": "greater_than_days", "value": "5"}
        ],
        "actions": [
            {"action": "move_label", "value": "trash"},
            {"action": "change_read_status", "value": "unread"}
        ]
    },
    {
        "id": 3,
        "case": "rule_3",
        "rule_level_predicate": "all",
        "pre_requisites": [
            {"field":"subject", "predicate": "equals", "value": "Test"},
            {"field":"body", "predicate": "does_not_contain", "value": "test email"}
        ],
        "actions": [
            {"action": "move_label", "value": "important"},
            {"action": "change_read_status", "value": "read"}
        ]
    },
    {
        "id": 4,
        "case": "rule_4",
        "rule_level_predicate": "any",
        "pre_requisites": [
            {"field":"subject", "predicate": "equals", "value": "Summer Sale"},
            {"field":"sender", "predicate": "equals", "value": "test-shopping@gmail.com"},
            {"field":"received_date", "predicate": "greater_than_days", "value": "10"}
        ],
        "actions": [
            {"action": "move_label", "value": "spam"},
            {"action": "change_read_status", "value": "read"}
        ]
    }
]
```

Here have ensured that atleast each email tested in the example video will pass exactly one rule here and the corresponding actions will be applied on the same 

+ `rule_level_predicate`
  + Ensures what is the overall ruling that has to be checked for an email
  + Values - `all or any`
  + `all` - means that all conditions under **pre_requisites** must pass for the rule to pass
  + `any` - means that atleast one condition under **pre_requisites** must pass for the rule to pass

+ `pre_requisites`
   + Bunch of condition that each rule has
   + Each condtion has three parts - `field, predicate, value`
   + `field` - the field of attribute on which the condition is checked upon like the actual attributes of an email
   + `predicate` - the condtion criteria that the field will be tested on
   + `value` - the value to which the field has to match to for the respective field

+ `actions`
   + Each action with multiple action objects
   + 
