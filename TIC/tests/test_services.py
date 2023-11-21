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

    def test_register(self):
        # Test that a new user can be added to the database
        response = self.app.post('/auth/register', json={'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 200)
        user = User.query.filter_by(Username='testuser').first()
        self.assertIsNotNone(user)

    def test_login(self):
        # Test that a user can log in
        response = self.app.post('/auth/login', json={'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        # Ensure that the user created in `test_register` is removed from the database
        user = User.query.filter_by(Username='testuser').first()
        if user:
            self.db.session.delete(user)
            self.db.session.commit()
        self.app_context.pop()

if __name__ == '__main__':
    unittest.main()
