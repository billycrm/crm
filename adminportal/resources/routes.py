import os
from datetime import datetime
from datetime import timezone, timedelta

import flask
from flask_jwt_extended import create_access_token, verify_jwt_in_request, set_access_cookies, \
    unset_jwt_cookies
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import decode_token

from database.models.token import TokenBlocklist, TokenList
from database.models.logs import Logs
from database.models.user import User
from database.db import db
from hashlib import md5
import json


def get_identity_if_logedin():
    """
    Получает identity пользователя, если он залогинен
    :return: identity пользователя или None
    """
    try:
        verify_jwt_in_request()
        return get_jwt_identity()
    except Exception:
        pass
    return None


def hash_password(password, username):
    """
    Хеширует пароль с солью
    :param password: пароль
    :param username: имя пользователя
    :return: хешированный пароль
    """
    encoded_password = (password + username).encode()
    return md5(encoded_password).hexdigest()

def login():
    """
    Авторизует пользователя
    :return: json ответ с access_token или сообщение об ошибке
    """
    if not flask.request.json:
        return flask.jsonify({"msg": "Missing JSON in request"}), 400
    # get username and password from request (form)
    username = flask.request.json.get('username', None)
    password = flask.request.json.get('password', None)
    email = flask.request.json.get('email', None)
    if not username and not email:
        return flask.jsonify({"msg": "Missing username or email parameter"}), 400
    if not password:
        return flask.jsonify({"msg": "Missing password parameter"}), 400

    if email:  # Если указан email, ищем пользователя по email
        user = User.query.filter_by(email=email).first()
    else:  # Иначе ищем по username
        user = User.query.filter_by(username=username).first()

    if user is None:
        return flask.jsonify({"msg": "Bad username or password"}), 401

    password_hash = hash_password(password, user.username)

    if user is None or (user.password != password and user.password != password_hash):  # Проверяем пароль и хеш пароля
        return flask.jsonify({"msg": "Bad username or password"}), 401

    if not user.email_confirmed:  # Проверяем подтверждение email
        return flask.jsonify({"msg": "Email not confirmed"}), 401

    if not user.user_confirmed:  # Проверяем подтверждение пользователя
        return flask.jsonify({"msg": "User not confirmed"}), 401

    # Блок кода закомментирован, но оставлен для справки (блоклистинг токенов)

    access_token = create_access_token(identity=username)  # Создаем access token

    user.tokens.append(TokenList(token=access_token, type='access'))  # Сохраняем токен в базе
    db.session.commit()

    resp = flask.jsonify({'login': True, 'access_token': access_token})


    # log login action
    db.session.add(Logs(user_id=user.id, action='login', url=flask.request.url))
    db.session.commit()

    return resp


@jwt_required()
def get_current_user_info():
    """
    Возвращает информацию о текущем пользователе
    :return: json ответ с информацией о пользователе или сообщение об ошибке
    """
    identity = get_jwt_identity()
    user = User.query.filter_by(username=identity).first()
    if user is None:
        return flask.jsonify({"msg": "Token is invalid"}), 401

    # log me action
    db.session.add(Logs(user_id=user.id, action='me', url=flask.request.url))
    db.session.commit()

    return flask.jsonify(user.serialize()), 200


@jwt_required()
def set_current_user_info():
    """
    Изменяет информацию о текущем пользователе
    :return: json ответ с сообщением об успехе или ошибке
    """
    if not flask.request.json:
        return flask.jsonify({"msg": "Missing json data"}), 400

    identity = get_jwt_identity()
    user = User.query.filter_by(username=identity).first()
    if user is None:
        return flask.jsonify({"msg": "Token is invalid"}), 401

    allowed_fields = ['username', 'name', 'email', 'password']  # Разрешенные поля для изменения
    fields = dict(flask.request.json)

    for field in fields:  # Проверка на разрешенные поля
        if field not in allowed_fields:
            return flask.jsonify({"msg": f"Field {field} is not allowed"}), 400

    if 'username' in fields:
        user.username = fields['username']
    if 'password' in fields:  # Хешируем пароль, если он меняется
        username = user.username
        password = hash_password(fields['password'], username)
        user.password = password
    if 'email' in fields:
        user.email = fields['email']
    if 'name' in fields:
        user.name = fields['name']

    db.session.commit()

    # log me action
    db.session.add(Logs(user_id=user.id, action='me', url=flask.request.url))
    db.session.commit()

    return flask.jsonify({"msg": "User updated"}), 200


