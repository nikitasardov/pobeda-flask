from flask import Blueprint, jsonify, request

from app.models import get_all_users, get_user_by_id, create_user
import re

api = Blueprint('api', __name__)

EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')


@api.route('/users', methods=['GET'])
def users_list():
    users = get_all_users()
    return jsonify(users)


@api.route('/users', methods=['POST'])
def users_create():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Тело запроса должно быть JSON'}), 400

    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip()

    errors = []
    if not name:
        errors.append('Имя обязательно')
    if not email:
        errors.append('Email обязателен')
    elif not EMAIL_RE.match(email):
        errors.append('Некорректный формат email')

    if errors:
        return jsonify({'error': ', '.join(errors)}), 400

    user = create_user(name, email)
    return jsonify(user), 201


@api.route('/users/<int:user_id>', methods=['GET'])
def user_detail(user_id):
    user = get_user_by_id(user_id)
    if user is None:
        return jsonify({'error': 'Пользователь не найден'}), 404
    return jsonify(user)
