from flask import Blueprint, request, jsonify, current_app
from models import ServiceTicket, db
import uuid

services = Blueprint('services', __name__)

@services.route('/createissue', methods=['POST'])
def create_ticket():
    data = request.get_json()
    ticket_id = str(uuid.uuid4())  # Generate a unique ID for the ticket
    new_ticket = ServiceTicket(
        TicketID=ticket_id,
        location_lat=data['lat'],
        location_long=data['long'],
        issue_type=data['issueType'],
        issue_description=data['description']
    )

    db.session.add(new_ticket)
    db.session.commit()

    return jsonify({'message': 'Ticket created successfully!', 'ticket_id': ticket_id}), 201
