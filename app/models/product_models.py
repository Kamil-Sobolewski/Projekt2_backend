from datetime import datetime

from app import db


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.Text)
    weight = db.Column(db.Float)
    price = db.Column(db.Float)
    added = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    seller_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    # photos = db.relationship('Photo', backref='product', lazy='dynamic')


# class Photo(db.Model):
#     __tablename__ = 'photos'

#     id = db.Column(db.Integer, primary_key=True)
#     product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
#     filename = db.Column(db.String(64))

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    products = db.relationship('Product', backref='category', lazy='dynamic')
