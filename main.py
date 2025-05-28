import database
from flask import Flask, render_template, redirect, session

app = Flask(__name__)

# --- Маршруты для викторины ---

@app.route('/')
def home():
    """Главная страница или стартовая страница викторины."""
    return render_template('start_quiz.html')

@app.route('/start-quiz', methods=['POST'])
def start_quiz():
    """Начинает викторину: загружает вопросы, инициализирует сессию."""
    all_question_from_db = database.get_all_questions()
    if not all_question_from_db:
        return redirect('/')
    
    session['questions'] = [dict(question) for question in all_question_from_db]
    session['current_question_index'] = 0
    session['score'] = 0

    return redirect('/quiz')

# --- Маршруты для простой админ-панели ---

database.init_database()
app.run(debug=True) 
