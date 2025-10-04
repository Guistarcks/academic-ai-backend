
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import db_controller
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
CORS(app)

# Clave secreta para JWT (en producción, usa variable de entorno)
app.config['SECRET_KEY'] = 'supersecretkey'

# Decorador para requerir token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = db_controller.get_user_by_id(data['user_id'])
            if not current_user:
                return jsonify({'message': 'User not found!'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expired!'}), 401
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(*args, **kwargs)
    return decorated

# Endpoint de login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = db_controller.get_user_by_email(email)
    if not user or not check_password_hash(user[4], password):
        return jsonify({'message': 'Credenciales inválidas'}), 401
    token = jwt.encode({
        'user_id': user[0],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    }, app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({'token': token})

@app.route('/api/students', methods=['POST'])
@token_required
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
@token_required
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
    
    # Validación de campos requeridos
    if not data:
        return jsonify({"message": "No se enviaron datos"}), 400
    
    if not data.get('email'):
        return jsonify({"message": "El email es requerido"}), 400
    
    if not data.get('password'):
        return jsonify({"message": "La contraseña es requerida"}), 400
    
    if not data.get('nome'):
        return jsonify({"message": "El nombre es requerido"}), 400
    
    rol = data.get('rol', 'user')
    email = data['email']
    nome = data['nome']
    password = generate_password_hash(data['password'])
    data_creacao = data.get('data_creacao', '')
    
    success = db_controller.insert_user(rol, email, nome, password, data_creacao)
    if not success:
        return jsonify({"message": "El email ya está registrado"}), 409
    return jsonify({"message": "User inserted successfully"}), 201

@app.route('/api/me', methods=['GET'])
@token_required
def get_current_user():
    """Endpoint para obtener los datos del usuario actual (requiere autenticación)"""
    token = None
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
    
    if token:
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            user = db_controller.get_user_by_id(data['user_id'])
            if user:
                return jsonify({
                    "id": user[0],
                    "rol": user[1],
                    "email": user[2],
                    "nome": user[3],
                    "data_creacao": user[5]
                }), 200
        except:
            pass
    
    return jsonify({"message": "Usuario no encontrado"}), 404

@app.route('/api/users', methods=['GET'])
@token_required
def get_all_users():
    """Endpoint para obtener todos los usuarios (requiere autenticación)"""
    users = db_controller.get_all_users()
    result = []
    for u in users:
        result.append({
            "id": u[0],
            "rol": u[1],
            "email": u[2],
            "nome": u[3],
            "data_creacao": u[5]  # u[4] es password, no la devolvemos
        })
    return jsonify(result), 200

@app.route('/api/forms', methods=['POST'])
@token_required
def add_form():
    data = request.get_json()
    form_name = data['name']
    form_data = json.dumps(data['data'])
    db_controller.insert_form(form_name, form_data)
    return jsonify({"message": "Form inserted successfully"}), 201

@app.route('/api/forms', methods=['GET'])
@token_required
def get_forms():
    forms = db_controller.get_all_forms()
    result = [{"id": f[0], "name": f[1], "data": json.loads(f[2])} for f in forms]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
