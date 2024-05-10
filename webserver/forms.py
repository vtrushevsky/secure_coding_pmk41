from wtforms import Form, StringField, SelectField, IntegerField


class UserForm(Form):
    id = StringField('id')
    email = StringField('email')
    surname = StringField('surname')
    name = StringField('name')
    birth_date = StringField('birth_date')
    phone_number = StringField('phone_number')
    role = StringField('role')


class ProductForm(Form):
    id = StringField('id')
    product_name = StringField('product_name')
    barcode = StringField('barcode')
    product_type = StringField('product_type')
    product_number = IntegerField('product_number')
