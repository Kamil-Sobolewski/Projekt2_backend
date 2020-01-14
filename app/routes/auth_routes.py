from flask import Blueprint, jsonify, request
from flask_jwt_extended import (jwt_required, create_access_token, get_jwt_identity,
                                get_jwt_claims, current_user, create_refresh_token,
                                jwt_refresh_token_required, fresh_jwt_required, set_access_cookies,
                                set_refresh_cookies, unset_jwt_cookies)

from app.models.account_models import Account
from app import jwt


bp = Blueprint('authorization', __name__, url_prefix='/auth')


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    acc = Account.query.filter_by(email=identity).first()
    if not acc:
        return None
    return acc


@jwt.user_claims_loader
def add_claims_to_access_token(acc):
    return {'role': acc.role.name}


@jwt.user_identity_loader
def user_identity_lookup(acc):
    return acc.email


@bp.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email:
        return jsonify({"msg": "Missing mail parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    acc = Account.query.filter_by(email=email).first()
    if not acc:
        return jsonify({"msg": "User doesn't exist"}), 400
    if not acc.verify_password(password):
        return jsonify({"msg": "Incorrect password"}), 401

    access_token = create_access_token(identity=acc)
    refresh_token = create_refresh_token(identity=acc)
    resp = jsonify({'login': True, 'user_id': acc.id})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)

    return resp, 200


@bp.route('/remove', methods=['POST'])
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200


@bp.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    ret = {
        'access_token': create_access_token(identity=current_user, fresh=False)
    }
    return jsonify(ret), 200


@bp.route('/fresh-login', methods=['POST'])
def fresh_login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email:
        return jsonify({"msg": "Missing mail parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    acc = Account.query.filter_by(email=email).first()
    if not acc:
        return jsonify({"msg": "User doesn't exist"}), 400
    if not acc.verify_password(password):
        return jsonify({"msg": "Incorrect password"}), 401

    ret = {
        'access_token': create_access_token(identity=acc, fresh=True)
    }
    return jsonify(ret), 200


@bp.route('/protected', methods=['GET'])
@fresh_jwt_required
def protected():
    ret = {
        'current_identity': get_jwt_identity(),
        'current_role': get_jwt_claims()['role']
    }
    return jsonify(ret), 200


@bp.route('/protected2', methods=['GET'])
@jwt_required
def protecteddwa():
    if not current_user.role.name == 'Administrator':
        return jsonify({"msg": "You are not admin"}), 400
    return jsonify({"msg": "ok"}), 200
