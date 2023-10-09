from flask import Blueprint, request, jsonify
from models import db, User  # Import directly from models, not from app
from flask import json

test_routes = Blueprint('test_routes', __name__)

@test_routes.route('/register', methods=['POST'])
def test_register():
    print("Received a request")
    data = json.loads(request.data)
    print(f"Data received: {data}")  # Print the received data
    new_user = User(Username=data['username'], Password=data['password'])
    db.session.add(new_user)
    try:
        db.session.commit()
        print("User added successfully")  # Print success message
    except Exception as e:
        print(f"Error occurred: {e}")  # Print any error that occurs
    return jsonify({'message': 'Test user created successfully!'})

