import sqlite3

DATABASE_NAME = 'quiz_data.db'

def get_connection():
    """Подключается к БД и возвращает объект соединения."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row 
    return conn

def init_database():
    """Создает таблицу вопросов, если она еще не существует."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT NOT NULL,
            option1 TEXT NOT NULL,
            option2 TEXT NOT NULL,
            option3 TEXT NOT NULL,
            option4 TEXT NOT NULL,
            correct_option_index INTEGER NOT NULL -- 0, 1, 2, or 3
        )
    """)
    conn.commit()
    conn.close()

def add_new_question(text, opt1, opt2, opt3, opt4, correct_idx):
    """Добавляет новый вопрос в базу данных."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                    INSERT INTO questions (question_text, option1, option2, option3, option4, correct_option_index)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """, (text, opt1, opt2, opt3, opt4, correct_idx))
    conn.commit()
    conn.close()

def get_all_questions():
    """Возвращает список всех вопросов из базы данных."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, question_text, option1, option2, option3, option4, correct_option_index FROM questions")
    questions = cursor.fetchall()
    conn.close()
    return questions

def delete_question_by_id(question_id):
    """Удаляет вопрос по его ID."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM questions WHERE id = ?", (question_id,))
        conn.commit()
        return True # Возвращаем True в случае успеха
    except sqlite3.Error as e:
        print(f"Ошибка при удалении вопроса из БД (ID: {question_id}): {e}")
        return False # Возвращаем False в случае ошибки
    finally:
        conn.close()
