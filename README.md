
# Mentor Baba Quiz Application

## Project Overview
The Mentor Baba Quiz Application is a full-stack web application designed to provide an interactive quiz experience. It features user registration and login, dynamic question loading from an Excel file, a per-question timer, navigation capabilities, and a comprehensive score summary upon quiz submission. This project demonstrates a practical application of Python (Flask) for the backend, MySQL for database management, and standard web technologies (HTML, CSS, JavaScript) for the frontend.

## Features
- **User Authentication**: Secure user registration and login system.
- **Excel Question Upload**: Admins can easily upload quiz questions using an Excel file, allowing for flexible quiz content management.
- **Timed Questions**: Each question is presented with a 30-second timer to encourage quick thinking.
- **Question Navigation**: Users can navigate between questions using "Previous" and "Next" buttons, or jump directly to any question using a numbered navigation panel. Answered questions are visually marked.
- **Score Calculation**: Automatic calculation of the user's score upon quiz submission.
- **Result Summary**: Detailed breakdown of correct and incorrect answers after the quiz, along with the user's score.
- **Responsive Design**: The application is designed to be usable across various devices (desktop, tablet, mobile).

## Technologies Used
### Backend:
- **Python 3.x**: The core programming language.
- **Flask**: A micro web framework for building the API.
- **Flask-CORS**: For handling Cross-Origin Resource Sharing between frontend and backend.
- **MySQL Connector/Python**: To interact with the MySQL database.
- **Pandas**: For reading and processing Excel files.
- **Werkzeug**: For secure password hashing.

### Frontend:
- **HTML5**: Structure of the web pages.
- **CSS3**: Styling and layout, including responsive design.
- **JavaScript (ES6+)**: Client-side logic, API calls, and dynamic content updates.

### Database:
- **MySQL**: Relational database for storing user credentials and quiz questions.

## Project Structure
```
Mentor_baba_Quiz_app/
├── app.py                  # Flask backend application
├── index.html              # Frontend (HTML, CSS, JavaScript)
├── quiz_questions.xlsx     # Example Excel file for questions
└── README.md               # This README file
```

## Setup Instructions
Follow these steps to get the Quiz Application up and running on your local machine.

### Prerequisites
Before you begin, ensure you have the following installed:
- **Git**: Download Git
- **Python 3.x**: Download Python
- **MySQL Server**: Ensure you have a MySQL server installed and running (e.g., via XAMPP/WAMP/MAMP, or a standalone MySQL installation).

### 1. Clone the Repository
First, clone this GitHub repository to your local machine:
```
git clone https://github.com/tanishqkolhatkar93/Mentor_baba_Quiz_app.git
cd Mentor_baba_Quiz_app
```

### 2. Backend Setup (app.py)
#### Install Python Dependencies:
Open your terminal or command prompt, navigate to the Mentor_baba_Quiz_app directory, and install the required Python packages:
```
pip install Flask Flask-CORS mysql-connector-python pandas openpyxl werkzeug
```

#### MySQL Database Configuration:
- Start your MySQL Server. Ensure your MySQL service is running (e.g., via XAMPP/WAMP/MAMP control panel, or by starting the MySQL service directly on your OS).
- Create the Database and Tables: Open your MySQL client (e.g., MySQL Workbench, phpMyAdmin, or command line `mysql -u root -p`) and execute the following SQL commands:

```sql
CREATE DATABASE IF NOT EXISTS quiz_app_db;

USE quiz_app_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_text TEXT NOT NULL,
    option_a VARCHAR(255) NOT NULL,
    option_b VARCHAR(255) NOT NULL,
    option_c VARCHAR(255) NOT NULL,
    option_d VARCHAR(255) NOT NULL,
    correct_option CHAR(1) NOT NULL
);
```

