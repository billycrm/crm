from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.db import db
from database.models.membership import Membership
from database.models.user import User
from datetime import datetime

membership_bp = Blueprint('membership_bp', __name__)


@membership_bp.route('/memberships', methods=['POST'])
@jwt_required()
def create_membership():
    data = request.get_json()
    user_id = get_jwt_identity()
    membership_type = data.get('membership_type')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    print(data)

    if not all([membership_type, start_date, end_date]):
        return jsonify({'message': 'All fields are required.'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found.'}), 404

    membership = Membership(
        membership_type=membership_type,
        start_date=datetime.strptime(start_date, '%Y-%m-%d').date(),
        end_date=datetime.strptime(end_date, '%Y-%m-%d').date(),
        user_id=user_id
    )
    db.session.add(membership)
    db.session.commit()

    return jsonify({'message': 'Membership created successfully.'}), 201


@membership_bp.route('/memberships/<int:id>', methods=['GET'])
@jwt_required()
def get_membership(id):
    user_id = get_jwt_identity()
    membership = Membership.query.filter_by(id=id, user_id=user_id).first()

    if not membership:
        return jsonify({'message': 'Membership not found.'}), 404

    membership_data = {
        'id': membership.id,
        'membership_type': membership.membership_type,
        'start_date': membership.start_date.strftime('%Y-%m-%d'),
        'end_date': membership.end_date.strftime('%Y-%m-%d'),
        'user_id': membership.user_id,
        'has_used_free_trial': membership.has_used_free_trial
    }

    return jsonify(membership_data), 200


@membership_bp.route('/memberships', methods=['GET'])
@jwt_required()
def list_memberships():
    user_id = get_jwt_identity()
    memberships = Membership.query.filter_by(user_id=user_id).all()

    memberships_list = [{
        'id': membership.id,
        'membership_type': membership.membership_type.name,
        'start_date': membership.start_date.strftime('%Y-%m-%d'),
        'end_date': membership.end_date.strftime('%Y-%m-%d'),
        'user_id': membership.user_id,
        'has_used_free_trial': membership.has_used_free_trial,
        'active': membership.active
    } for membership in memberships]

    return jsonify(memberships_list), 200
    # return jsonify(memberships_list), 200


@membership_bp.route('/memberships/<int:id>', methods=['PUT'])
@jwt_required()
def update_membership(id):
    data = request.get_json()
    user_id = get_jwt_identity()
    membership = Membership.query.filter_by(id=id, user_id=user_id).first()

    if not membership:
        return jsonify({'message': 'Membership not found.'}), 404

    membership.membership_type = data.get('membership_type', membership.membership_type)
    membership.start_date = datetime.strptime(data.get('start_date', membership.start_date.strftime('%Y-%m-%d')),
                                              '%Y-%m-%d').date()
    membership.end_date = datetime.strptime(data.get('end_date', membership.end_date.strftime('%Y-%m-%d')),
                                            '%Y-%m-%d').date()
    membership.has_used_free_trial = data.get('has_used_free_trial', membership.has_used_free_trial)

    db.session.commit()

    return jsonify({'message': 'Membership updated successfully.'}), 200


@membership_bp.route('/memberships/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_membership(id):
    user_id = get_jwt_identity()
    membership = Membership.query.filter_by(id=id, user_id=user_id).first()

    if not membership:
        return jsonify({'message': 'Membership not found.'}), 404

    db.session.delete(membership)
    db.session.commit()

    return jsonify({'message': 'Membership deleted successfully.'}), 200

