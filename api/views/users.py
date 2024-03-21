#!/usr/bin/env python
"""
users route controller for handling api calls for User"""

import psycopg2
import pydantic
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
from api.views import app_views
from flask import jsonify, request, abort
from models.user import User
from models import storage
from flask_login import login_required, login_user, logout_user, current_user


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """
    query-> SELECT * FROM users 
    [Returns a dictionary (key:obj) object for easy indexing]
    """
    users = storage.get_all(User)
    if not users:
        abort(404)
    return jsonify([user.to_dict() for user in users])

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@login_required
def get_user_by_id(user_id):
    """
    query-> SELECT * FROM user where id=user_id
    Returns a user object
    """
    if current_user.id != user_id:
         abort(401)
    user = storage.get(User, current_user.id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


from psycopg2 import errors

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Insert a new user into the database
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Data not provided or not JSON"}), 400
    
    try:
        # Create a new user object
        if data.get("id"):  # Check if 'id' is provided in data and remove it to prevent conflicts
             data.pop("id")
        
        user = User(**data)
        
        # Add the user to the database session
        storage.new(user)
        # Commit the session to save the user to the database
        storage.save()
        
        return jsonify({"success": "User created successfully", "user": user.to_dict()}), 200
    
    except errors.UniqueViolation:
        return jsonify({"error": "User already exists"}), 400

    except errors.InvalidTextRepresentation:
        return jsonify({"error": "Invalid data"}), 400

    except SQLAlchemyError as e:
        print(e)
        return jsonify({"error": "Database error", "details": str(e)}), 500
    
    except Exception as e:
        return jsonify({"error": "An error occurred", "details": str(e)}), 500


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
@login_required
def update_user(user_id):
    """Update User with a matching user_id"""
    if current_user.id != user_id:
         abort(401)
    user = storage.get(User, current_user.id)
    if user is None:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'error': 'Data not a JSON'}), 400
    if 'id' in data:
        data.pop('id')
    try:
        for key, value in data.items():
            setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
    except errors.UniqueViolation:
        return jsonify({"error": "User already exists"}), 400

    except errors.InvalidTextRepresentation:
        return jsonify({"error": "Invalid data"}), 400

    except SQLAlchemyError as e:
        print(e)
        return jsonify({"error": "Database error", "details": str(e)}), 500
    
    except Exception as e:
        return jsonify({"error": "An error occurred", "details": str(e)}), 500


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes User with a matching user_id:
    query-> DELETE FROM users WHERE id=user_id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/login', methods=['POST'])
def login():
    # Get the user object based on credentials
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Data not provided or not JSON"})
    user = storage.get(User, email=data['email'])
    if not user:
        return abort(404, {"error": "User not found"})
    print("user password: ", user.password)
    print("data password: ", data['password'])
    if not user.check_password(data['password']):
        return abort(401, {"error": "Invalid password"})
    print(user.check_password(data['password']))
    
    login_user(user)
    return jsonify({"succes": "User logged in successfully", "user": user.to_dict()}), 200
    
@app_views.route('/logout', methods=['GET'])
@login_required
def logout():
     result = logout_user()
     print(result)
     return jsonify({"success": "Logout successfully"}), 200