# logout route
@jwt_required()
def modify_token():
    """
    Выход пользователя из системы (добавление токена в блоклист)
    :return: json ответ с сообщением об успехе или ошибке
    """
    identity = get_jwt_identity()
    user = User.query.filter_by(username=identity).first()
    if user is None:
        return flask.jsonify({"msg": "Token is invalid"}), 401

    # log logout action
    db.session.add(Logs(user_id=user.id, action='logout', url=flask.request.url))
    db.session.commit()


    for token in user.tokens:  # Добавляем все access токены пользователя в блоклист
        token_decoded = decode_token(token.token, csrf_value=None, allow_expired=True)
        if token_decoded['type'] == 'access':
            jti = token_decoded['jti']
            ttype = token_decoded['type']
            now = datetime.now(timezone.utc)
            db.session.add(TokenBlocklist(jti=jti, type=ttype, created_at=now))
            user.tokens.remove(token) # Удаляем токен из списка активных токенов пользователя
            db.session.commit()


    resp = flask.jsonify({"msg": "Successfully logged out"})
    return resp


def register():
    """
    Регистрирует нового пользователя
    :return: json ответ с сообщением об успехе или ошибке
    """
    if not flask.request.json:
        return flask.jsonify({"msg": "Missing json data"}), 400

    username = flask.request.json.get('username', None)
    password = flask.request.json.get('password', None)
    email = flask.request.json.get('email', None)
    name = flask.request.json.get('name', None)

    if not username:
        return flask.jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return flask.jsonify({"msg": "Missing password parameter"}), 400
    if not email:
        return flask.jsonify({"msg": "Missing email parameter"}), 400
    if not name:
        return flask.jsonify({"msg": "Missing name parameter"}), 400

    if User.query.filter_by(username=username).first():  # Проверка на уникальность имени пользователя
        return flask.jsonify({"msg": "User with this username already exists"}), 400
    if User.query.filter_by(email=email).first():  # Проверка на уникальность email
        return flask.jsonify({"msg": "User with this email already exists"}), 400

    password = hash_password(password, username)  # Хешируем пароль

    new_user = User(username=username, password=password, email=email, name=name)

    db.session.add(new_user)
    db.session.commit()

    # log add_user action
    db.session.add(Logs(user_id=new_user.id, action='register ' + username, url=flask.request.url))
    db.session.commit()

    return flask.jsonify({"msg": "User created"}), 200


@jwt_required()
def remove_user():
    """
    Удаляет пользователя (только для администратора)
    :return: json ответ с сообщением об успехе или ошибке
    """
    if not flask.request.json:
        return flask.jsonify({"msg": "Missing json data"}), 400

    # check if current user is admin
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if user.admin is False:
        return flask.jsonify({"msg": "You are not admin"}), 403

    user_id = flask.request.json.get('user_id', None)

    if not user_id:
        return flask.jsonify({"msg": "Missing user_id parameter"}), 400

    user2 = User.query.filter_by(id=user_id).first()

    # check if user with this id exists
    if not user2:
        return flask.jsonify({"msg": "User with this id does not exists"}), 404

    # log delete_user action
    db.session.add(Logs(user_id=user.id, action='delete_user ' + user2.username, url=flask.request.url))

    db.session.delete(user2)
    db.session.commit()
    return flask.jsonify({"msg": "User deleted"}), 200


@jwt_required()
def get_users():
    """
    Возвращает список всех пользователей (только для администратора)
    :return: json ответ со списком пользователей или сообщение об ошибке
    """
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if user.admin is False:
        return flask.jsonify({"msg": "You are not admin"}), 403

    # log get_users action
    db.session.add(Logs(user_id=user.id, action='get_users', url=flask.request.url))
    db.session.commit()

    users = User.query.all()
    return flask.jsonify([user.serialize() for user in users]), 200


