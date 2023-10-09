from app import app, db
from models import ServiceTicket, Vehicle, Agent, ServiceStation, User


def create_or_update_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    print("Creating or updating tables...")
    create_or_update_tables()
    print("Tables created or updated successfully.")
