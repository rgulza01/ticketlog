from app import app, db
from models import User

# Initialize the Flask app and database
app.app_context().push()
db.create_all()

# Create a new user named "Bismillah"
new_user = User(Username='bismillah', FirstName='Bismillah', LastName='LastName', Email='bismillah@example.com', UserPhoneNumber='123456789')
new_user.set_password('password123')  # Set the user's password
db.session.add(new_user)
db.session.commit()

# Authenticate the user
username = 'bismillah'
password = 'password123'
user = User.query.filter_by(Username=username).first()

if user and user.verify_password(password):
    print(f"User '{username}' authenticated successfully.")
else:
    print(f"Authentication failed for user '{username}'.")

# Clean up: drop all tables after testing
#db.drop_all()
