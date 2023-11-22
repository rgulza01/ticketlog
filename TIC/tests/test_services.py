import unittest
import os
import sys
from datetime import datetime

# Navigate to parent directory 
parent_dir = os.path.abspath(os.path.join('..'))
sys.path.append(parent_dir)  

# Now imports will work
from app import app  
from models import User, ServiceTicket, db

class TestServices(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = db
        self.app_context = app.app_context()
        self.app_context.push()

    def test_create_ticket(self):
        # Test that a new ticket can be created
        response = self.app.post('/tickets/createissue', json={'UserID': 1, 'lat': 41.8781, 'long': -87.6298, 'issueType': 'Flat tire', 'description': 'Need help'})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        ticket = ServiceTicket.query.get(data['ticket_id'])
        self.assertIsNotNone(ticket)

    def test_confirm_ticket(self):
        # Test that a ticket can be confirmed
        response = self.app.post('/tickets/<ticket_id>/confirm')
        self.assertEqual(response.status_code, 200)

    def test_cancel_ticket(self):
        # Test that a ticket can be cancelled
        response = self.app.delete('/tickets/<ticket_id>')
        self.assertEqual(response.status_code, 200)

    def test_get_ticket_status(self):
        # Test that a ticket status can be retrieved
        response = self.app.get('/tickets/<ticket_id>/status')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        # Ensure that the ticket created in `test_create_ticket` is removed from the database
        ticket = ServiceTicket.query.filter_by(UserID=1).first()
        if ticket:
            self.db.session.delete(ticket)
            self.db.session.commit()
        self.app_context.pop()

if __name__ == '__main__':
    unittest.main()
