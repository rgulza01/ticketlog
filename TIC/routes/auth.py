from flask import Blueprint, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(Username=data['username'], Password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})

@auth.route('/login', methods=['POST']) 
def login():
    data = request.get_json()
    user = User.query.filter_by(Username=data['username']).first()

    if not user or not check_password_hash(user.Password, data['password']):
        return make_response('Could not verify', 401)

    return jsonify({'message': 'Logged in successfully!'})
