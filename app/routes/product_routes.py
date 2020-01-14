from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
# import uuid
import json
import os

from app import db
from app.models.product_models import Product, Category
from app.models.schemas import ProductSchema, CategorySchema

bp = Blueprint('products', __name__, url_prefix='/products')


@bp.route('/add', methods=['POST'])
def add_product():
    data = json.loads(request.data)
    product = data['product']
    category = Category.query.filter_by(name=product['category']).first()
    new_product = Product(name=product['name'], description=product['description'],
                          weight=product['weight'], price=product['price'],
                          category=category)
    db.session.add(new_product)
    db.session.commit()
    schema = ProductSchema()
    return jsonify({'message': 'Product has been added',
                    'product': schema.dump(new_product)})
    # data = json.loads(dict(request.form)['data'])
    # files = request.files.getlist('files')
    # for _file in files:
    #     _file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], _file.filename))
    #     new_photo = Photo(filename=_file.filename, product=new_product)
    #     db.session.add(new_photo)


@bp.route('/all', methods=["GET"])
def get_all_products():
    schema = ProductSchema(many=True)
    prod_list = Product.query.all()

    schema2 = CategorySchema(many=True)
    cat_list = Category.query.all()

    return jsonify({"products": schema.dump(prod_list),
                    "categories": schema2.dump(cat_list)})


@bp.route('/<int:_id>')
def get_one_product(_id):
    schema = ProductSchema()
    acc = Product.query.filter_by(id=_id).first()
    return jsonify(schema.dump(acc))


@bp.route('/<int:_id>/delete', methods=['DELETE'])
def delete_product(_id):
    product = Product.query.filter_by(id=_id).first()
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product has been removed'})
    else:
        return jsonify({'message': "Error"})


@bp.route('/<int:_id>/edit', methods=['POST'])
def edit_product(_id):
    old_product = Product.query.get_or_404(_id)
    data = json.loads(request.data)
    product = data['product']
    category = Category.query.filter_by(id=product['category_id']).first()
    old_product.name = product['name']
    old_product.description = product['description']
    old_product.price = product['price']
    old_product.weight = product['weight']
    old_product.category = category

    db.session.commit()
    schema = ProductSchema()
    return jsonify({'message': 'Product has been edited',
                    'product': schema.dump(old_product)})
