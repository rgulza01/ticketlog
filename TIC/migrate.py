from app import app, db
from models import ServiceTicket, Vehicle, Agent, ServiceStation, User

# def drop_tables():
#     with app.app_context():
#         db.drop_all()

def create_or_update_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    # print("Dropping all tables...")
    # drop_tables()
    # print("Creating or updating tables...")
    create_or_update_tables()
    print("Tables created or updated successfully.")