#### Update app.py Credentials:
Open `app.py` and modify the DB_CONFIG dictionary with your actual MySQL username and password:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_mysql_user',        # <--- REPLACE THIS
    'password': 'your_mysql_password', # <--- REPLACE THIS
    'database': 'quiz_app_db'
}
```

#### Run the Flask Backend:
In your terminal, from the Mentor_baba_Quiz_app directory, run the Flask application:
```
python app.py
```
You should see output indicating the Flask app is running, typically on `http://127.0.0.1:5000/`. Keep this terminal window open.

### 3. Frontend Setup (index.html)
Open `index.html`:
Simply open the `index.html` file in your preferred web browser (e.g., Chrome, Firefox, Edge). There's no need for a separate web server for the frontend as it directly calls the Flask backend.

### 4. Prepare Quiz Questions (Excel)
The application uses an Excel file to upload quiz questions.
- The file must have the following exact column headers in the first row: `question_text`, `option_a`, `option_b`, `option_c`, `option_d`, `correct_option`
- The `correct_option` column should contain a single character: `a`, `b`, `c`, or `d`.

An example file (`quiz_questions.xlsx`) is included in the repository.

#### Example quiz_questions.xlsx content:
| question_text                        | option_a | option_b | option_c | option_d | correct_option |
|--------------------------------------|----------|----------|----------|----------|----------------|
| What is the capital of France?       | Berlin   | Madrid   | Paris    | Rome     | c              |
| Which planet is red?                 | Earth    | Mars     | Jupiter  | Venus    | b              |
| ...                                  | ...      | ...      | ...      | ...      | ...            |

## How to Use the Application
- **Access the App**: Open `index.html` in your web browser.
- **Register/Login**:
  - If you're a new user, enter a Username and Password and click "Register".
  - If you have an account, enter your credentials and click "Login".
- **Upload Questions (Admin/First Time Setup)**:
  - In the "Admin: Upload Questions" section, click "Choose File", select your `quiz_questions.xlsx` file, and then click "Upload Questions". This will populate the quiz with questions.
  - Important: You only need to do this once, or whenever you want to update the quiz questions.
- **Start the Quiz**: After successful login and question upload, you'll be taken to the quiz section.
- **Answer Questions**:
  - Select your answer for each question. Your selection is automatically saved.
  - A 30-second timer will count down for each question. If the timer runs out, the app will automatically move to the next question.
- **Navigate Questions**:
  - Use the "Previous" and "Next" buttons to move sequentially.
  - Click on the numbered buttons in the navigation panel to jump to any specific question. Answered questions will turn green in the navigation panel.
- **Submit Quiz**: Once you've answered all questions (or are ready to finish), click the "Submit Quiz" button.
- **View Results**: The "Quiz Results" section will display your score and a detailed summary, showing which questions you answered correctly or incorrectly, along with the correct answers.
- **Restart**: Click "Go to Login" to return to the authentication page and start a new quiz session.

## Screenshots

- **Login/Registration Page**: Initial screen for user authentication and Excel upload.
  <img title="a title" alt="Alt text" src="https://github.com/tanishqkolhatkar93/Mentor_baba_Quiz_app/blob/main/Screenshot%202025-07-17%20224438.png">
  
- **Quiz Interface**: A question displayed with options, timer, and navigation buttons.
 <img title="a title" alt="Alt text" src="https://github.com/tanishqkolhatkar93/Mentor_baba_Quiz_app/blob/main/Screenshot%202025-07-17%20224516.png">
 
- **Quiz Results Summary**: Final score and a breakdown of correct/incorrect answers.
   <img title="a title" alt="Alt text" src="https://github.com/tanishqkolhatkar93/Mentor_baba_Quiz_app/blob/main/Screenshot%202025-07-17%20224549.png">
 


## Contributing
Contributions are welcome! If you have suggestions for improvements or find any bugs, please feel free to:
- Fork the repository.
- Create a new branch (`git checkout -b feature/your-feature-name`).
- Make your changes.
- Commit your changes (`git commit -m 'Add new feature'`).
- Push to the branch (`git push origin feature/your-feature-name`).
- Open a Pull Request.

## License
This project is open-source and available under the MIT License.
