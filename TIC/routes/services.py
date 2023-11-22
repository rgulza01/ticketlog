from flask import Blueprint, request, jsonify, current_app
from models import ServiceTicket, db, User, ServiceStation
import uuid
import math

services = Blueprint('services', __name__)


@services.route('/createissue', methods=['POST'])
def create_ticket():
    data = request.get_json()
    
    # Check if the provided UserID exists in the User table
    user = User.query.get(data['UserID'])
    if not user:
        return jsonify({'message': 'User not found'}), 404

    ticket_id = str(uuid.uuid4())  # Generate a unique ID for the ticket
    new_ticket = ServiceTicket(
        TicketID=ticket_id,
        UserID=user.UserID,  # Set the UserID from the user
        location_lat=data['lat'],
        location_long=data['long'],
        issue_type=data['issueType'],
        issue_description=data['description'],
        status='pending'  # Set the status explicitly

    )

    db.session.add(new_ticket)
    db.session.commit()

    return jsonify({'message': 'New ticket created successfully!', 'ticket_id': ticket_id}), 201

#...................................being tested............................

@services.route('/<ticket_id>', methods=['DELETE'])
def cancel_ticket(ticket_id):
    ticket = ServiceTicket.query.get(ticket_id)

    if ticket:
        # Update the ticket status to "canceled"
        ticket.status = "canceled"
        db.session.commit()
        return jsonify({"message": "Ticket canceled successfully"})
    else:
        return jsonify({"error": "Ticket not found"}), 404
    
#...................................being tested............................

@services.route('/<ticket_id>/status', methods=['GET'])
def get_ticket_status(ticket_id):
    # Retrieve the ticket from the database based on the provided ticket_id
    ticket = ServiceTicket.query.get(ticket_id)

    if ticket:
        # Return the ticket status
        return jsonify({"status": ticket.status}), 200
    else:
        return jsonify({"error": "Ticket not found"}), 404
    
@services.route('/complete/<ticket_id>', methods=['POST'])
def complete_ticket(ticket_id):
    # Retrieve the ticket from the database based on the provided ticket_id
    ticket = ServiceTicket.query.get(ticket_id)

    if ticket:
        # Update the ticket status to "Completed"
        ticket.status = "Completed"

        # Add any additional details related to the completion if needed
        # ...

        db.session.commit()
        return jsonify({"message": "Ticket completed successfully"}), 200
    else:
        return jsonify({"error": "Ticket not found"}), 404
    

@services.route('/createstation', methods=['POST'])
def create_station():
    data = request.get_json()

    # Assuming you have the necessary fields in the request data
    new_station = ServiceStation(
        StationLatitude=data['latitude'],
        StationLongitude=data['longitude'],
        StationAddress=data['address'],
        StationName=data['name'],
        StationPhoneNumber=data['phone']
    )

    db.session.add(new_station)
    db.session.commit()

    return jsonify({'message': 'New station created successfully!', 'station_id': new_station.StationID}), 201

# ------------------------ Helper functions ------------------------   

def find_nearby_stations(lat, lng):
    stations = ServiceStation.query.filter(
        db.and_(
            ServiceStation.StationLatitude.between(lat - 0.5, lat + 0.5),
            ServiceStation.StationLongitude.between(lng - 0.5, lng + 0.5)
        )
    ).all()
    return stations

def calculate_distance(lat1, lon1, lat2, lon2):
    # Haversine formula
    R = 6371  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance
# ------------------------ End helper functions ------------------------   

@services.route('/assign', methods=['POST'])
def assign_ticket():
    ticket_id = request.args.get('ticket_id')

    if ticket_id:
        ticket = ServiceTicket.query.get(ticket_id)
    else:
        ticket = ServiceTicket.query.filter_by(status='pending').order_by(ServiceTicket.Timestamp).first()

    if ticket:
        stations = find_nearby_stations(ticket.location_lat, ticket.location_long)
        nearest = None
        min_distance = float("inf")

        for station in stations:
            dist = calculate_distance(station.StationLatitude, station.StationLongitude, ticket.location_lat, ticket.location_long)
            if dist < min_distance:  
                nearest = station  
                min_distance = dist

        ticket.assigned_center_id = nearest.StationID
        ticket.status = "Assigned"  # Add this line to update the status

        db.session.commit()
        return jsonify({"message": "Ticket assigned successfully", "assigned_ticket_id": ticket.TicketID, "status": ticket.status})
    else:
        return jsonify({"error": "No pending tickets found"}), 404

    