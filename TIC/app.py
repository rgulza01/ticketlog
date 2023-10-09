from flask import Flask
from models import db
import os

app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "app.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

# Initialize the app with Flask-SQLAlchemy
db.init_app(app)

# Create the database tables within SQLAlchemy's scope
with app.app_context():
    db.create_all()

# Import the routes module, which contains the definitions for your API endpoints
from routes.auth import auth
app.register_blueprint(auth, url_prefix='/auth')

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/')
def home():
    return 'Welcome to my Flask app!'
