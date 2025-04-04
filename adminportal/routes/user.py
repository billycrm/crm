from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import db
from database.models.user import User

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    name = data.get('name')

    if not all([username, password, email, name]):
        return jsonify({'message': 'All fields are required.'}), 400

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'message': 'User with this username or email already exists.'}), 409

    hashed_password = generate_password_hash(password, method='sha256')

    user = User(
        username=username,
        password=hashed_password,
        email=email,
        name=name
    )

    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully.'}), 201


@user_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found.'}), 404

    return jsonify(user.serialize()), 200


@user_bp.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    users_list = [user.serialize() for user in users]
    return jsonify(users_list), 200


@user_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found.'}), 404

    username = data.get('username', user.username)
    email = data.get('email', user.email)
    name = data.get('name', user.name)
    password = data.get('password', None)

    if password:
        user.password = generate_password_hash(password, method='sha256')

    user.username = username
    user.email = email
    user.name = name
    user.email_confirmed = data.get('email_confirmed', user.email_confirmed)
    user.user_confirmed = data.get('user_confirmed', user.user_confirmed)
    user.admin = data.get('admin', user.admin)

    db.session.commit()
    return jsonify({'message': 'User updated successfully.'}), 200


@user_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found.'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully.'}), 200
