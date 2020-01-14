from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app import db
from app.models.account_models import Account
from app.models.schemas import RoleSchema, AccountSchema

bp = Blueprint('accounts', __name__, url_prefix='/accounts')


@bp.route('/')
def get_all_accounts():
    schema = AccountSchema(many=True)
    acc_list = Account.query.all()
    return jsonify(schema.dump(acc_list))


@bp.route('/<int:_id>')
def get_one_account(_id):
    schema = AccountSchema()
    acc = Account.query.filter_by(id=_id).first()
    return jsonify(schema.dump(acc))


@bp.route('/create', methods=['POST'])
def create_account():
    data = request.get_json()
    print(data)
    new_acc = Account(email=data['email'], password=data['password'])
    db.session.add(new_acc)
    db.session.commit()
    schema = AccountSchema()
    return jsonify(schema.dump(new_acc))


@bp.route('/<int:_id>/delete', methods=['POST'])
def delete_account(_id):
    acc = Account.query.filter_by(id=_id).first()
    if acc:
        db.session.delete(acc)
        db.session.commit()
        return jsonify({'message': 'Account has been removed'})
    else:
        return jsonify({'message': 'Account doesn\'t exist'})
