## Flask Feedback 
An application that allows users to manage their personal accounts, provide feedback, and view their feedback history. It features account-specific access to ensure that users can only modify their own feedback. This application provides a practical implementation of user authentication and access control using Python, Flask, SQLAlchemy.

## **Part 0: Set up your environment**
 To set it up locally, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/Pike1868/flask_auth_feedback.git
   ```
2. Create and activate a virtual environment:
   ```
   cd into_your_project_directory
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the requirements:
   ```
   pip install -r requirements.txt
   ```
4. Create the database:
   ```
   createdb your_database_name
   ```
5. Run the application:
   ```
   flask run
   ```
## **Part 1: Create User Model**

Create a ***User*** model for SQLAlchemy with the following columns:

- ***username*** - a unique primary key that is no longer than 20 characters.
- ***password*** - a not-nullable column that is text
- ***email*** - a not-nullable column that is unique and no longer than 50 characters.
- ***first_name*** - a not-nullable column that is no longer than 30 characters.
- ***last_name*** - a not-nullable column that is no longer than 30 characters.

## **Part 2: Make a Base Template**

Add a base template with slots for the page title and content. Other templates will extend from this. Bootstrap included in base template.