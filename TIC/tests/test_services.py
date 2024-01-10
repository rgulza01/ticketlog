import unittest
import os
import sys
from datetime import datetime

# Navigate to parent directory 
parent_dir = os.path.abspath(os.path.join('..'))
sys.path.append(parent_dir)  

# Now imports will work
from app import app  
from models import User, ServiceTicket, db, ServiceStation

class TestServices(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = db
        self.app_context = app.app_context()
        self.app_context.push()

    def test_ticket_lifecycle(self):
        # Test that a new ticket can be created
        response = self.app.post('/tickets/createissue', json={'UserID': 1, 'lat': 41.8781, 'long': -87.6298, 'issueType': 'Test tire', 'description': 'Need help'})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        ticket_id = data['ticket_id']
        ticket = ServiceTicket.query.get(ticket_id)
        self.assertIsNotNone(ticket)

        # Test that the created ticket can be cancelled
        response = self.app.delete(f'/tickets/{ticket_id}')
        self.assertEqual(response.status_code, 200)

        # Test that a ticket status can be retrieved
        response = self.app.get(f'/tickets/{ticket_id}/status')
        self.assertEqual(response.status_code, 200)

        # Test that a ticket can be completed
        response = self.app.post(f'/tickets/complete/{ticket_id}')
        self.assertEqual(response.status_code, 200)

        # Test that a ticket can be assigned
        response = self.app.post(f'/tickets/assign?ticket_id={ticket_id}')
        self.assertEqual(response.status_code, 200)

    def test_create_station(self):
        # Test that a new station can be created
        response = self.app.post('/tickets/createstation', json={'latitude': 56.8561, 'longitude': -75.8697, 'address': 'Some address', 'name': 'Station name', 'phone': '1234567890'})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        station_id = data['station_id']
        station = ServiceStation.query.get(station_id)
        self.assertIsNotNone(station)

    def tearDown(self):
        # # Ensure that the ticket created in `test_create_ticket` is removed from the database
        # ticket = ServiceTicket.query.filter_by(UserID=1).first()
        # if ticket:
        #     self.db.session.delete(ticket)
        #     self.db.session.commit()

        #  # Ensure that the station created in `test_create_station` is removed from the database
        # station = ServiceStation.query.filter_by(StationName='Station name').first()
        # if station:
        #     self.db.session.delete(station)
        #     self.db.session.commit()

        self.app_context.pop()

if __name__ == '__main__':
    unittest.main()
