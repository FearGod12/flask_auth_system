#!/usr/bin/env python
from flask import request, jsonify, abort
from models.book import Book
from models.user import User
from flask_login import current_user, login_required
from models import storage
from psycopg2 import errors
from sqlalchemy.exc import SQLAlchemyError
from api.views import app_views


@app_views.route('/books/<book_id>', methods=['GET'])
@login_required
def get_book(book_id):
    book = storage.get(Book, id=book_id)
    if not book:
        abort(404)
    if book.author_id != current_user.id:
        abort(401)
    return jsonify(book.to_dict())

@app_views.route('/books', methods=['GET'], strict_slashes=False)
@login_required
def get_books():
    books = storage.get_all(Book, author_id=current_user.id)
    if not books:
        abort(404)
    return jsonify([book.to_dict() for book in books])

@app_views.route('/books', methods=['POST'], strict_slashes=False)
@login_required
def create_book():
    """creats a new book"""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Data not provided or not JSON"}), 400
    data['author_id'] = current_user.id
    data['author'] = current_user
    if data.get("id"):  # Check if 'id' is provided in data and remove it to prevent conflicts
        data.pop("id")
    try:
        book = Book(**data)
        storage.new(book)
        storage.save()
        return jsonify(book.to_dict()), 201
    
    except SQLAlchemyError as e:
        print(e)
        return jsonify({"error": "Database error", "details": str(e)}), 500

    except errors.InvalidTextRepresentation:
        return jsonify({"error": "Invalid data"}), 400
    
    except Exception as e:
        return jsonify({"error": "An error occurred", "details": str(e)}), 500


@app_views.route('/books/<book_id>', methods=['DELETE'], strict_slashes=False)
@login_required
def delete_book(book_id):
    """deletes a book"""
    book = storage.get(Book, id=book_id)
    if book is None:
        abort(404)
    if book.author_id != current_user.id:
        abort(401)
    storage.delete(book)
    storage.save()
    return jsonify({}), 200