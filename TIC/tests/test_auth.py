import unittest
import os
import sys

# Navigate to parent directory 
parent_dir = os.path.abspath(os.path.join('..'))
sys.path.append(parent_dir)  

# Now imports will work
from app import app  
from models import User, db

class TestAuth(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = db
        self.app_context = app.app_context()
        self.app_context.push()

        # Create a new user
        response = self.app.post('/auth/register', json={'username': 'testuser2', 'password': 'testpass'})
        self.assertEqual(response.status_code, 200)
        user = User.query.filter_by(Username='testuser2').first()
        self.assertIsNotNone(user)
        self.db.session.commit()  # Commit the changes to the database

    def test_login(self):
        # Test that a user can log in
        response = self.app.post('/auth/login', json={'username': 'testuser2', 'password': 'testpass'})
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        # Ensure that the user created in `setUp` is removed from the database
        user = User.query.filter_by(Username='testuser2').first()
        if user:
            print(f"User before deletion: {user.Username}")  # Print the username of the user before deletion
            self.db.session.delete(user)
            self.db.session.commit()
            user_after_deletion = User.query.filter_by(Username='testuser2').first()
            print(f"User after deletion: {user_after_deletion}")  # This should print 'None' if the user was successfully deleted
        self.app_context.pop()

if __name__ == '__main__':
    unittest.main()