
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

@app.route('/api/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(user_id):
    """Endpoint para actualizar un usuario (requiere autenticación)"""
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "No se enviaron datos"}), 400
    
    # Obtener el usuario actual
    user = db_controller.get_user_by_id(user_id)
    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404
    
    # Preparar datos para actualizar
    nome = data.get('nome', user[3])
    rol = data.get('rol', user[1])
    email = data.get('email', user[2])
    
    # Si se envía una nueva contraseña, hashearla
    if data.get('password') and data.get('password').strip():
        password = generate_password_hash(data['password'])
    else:
        password = user[4]  # Mantener la contraseña actual
    
    # Actualizar en la base de datos
    success = db_controller.update_user(user_id, rol, email, nome, password)
    
    if not success:
        return jsonify({"message": "Error al actualizar el usuario (email duplicado)"}), 409
    
    return jsonify({"message": "Usuario actualizado exitosamente"}), 200

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(user_id):
    """Endpoint para eliminar un usuario (requiere autenticación)"""
    
    # Verificar que el usuario existe
    user = db_controller.get_user_by_id(user_id)
    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404
    
    # Eliminar el usuario
    success = db_controller.delete_user(user_id)
    
    if not success:
        return jsonify({"message": "Error al eliminar el usuario"}), 500
    
    return jsonify({"message": "Usuario eliminado exitosamente"}), 200

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

@app.route('/api/historicos', methods=['POST'])
@token_required
def add_historico():
    """Endpoint para guardar un histórico de análisis (requiere autenticación)"""
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "No se enviaron datos"}), 400
    
    nome = data.get('nome', '')
    metas = data.get('metas', '')
    feedback = data.get('feedback', '')
    analysisResult = data.get('analysisResult', '')
    data_creacao = data.get('data_creacao', '')
    
    if not nome or not metas or not feedback or not analysisResult:
        return jsonify({"message": "Todos los campos son requeridos"}), 400
    
    success = db_controller.insert_historico(nome, metas, feedback, analysisResult, data_creacao)
    
    if not success:
        return jsonify({"message": "Error al guardar el histórico"}), 500
    
    return jsonify({"message": "Histórico guardado exitosamente"}), 201

@app.route('/api/historicos', methods=['GET'])
@token_required
def get_historicos():
    """Endpoint para obtener todos los históricos (requiere autenticación)"""
    historicos = db_controller.get_all_historicos()
    result = []
    for h in historicos:
        result.append({
            "id": h[0],
            "nome": h[1],
            "metas": h[2],
            "feedback": h[3],
            "analysisResult": h[4],
            "data_creacao": h[5]
        })
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