@jwt_required()
def set_users():
    """
    Изменяет информацию о нескольких пользователях (только для администратора)
    :return: json ответ с сообщением об успехе или ошибке
    """
    if not flask.request.json:
        return flask.jsonify({"msg": "Missing json data"}), 400

    # check if current user is admin
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if user.admin is False:
        return flask.jsonify({"msg": "You are not admin"}), 403

    allowed_fields = user.serialize().keys()  # Разрешенные поля для изменения
    allowed_fields = list(allowed_fields) + ['password']
    users = flask.request.json.get('users', None)

    if not users:
        return flask.jsonify({"msg": "Missing users parameter"}), 400

    for edit_user in users:  # Проверка на разрешенные поля для каждого пользователя
        for field in edit_user:
            if field not in allowed_fields:
                return flask.jsonify({"msg": f"Field {field} is not allowed"}), 400

    for edit_user in users: # Изменение информации о каждом пользователе
        user_id = edit_user.get('user_id', None)
        user2 = User.query.filter_by(id=user_id).first()
        if not user2:
            return flask.jsonify({"msg": "User not found"}), 404

        for field in edit_user:
            if field == 'user_id':
                continue
            if field == 'password':  # Хешируем пароль, если он меняется
                username = user2.username
                password = hash_password(edit_user['password'], username)
                user2.password = password
            elif field == 'email_confirmed' or field == 'user_confirmed' or field == 'admin':  # Приводим к булеву типу
                setattr(user2, field, bool(edit_user[field]))
            else:
                setattr(user2, field, edit_user[field])

        db.session.commit()

    # log edit_user action
    db.session.add(Logs(user_id=user.id, action='edit_users', url=flask.request.url))

    return flask.jsonify({"msg": "Users updated"}), 200


@jwt_required()
def edit_user():
    """
    Изменяет информацию о конкретном пользователе (только для администратора)
    :return: json ответ с сообщением об успехе или ошибке
    """
    if not flask.request.json:
        return flask.jsonify({"msg": "Missing json data"}), 400

    # check if current user is admin
    current_user = get_jwt_identity()
    admin = User.query.filter_by(username=current_user).first()
    if admin.admin is False:
        return flask.jsonify({"msg": "You are not admin"}), 403


    allowed_fields = admin.serialize().keys()  # Разрешенные поля для изменения
    user_id = flask.request.json.get('user_id', None)
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return flask.jsonify({"msg": "User not found"}), 404

    fields = dict(flask.request.json)
    fields.pop('user_id')
    for field in fields:  # Проверка на разрешенные поля
        if field not in allowed_fields:
            return flask.jsonify({"msg": f"Field {field} is not allowed"}), 400

    if 'username' in fields:
        user.username = fields['username']
    if 'password' in fields:  # Хешируем пароль, если он меняется
        username = user.username
        password = hash_password(fields['password'], username)
        user.password = password
    if 'email' in fields:
        user.email = fields['email']
    if 'name' in fields:
        user.name = fields['name']
    if 'email_confirmed' in fields:  # Приводим к булеву типу
        user.email_confirmed = bool(fields['email_confirmed'])
    if 'user_confirmed' in fields:  # Приводим к булеву типу
        user.user_confirmed = bool(fields['user_confirmed'])
    if 'admin' in fields:  # Приводим к булеву типу
        user.admin = bool(fields['admin'])

    db.session.commit()

    # log edit_user action
    db.session.add(Logs(user_id=admin.id, action='edit_user ' + user.username, url=flask.request.url))
    db.session.commit()

    return flask.jsonify({"msg": "User updated"}), 200


def init_routes(app):
    """
    Инициализирует маршруты приложения
    :param app: экземпляр Flask приложения
    """
    app.add_url_rule('/login', 'login', login, methods=['POST'])
    app.add_url_rule('/logout', 'logout', modify_token, methods=['get'])
    app.add_url_rule('/register', 'register', register, methods=['POST'])

    app.add_url_rule('/me', 'me_get', get_current_user_info, methods=['GET'])
    app.add_url_rule('/me', 'me_post', set_current_user_info, methods=['POST'])
    app.add_url_rule('/users', 'users_get', get_users, methods=['GET'])
    app.add_url_rule('/users', 'users_post', set_users, methods=['POST'])

    app.add_url_rule('/remove_user', 'remove_user', remove_user, methods=['DELETE'])
    app.add_url_rule('/edit_user', 'edit_user', edit_user, methods=['POST'])