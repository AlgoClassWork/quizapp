import database
from flask import Flask, render_template

app = Flask(__name__)

# --- Маршруты для викторины ---

@app.route('/')
def home():
    """Главная страница или стартовая страница викторины."""
    return render_template('start_quiz.html')

@app.route('/start-quiz', methods=['POST'])
def start_quiz():
    """Начинает викторину: загружает вопросы, инициализирует сессию."""
    pass

# --- Маршруты для простой админ-панели ---

database.init_database()
app.run(debug=True) 