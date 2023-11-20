from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), unique=True)
    Password = db.Column(db.String(50))
    FirstName = db.Column(db.String(50))
    LastName = db.Column(db.String(50))
    Email = db.Column(db.String(50), unique=True)
    UserPhoneNumber = db.Column(db.String(20))
    def set_password(self, password):
        # Hash the password before storing it in the database
        self.Password = generate_password_hash(password, method='pbkdf2:sha256')

    def verify_password(self, password):
        # Check if the provided password matches the stored hashed password
        return check_password_hash(self.Password, password)

class Vehicle(db.Model):
    VIN = db.Column(db.String(50), primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    VehicleModel = db.Column(db.String(50))
    Make = db.Column(db.String(50))
    YearOfManufacture = db.Column(db.Integer)
    LicenseNo = db.Column(db.String(20))
    DateOfPurchase = db.Column(db.DateTime)

class ServiceTicket(db.Model):
    TicketID = db.Column(db.String(36), primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    StationID = db.Column(db.Integer, db.ForeignKey('service_station.StationID'))
    VIN = db.Column(db.String(50), db.ForeignKey('vehicle.VIN'))
    Timestamp = db.Column(db.DateTime)
    location_lat = db.Column(db.Float)  
    location_long = db.Column(db.Float)   
    issue_status = db.Column(db.String(20))   
    issue_type = db.Column(db.String)  
    issue_description = db.Column(db.Text)  
    Address = db.Column(db.Text)
    Warranty = db.Column(db.Boolean)
    #status = db.Column(db.String(20), nullable=False)  # for TIC-15 and cancellation


class ServiceStation(db.Model):
    StationID = db.Column(db.Integer, primary_key=True)
    AgentID = db.Column(db.Integer, db.ForeignKey('agent.AgentID'))
    StationLatitude = db.Column(db.Float)
    StationLongitude = db.Column(db.Float)
    StationAddress = db.Column(db.Text)
    StationName = db.Column(db.String(50))
    StationPhoneNumber = db.Column(db.String(20))

class Agent(db.Model):
    AgentID = db.Column(db.Integer, primary_key=True)
    TicketID = db.Column(db.Integer, db.ForeignKey('service_ticket.TicketID'))
    Username = db.Column(db.String(50), unique=True)
    Password = db.Column(db.String(50))
    FirstName = db.Column(db.String(50))
    LastName = db.Column(db.String(50))
