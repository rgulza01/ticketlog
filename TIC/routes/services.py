from flask import Blueprint, request, jsonify, current_app
from models import ServiceTicket, db, User
import uuid
import smtplib
from email.mime.text import MIMEText

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

@services.route('/assign/<ticket_id>', methods=['POST'])
def assign_ticket(ticket_id):
    ticket = ServiceTicket.query.get(ticket_id)

    if ticket:
        # Update the ticket status to "Assigned"
        ticket.status = "Assigned"

        # Here I can also notify the technician of the new ticket
        # ...

        db.session.commit()
        return jsonify({"message": "Ticket assigned successfully"})
    else:
        return jsonify({"error": "Ticket not found"}), 404
