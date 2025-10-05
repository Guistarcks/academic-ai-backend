

import sqlite3

def init_db():
    conn = sqlite3.connect('academicia.db')
    cursor = conn.cursor()
    # Tabela de estudantes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            grades TEXT,
            goals TEXT,
            feedback TEXT,
            data_creacao TEXT
        )
    ''')
    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rol TEXT,
            email TEXT UNIQUE NOT NULL,
            nome TEXT,
            password TEXT,
            data_creacao TEXT
        )
    ''')
    # Tabela de históricos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            metas TEXT,
            feedback TEXT,
            analysisResult TEXT,
            data_creacao TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_user_by_id(user_id):
    conn = sqlite3.connect('academicia.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user
    
def get_user_by_email(email):
    conn = sqlite3.connect('academicia.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def insert_student(nome, grades, goals, feedback, data_creacao):
    conn = sqlite3.connect('academicia.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (nome, grades, goals, feedback, data_creacao) VALUES (?, ?, ?, ?, ?)',
                   (nome, grades, goals, feedback, data_creacao))
    conn.commit()
    conn.close()

def get_all_students():
    conn = sqlite3.connect('academicia.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    conn.close()
    return students

def insert_user(rol, email, nome, password, data_creacao):
    conn = sqlite3.connect('academicia.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (rol, email, nome, password, data_creacao) VALUES (?, ?, ?, ?, ?)',
                       (rol, email, nome, password, data_creacao))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_users():
    conn = sqlite3.connect('academicia.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

def update_user(user_id, rol, email, nome, password):
    """Actualizar un usuario en la base de datos"""
    conn = sqlite3.connect('academicia.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE users 
            SET rol = ?, email = ?, nome = ?, password = ?
            WHERE id = ?
        ''', (rol, email, nome, password, user_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Error si el email ya existe
        return False
    finally:
        conn.close()

def delete_user(user_id):
    """Eliminar un usuario de la base de datos"""
    conn = sqlite3.connect('academicia.db')
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")
        return False
    finally:
        conn.close()

def create_forms_table():
    conn = sqlite3.connect('academicia.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS forms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            answers TEXT,
            data_creacao TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_form(student_id, answers, data_creacao):
    conn = sqlite3.connect('academicia.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO forms (student_id, answers, data_creacao) VALUES (?, ?, ?)',
                   (student_id, answers, data_creacao))
    conn.commit()
    conn.close()

def get_all_forms():
    conn = sqlite3.connect('academicia.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM forms')
    forms = cursor.fetchall()
    conn.close()
    return forms

def insert_historico(nome, metas, feedback, analysisResult, data_creacao):
    """Insertar un nuevo histórico de análisis en la base de datos"""
    conn = sqlite3.connect('academicia.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO historicos (nome, metas, feedback, analysisResult, data_creacao) 
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, metas, feedback, analysisResult, data_creacao))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al insertar histórico: {e}")
        return False
    finally:
        conn.close()

def get_all_historicos():
    """Obtener todos los históricos de análisis"""
    conn = sqlite3.connect('academicia.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM historicos ORDER BY id DESC')
    historicos = cursor.fetchall()
    conn.close()
    return historicos