from flask import Blueprint, render_template, request, flash, redirect, escape
from flask_login import login_required, current_user
from .models import db, User, Product, Order
from .forms import *
from .tables import *
from .logger import Logger
from datetime import datetime

# from . import db

curr_cart = dict({})
views = Blueprint('views', __name__)


@views.route('/myAccount', methods=['GET', 'POST'])
@login_required
def my_acc():
    return render_template("account.html")


@views.route('/AddToCart/<int:id>', methods=['GET', 'POST'])
@login_required
def add_cart(id):
    if current_user.email in curr_cart.keys():
        temp: set = curr_cart[current_user.email].copy()
        temp.add(id)
        curr_cart.update({current_user.email: temp})
    else:
        temp: set = set({})
        temp.add(id)
        curr_cart.update({current_user.email: temp})
        Logger.log(f'[{datetime.now().strftime("%H:%M:%S.%f")[:10]}] UserID: {current_user.id} '
                   f'added item #{id} to cart.')
    return redirect(url_for("views.home"))


@views.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    print("len", len(curr_cart))
    if current_user.email not in curr_cart.keys():
        return render_template("EmptyCart.html")
    elif len(curr_cart[current_user.email]) == 0:
        return render_template("EmptyCart.html")
    else:
        products = []
        for i in curr_cart[current_user.email]:
            products.append(db.session.query(Product).filter_by(id=i).first())
        table = ProductCart(products)
        table.border = True
        return render_template("cart.html", table=escape(table))


