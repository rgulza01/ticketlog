from flask import Blueprint, request, jsonify, current_app
from models import ServiceTicket, db, User, ServiceStation
import uuid
import smtplib
from email.mime.text import MIMEText
import math


services = Blueprint('services', __name__)

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587  
SMTP_USERNAME = 'joygum21@gmail.com'
SMTP_PASSWORD = 'not telling you'

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


@services.route('/<ticket_id>/confirm', methods=['POST'])
def confirm_ticket(ticket_id):
    print("Confirming ticket...")  # for logging

    ticket = ServiceTicket.query.get(ticket_id)

    if ticket:
        # Lookup user
        user = User.query.get(ticket.UserID)

        if user:
            # Print recipient email for debugging
            print(f"Sending confirmation email to {user.Email}")

            # Send confirmation email
            msg = MIMEText('Your ticket has been confirmed')
            msg['Subject'] = 'Ticket Confirmation'  
            msg['From'] = SMTP_USERNAME
            msg['To'] = user.Email

            try:
                print(SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD)  # new
                s = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                s.starttls()
                s.login(SMTP_USERNAME, SMTP_PASSWORD)
                s.send_message(msg)
                s.quit()

                return jsonify({'message': 'Ticket confirmed'}), 200
            except smtplib.SMTPRecipientsRefused as e:
                print(f"SMTPRecipientsRefused Exception: {e}")
                return jsonify({'message': 'Recipients refused by SMTP server'}), 500
            except smtplib.SMTPException as e:
                print(f"SMTPException: {e}")
                return jsonify({'message': 'Error sending confirmation email'}), 500
        else:
            return jsonify({'message': 'User not found'}), 404
    else:
        return jsonify({'message': 'Ticket not found'}), 404

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

    