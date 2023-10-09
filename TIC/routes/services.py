from flask import Blueprint

# Create a Blueprint object
services = Blueprint('services', __name__)

# Use the Blueprint object to define routes
@services.route('/some_route', methods=['GET'])
def some_route():
    return "This is some route"
