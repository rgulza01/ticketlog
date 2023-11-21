import importlib
# import routes.test_routes

import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from models import db
from routes.auth import auth
from routes.services import services
# from routes.test_routes import test_routes  # Import the new Blueprint
import os

app = Flask(__name__)

# Configure logging
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

# Configure SQLAlchemy
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "app.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db.init_app(app)

# Register blueprints
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(services, url_prefix='/tickets')
# app.register_blueprint(test_routes, url_prefix='/test')  

if __name__ == "__main__":
    app.run(debug=True)
