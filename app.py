#!/usr/bin/env python

"""
flask app for api calls
"""

from datetime import timedelta
from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
from models import storage
from api.views import app_views
from flask_login import LoginManager
from os import getenv
from models import storage
from models.user import User


app = Flask(__name__)
app.secret_key = getenv('APP_SECRET_KEY') 
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=1)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return storage.get(User, id=user_id)

@login_manager.unauthorized_handler
def unauthorized():
    """unauthorized 401 error handler"""
    return jsonify({"Error": "Unauthorized"}), 401

@app.errorhandler(404)
def not_found(error):
    """custom 404 error message"""
    return jsonify({"Error": "The requested resource could not be found"}), 404

@app.errorhandler(401)
def unauthorized(error):
    """custom 401 error message"""
    return jsonify({"Error": "You are not authorized to access this resource"}), 401



@app.route('/', methods=['GET'])
def home():
    """home route"""
    return jsonify({"message": "Welcome to the Authors Haven API"})

def index():
    """index route"""
    return jsonify({"message": "Welcome to the Authors Haven API"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001)