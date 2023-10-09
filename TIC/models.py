from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), unique=True)
    Password = db.Column(db.String(50))
    FirstName = db.Column(db.String(50))
    LastName = db.Column(db.String(50))
    Email = db.Column(db.String(50), unique=True)
    UserPhoneNumber = db.Column(db.String(20))

class Vehicle(db.Model):
    VIN = db.Column(db.String(50), primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    VehicleModel = db.Column(db.String(50))
    Make = db.Column(db.String(50))
    YearOfManufacture = db.Column(db.Integer)
    LicenseNo = db.Column(db.String(20))
    DateOfPurchase = db.Column(db.DateTime)

class ServiceTicket(db.Model):
    TicketID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    StationID = db.Column(db.Integer, db.ForeignKey('service_station.StationID'))
    VIN = db.Column(db.String(50), db.ForeignKey('vehicle.VIN'))
    Timestamp = db.Column(db.DateTime)
    TicketLatitude = db.Column(db.Float)
    TIcketLongitude = db.Column(db.Float)
    TIcketStatus = db.Column(db.String(20))
    IssuesDescription = db.Column(db.Text)
    Address = db.Column(db.Text)
    Warranty = db.Column(db.Boolean)

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
