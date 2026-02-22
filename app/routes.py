from flask import Blueprint, jsonify

from app.models import get_all_users, get_user_by_id

api = Blueprint('api', __name__)


@api.route('/users', methods=['GET'])
def users_list():
    users = get_all_users()
    return jsonify(users)


@api.route('/users/<int:user_id>', methods=['GET'])
def user_detail(user_id):
    user = get_user_by_id(user_id)
    if user is None:
        return jsonify({'error': 'Пользователь не найден'}), 404
    return jsonify(user)
