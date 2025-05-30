import os
import database
from flask import Flask, render_template, redirect, session, request

app = Flask(__name__)
app.secret_key = os.urandom(24) 

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

@app.route('/quiz')
def quiz_question():
    """ Отображение текущего вопроса викторины """
    question_index = session.get('current_question_index')
    questions = session.get('questions')

    if question_index < len(questions):
        current_question_data = questions[question_index]
        return render_template('question_page.html',
                               question = current_question_data,
                               question_number = question_index + 1,
                               total_question = len(questions),
                               page_title = f'Вопрос {question_index + 1}')
    else:
        return redirect('/results')

@app.route('/answer', methods=['POST'])
def submit_answer():
    """Обработка ответа пользователя на вопрос"""
    question_index = session.get('current_question_index')
    questions = session.get('questions')

    user_answer_index = int(request.form.get('answer'))
    corret_answer_index = questions[question_index]['correct_option_index']

    if user_answer_index == corret_answer_index:
        session['score'] += 1

    session['current_question_index'] += 1
    return redirect('/quiz')

@app.route('/results')
def results():
    score = session.get('score')
    total_questions = len( session.get('questions') )
    return render_template('results_page.html',
                           score = score,
                           total_questions = total_questions)

# --- Маршруты для простой админ-панели ---
@app.route('/admin/add', methods=['GET', 'POST'])
def admin_add_question_page():
    if request.method == 'GET':
        return render_template('admin_add_question.html')
    if request.method == 'POST':
        question_text = request.form.get('questions_text')
        option1 = request.form.get('option1')
        option2 = request.form.get('option2')
        option3 = request.form.get('option3')
        option4 = request.form.get('option4')
        correct_option_index = request.form.get('correct_option_index')
        database.add_new_question(question_text, option1, option2, option3, option4, correct_option_index)
        return redirect('/admin/add')

database.init_database()
app.run(debug=True) 