from flask_table import Table, Col, LinkCol, ButtonCol
from flask import url_for


class AdminUserEdit(Table):
    id = Col('Id', show=False)
    email = Col('email')
    surname = Col('surname')
    name = Col('name')
    birth_date = Col('birth_date')
    phone_number = Col('phone_number')
    role = Col('role')
    edit = LinkCol('Edit', 'views.edit_user', url_kwargs=dict(id='id'))


class AdminProductEdit(Table):
    id = Col('id', show=False)
    product_name = Col('product_name')
    barcode = Col('barcode')
    product_type = Col('product_type')
    product_number = Col('product_number')
    order = Col('order')
    edit = LinkCol('Edit', 'views.edit_product', url_kwargs=dict(id='id'))
