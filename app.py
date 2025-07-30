# app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json

# --- Configuration ---
# You would typically load these from environment variables or a config file
# For simplicity, they are hardcoded here. Replace with your MySQL credentials.

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Homepage (serves index.html)
@app.route('/')
def home():
    return render_template('index.html')


DB_CONFIG = {
    'host': 'localhost',
    'user': 'root', # <--- IMPORTANT: Replace with your MySQL username
    'password': '12345', # <--- IMPORTANT: Replace with your MySQL password
    'database': 'quiz_app_db' # <--- IMPORTANT: Ensure this database exists or create it
}

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
CORS(app) # Enable CORS for frontend communication
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Database Connection Helper ---
def get_db_connection():
    """Establishes and returns a new database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

# --- Database Initialization (Run this once manually or via a script) ---
# You can run these SQL commands directly in your MySQL client to set up the tables:
"""
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
"""

# --- API Endpoints ---

@app.route('/')
def index():
    """Serves a simple message for the root URL."""
    return "Quiz App Backend is running!"

@app.route('/register', methods=['POST'])
def register():
    """Handles user registration."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Database connection error'}), 500

    cursor = conn.cursor()
    try:
        # Check if username already exists
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify({'message': 'Username already exists'}), 409

        # Hash the password before storing
        hashed_password = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                       (username, hashed_password))
        conn.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Error during registration: {err}")
        return jsonify({'message': 'Registration failed'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    """Handles user login."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Database connection error'}), 500

    cursor = conn.cursor(dictionary=True) # Return rows as dictionaries
    try:
        cursor.execute("SELECT id, username, password_hash FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password_hash'], password):
            # In a real application, you would generate and return a JWT token here
            # For this example, we just return a success message and user ID.
            return jsonify({'message': 'Login successful', 'user_id': user['id'], 'username': user['username']}), 200
        else:
            return jsonify({'message': 'Invalid username or password'}), 401
    except mysql.connector.Error as err:
        print(f"Error during login: {err}")
        return jsonify({'message': 'Login failed'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/upload_questions', methods=['POST'])
def upload_questions():
    """
    Handles uploading quiz questions from an Excel file.
    Expected Excel columns: question_text, option_a, option_b, option_c, option_d, correct_option
    """
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file and file.filename.endswith(('.xlsx', '.xls')):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        conn = get_db_connection()
        if conn is None:
            return jsonify({'message': 'Database connection error'}), 500
        cursor = conn.cursor()

        try:
            # Read Excel file into a pandas DataFrame
            df = pd.read_excel(filepath)

            # Validate expected columns
            expected_columns = ['question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option']
            if not all(col in df.columns for col in expected_columns):
                return jsonify({'message': f'Excel file must contain columns: {", ".join(expected_columns)}'}), 400

            # Clear existing questions before inserting new ones (optional, but good for fresh uploads)
            cursor.execute("DELETE FROM questions")
            conn.commit()

            # Insert questions into the database
            for index, row in df.iterrows():
                try:
                    cursor.execute(
                        "INSERT INTO questions (question_text, option_a, option_b, option_c, option_d, correct_option) VALUES (%s, %s, %s, %s, %s, %s)",
                        (row['question_text'], row['option_a'], row['option_b'],
                         row['option_c'], row['option_d'], str(row['correct_option']).lower()) # Ensure correct_option is lowercase char
                    )
                except KeyError as e:
                    conn.rollback() # Rollback if a column is missing in a row
                    return jsonify({'message': f'Missing column in Excel row {index + 2}: {e}'}), 400
            conn.commit()
            return jsonify({'message': f'Successfully uploaded {len(df)} questions'}), 200

        except Exception as e:
            conn.rollback()
            print(f"Error processing Excel file: {e}")
            return jsonify({'message': f'Error processing Excel file: {str(e)}'}), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({'message': 'Invalid file type. Please upload an Excel (.xlsx or .xls) file.'}), 400

@app.route('/quiz/questions', methods=['GET'])
def get_quiz_questions():
    """Fetches all quiz questions from the database."""
    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Database connection error'}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, question_text, option_a, option_b, option_c, option_d FROM questions ORDER BY id")
        questions = cursor.fetchall()
        return jsonify(questions), 200
    except mysql.connector.Error as err:
        print(f"Error fetching questions: {err}")
        return jsonify({'message': 'Failed to fetch questions'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/quiz/submit', methods=['POST'])
def submit_quiz():
    """
    Receives user answers, calculates score, and returns results.
    Expected request body: {'answers': {'question_id_1': 'selected_option_char', ...}}
    """
    data = request.get_json()
    user_answers = data.get('answers') # This will be a dictionary: {question_id: selected_option_char}

    if not user_answers:
        return jsonify({'message': 'No answers provided'}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Database connection error'}), 500

    cursor = conn.cursor(dictionary=True)
    try:
        # Fetch all correct answers from the database for comparison
        # Use a WHERE IN clause to fetch only the questions the user answered
        question_ids = tuple(user_answers.keys())
        if not question_ids: # Handle case where user_answers is empty
            return jsonify({'score': 0, 'total_questions': 0, 'results': []}), 200

        # Ensure question_ids are integers for the query
        question_ids_int = [int(q_id) for q_id in question_ids]

        # Construct the placeholder string for the IN clause dynamically
        placeholders = ', '.join(['%s'] * len(question_ids_int))
        query = f"SELECT id, question_text, correct_option, option_a, option_b, option_c, option_d FROM questions WHERE id IN ({placeholders})"
        cursor.execute(query, tuple(question_ids_int))
        correct_answers_data = {q['id']: q for q in cursor.fetchall()}

        score = 0
        results = []
        total_questions_answered = len(user_answers)

        for q_id_str, selected_option in user_answers.items():
            q_id = int(q_id_str)
            question_data = correct_answers_data.get(q_id)

            if question_data:
                is_correct = (str(selected_option).lower() == str(question_data['correct_option']).lower())
                if is_correct:
                    score += 1
                results.append({
                    'question_id': q_id,
                    'question_text': question_data['question_text'],
                    'user_answer': selected_option,
                    'correct_answer': question_data['correct_option'],
                    'is_correct': is_correct,
                    'options': {
                        'a': question_data['option_a'],
                        'b': question_data['option_b'],
                        'c': question_data['option_c'],
                        'd': question_data['option_d']
                    }
                })
            else:
                # Handle case where a question ID from user answers isn't found in DB
                results.append({
                    'question_id': q_id,
                    'question_text': 'Question not found',
                    'user_answer': selected_option,
                    'correct_answer': 'N/A',
                    'is_correct': False,
                    'options': {}
                })

        return jsonify({
            'score': score,
            'total_questions': total_questions_answered,
            'results': results
        }), 200

    except mysql.connector.Error as err:
        print(f"Error submitting quiz: {err}")
        return jsonify({'message': 'Failed to submit quiz'}), 500
    except Exception as e:
        print(f"Unexpected error in submit_quiz: {e}")
        return jsonify({'message': f'An unexpected error occurred: {str(e)}'}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000) # Run on port 5000
