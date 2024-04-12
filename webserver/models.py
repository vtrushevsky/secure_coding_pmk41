from . import db
from flask_login import UserMixin


# from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True)
    surname = db.Column(db.String(20))
    name = db.Column(db.String(20))
    password = db.Column(db.String(100))
    birth_date = db.Column(db.String(10))
    phone_number = db.Column(db.String(20))
    role = db.Column(db.String(20))
    order = db.relationship('Order', backref='user', lazy=True)

    db.__table_args__ = (
        db.CheckConstraint('phone_number ~* \'^(\\+\\d{1,3}[- ]?)?\\d{10}$\'', name='valid_phone_number'),
        db.CheckConstraint("to_date(birth_date, 'DD.MM.YYYY') IS NOT NULL", name="valid_birth_date_format"),
        db.CheckConstraint("role IN ('Administrator', 'Advanced user', 'User')", name="valid_role"),
    )

    def __init__(self, email, surname, name, birth_date, phone_number, password, role):
        self.email = email
        self.surname = surname
        self.name = name
        self.birth_date = birth_date
        self.phone_number = phone_number
        self.role = role
        self.password = password

    @property
    def get_role(self):
        return self.role


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(40), unique=False)
    barcode = db.Column(db.String(85), unique=True)
    product_type = db.Column(db.String(20))
    product_number = db.Column(db.Integer)
    order = db.relationship('Order', backref='product', lazy=True)

    db.__table_args__ = (
        db.CheckConstraint("barcode ~ '^\d+$'", name="valid_barcode_digits")
    )

    def __init__(self, product_name, barcode, product_type, product_number):
        self.product_name = product_name
        self.barcode = barcode
        self.product_type = product_type
        self.product_number = product_number


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    db.__table_args__ = (
        db.CheckConstraint("to_date(order_date, 'DD.MM.YYYY') IS NOT NULL", name="valid_order_date_format")
    )

    def __init__(self, order_date, user_id, product_id):
        self.order_date = order_date
        self.user_id = user_id
        self.product_id = product_id