@views.route('/deleteFromCart/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_from_cart(id):
    curr_cart[current_user.email].remove(id)
    Logger.log(f'[{datetime.now().strftime("%H:%M:%S.%f")[:10]}] UserID: {current_user.id} '
               f'deleted item #{id} from cart.')
    return redirect(url_for("views.cart"))


@views.route('/makeOrder', methods=['GET', 'POST'])
@login_required
def make_order():
    user = User.query.filter_by(email=current_user.email).first()
    for i in curr_cart[current_user.email]:
        db.session.add(Order(str(datetime.now()), user.id, i))
        db.session.commit()
        Logger.log(f'[{datetime.now().strftime("%H:%M:%S.%f")[:10]}] UserID: {current_user.id} '
                   f'made new order of productID {i}.')
    curr_cart[current_user.email].clear()
    return redirect(url_for('views.orders'))


@views.route('/AdvancedUserTools', methods=['GET', 'POST'])
@login_required
def ad_user_list():
    if current_user.role == "AdvancedUser":
        users = User.query.all()
        table = ADUserEdit(users)
        table.border = True
        return render_template("ADuserList.html", table=table)
    else:
        return redirect(url_for("views.home"))


@views.route('/orders', methods=['GET', 'POST'])
@login_required
def orders():
    user = User.query.filter_by(email=current_user.email).first()
    orders = db.session.query(Order).filter_by(user_id=user.id).all()
    table = Orders(orders)
    table.border = True
    Logger.log(f'[{datetime.now().strftime("%H:%M:%S.%f")[:10]}] UserID: {current_user.id} '
               f'retrieved own product orders.')
    return render_template("orders.html", table=escape(table))


@views.route('/', methods=['GET', 'POST'])
@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    products = db.session.query(Product).all()
    table = ProductHome(products)
    table.border = True
    return render_template("home.html", table=escape(table))


@views.route('/admin_tools', methods=['GET', 'POST'])
@login_required
def user_list():
    if current_user.role == "Administrator":
        users = User.query.all()
        table = AdminUserEdit(users)
        table.border = True
        Logger.log(f'[{datetime.now().strftime("%H:%M:%S.%f")[:10]}] UserID: {current_user.id} '
                   f'(Administrator) retrieved user-list.')
        return render_template("userList.html", table=escape(table))
    else:
        return redirect(url_for("views.home"))


@views.route('/edit_user/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    if current_user.role == "Administrator":
        user = User.query.filter_by(id=id).first()
        if user:
            form = UserForm(formdata=request.form, obj=user)
            if request.method == 'POST' and form.validate():
                # save edits
                save_changes_user(user, form)
                Logger.log(f'[{datetime.now().strftime("%H:%M:%S.%f")[:10]}] UserID: {current_user.id} '
                           f'(Administrator) edited user {current_user.id} ({current_user.email}).')
                flash('User updated successfully!')
                return redirect('/admin_tools')
            return render_template('userEditForm.html', form=form)
        else:
            Logger.log(f'[{datetime.now().strftime("%H:%M:%S.%f")[:10]}] UserID: {current_user.id} '
                       f'(Administrator) attempted to edit user UNSUCCESSFULLY.')
            return 'Error loading #{id}'.format(id=id)
    else:
        Logger.log(f'[{datetime.now().strftime("%H:%M:%S.%f")[:10]}] UserID: {current_user.id} '
                   f'(NOT Administrator) attempted to edit user. ALARM.')
        return redirect(url_for("views.home"))


def save_changes_user(user, form, new=False):
    user.email = form.email.data
    user.surname = form.surname.data
    user.name = form.name.data
    user.birth_date = form.birth_date.data
    user.phone_number = form.phone_number.data
    user.role = form.role.data
    if new:
        db.session.add(user)
    db.session.commit()


@views.route('/product_list', methods=['GET', 'POST'])
@login_required
def product_list():
    if current_user.role == "Administrator":
        products = db.session.query(Product).all()
        table = AdminProductEdit(products)
        table.border = True
        return render_template("productList.html", table=escape(table))
    else:
        return redirect(url_for("views.home"))


@views.route('/edit_product/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    if current_user.role == "Administrator":
        product = Product.query.filter_by(id=id).first()
        if product:
            form = ProductForm(formdata=request.form, obj=product)
            if request.method == 'POST' and form.validate():
                save_changes_product(product, form)
                Logger.log(f'[{datetime.now().strftime("%H:%M:%S.%f")[:10]}] UserID: {current_user.id} '
                           f'(Administrator) edited productID {id}.')
                flash('User updated successfully!')
                return redirect('/product_list')
            return render_template('productEditForm.html', form=form)
        else:
            Logger.log(f'[{datetime.now().strftime("%H:%M:%S.%f")[:10]}] UserID: {current_user.id} '
                       f'(Administrator) edited productID {id} UNSUCCESSFULLY.')
            return 'Error loading #{id}'.format(id=id)
    else:
        Logger.log(f'[{datetime.now().strftime("%H:%M:%S.%f")[:10]}] UserID: {current_user.id} '
                   f'(NOT Administrator) attempted to edit product.')
        return redirect(url_for("views.home"))


@views.route('/delete_product/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_product(id):
    if current_user.role == "Administrator":
        db.session.query(Product).filter_by(id=id).delete()
        db.session.commit()
        Logger.log(f'[{datetime.now().strftime("%H:%M:%S.%f")[:10]}] UserID: {current_user.id} '
                   f'(Administrator) deleted productID {id}.')
        return redirect('/product_list')
    else:
        Logger.log(f'[{datetime.now().strftime("%H:%M:%S.%f")[:10]}] UserID: {current_user.id} '
                   f'(NOT Administrator) attempted to delete  productID {id}.')
        return redirect(url_for("views.home"))


@views.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.role == "Administrator":
        form = ProductForm(request.form)
        if request.method == 'POST' and form.validate():
            try:
                db.session.add(
                    Product(form.product_name.data, form.barcode.data, form.product_type.data,
                            form.product_number.data))
                db.session.commit()
                Logger.log(f'[{datetime.now().strftime("%H:%M:%S.%f")[:10]}] UserID: {current_user.id} '
                           f'(Administrator) added product {form.product_name}.')
            except Exception:
                flash("product already exist", category="ProdAddErr")
                Logger.log(f'[{datetime.now().strftime("%H:%M:%S.%f")[:10]}] UserID: {current_user.id} '
                           f'(Administrator) added product {form.product_name}, but product already exists.')
                return redirect('/add_product')
            return redirect('/product_list')
        return render_template("productAddForm.html", form=form)
    else:
        Logger.log(f'[{datetime.now().strftime("%H:%M:%S.%f")[:10]}] UserID: {current_user.id} '
                   f'IS NOT Administrator but attempted to add a product.')
        return redirect(url_for("views.home"))


def save_changes_product(prod, form, new=False):
    prod.product_name = form.product_name.data
    prod.barcode = form.barcode.data
    prod.product_type = form.product_type.data
    prod.product_number = form.product_number.data
    if new:
        db.session.add(prod)
    db.session.commit()


@views.route('/AdvancedUserTools', methods=['GET', 'POST'])
@login_required
def advanced_user_tools():
    return render_template("AdvancedUserTools.html")


@views.after_request  # VULNERABILITY prevention - clickjacking
def set_x_frame_options(response):
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return response
