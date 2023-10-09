from flask import Blueprint, request, jsonify, current_app
from models import ServiceTicket, db

services = Blueprint('services', __name__)

@services.route('/createissue', methods=['POST'])
def create_ticket():
    data = request.get_json()
    new_ticket = ServiceTicket(
        location_lat=data['lat'],
        location_long=data['long'],
        issue_type=data['issueType'],
        issue_description=data['description']
    )

    current_app.logger.info('Received POST request to /api/tickets')
    current_app.logger.info(f'Received data: {data}')
    db.session.add(new_ticket)
    db.session.commit()

    return jsonify({'message': 'Ticket created successfully!'}), 201



