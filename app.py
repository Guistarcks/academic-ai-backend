from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
from flask_cors import CORS
import db_controller

app = Flask(__name__)
CORS(app)

@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.get_json()
    nome = data['nome']
    grades = ','.join(map(str, data['grades']))  # lista a string
    goals = data['goals']
    feedback = data.get('feedback', '')
    data_creacao = data.get('data_creacao', '')
    db_controller.insert_student(nome, grades, goals, feedback, data_creacao)
    return jsonify({"message": "Student inserted successfully"}), 201

@app.route('/api/students', methods=['GET'])
def get_students():
    students = db_controller.get_all_students()
    result = [
        {"id": s[0], "nome": s[1], "grades": s[2], "goals": s[3], "feedback": s[4], "data_creacao": s[5]}
        for s in students
    ]
    return jsonify(result)

@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.get_json()
    rol = data['rol']
    email = data['email']
    nome = data['nome']
    password = generate_password_hash(data['password'])
    data_creacao = data.get('data_creacao', '')
    db_controller.insert_user(rol, email, nome, password, data_creacao)
    return jsonify({"message": "User inserted successfully"}), 201

@app.route('/api/users', methods=['GET'])
def get_users():
    users = db_controller.get_all_users()
    result = [
        {"id": u[0], "rol": u[1], "email": u[2], "nome": u[3], "password": u[4], "data_creacao": u[5]}
        for u in users
    ]
    return jsonify(result)

@app.route('/api/forms', methods=['POST'])
def add_form():
    data = request.get_json()
    student_id = data['student_id']
    answers = data['answers']
    data_criacao = data.get('data_criacao', '')
    db_controller.insert_form(student_id, answers, data_criacao)
    return jsonify({"message": "Form inserted successfully"}), 201

@app.route('/api/forms', methods=['GET'])
def get_forms():
    forms = db_controller.get_all_forms()
    result = [
        {"id": f[0], "student_id": f[1], "answers": f[2], "data_criacao": f[3]}
        for f in forms
    ]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
