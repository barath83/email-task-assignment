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
8. Once the OAuth client id is created, click on the download icon and store the **credentials.json** file
