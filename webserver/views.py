from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import db, User, Product
from .forms import *
from .tables import *

# from . import db
curr_cart = set([])

views = Blueprint('views', __name__)


@views.route('/myAccount', methods=['GET', 'POST'])
def my_acc():
    return render_template("account.html")


@views.route('/AddToCart/<int:id>', methods=['GET', 'POST'])
def add_cart(id):
    curr_cart.add(id)
    print(curr_cart)
    return redirect(url_for("views.home"))


@views.route('/cart', methods=['GET', 'POST'])
def cart():
    isemty = False
    print("len", len(curr_cart))
    if len(curr_cart) == 0:
        isemty = True
        return render_template("cart.html", isemty=isemty)
    else:
        products = []
        for i in curr_cart:
            products.append(db.session.query(Product).filter_by(id=i).first())
        table = ProductHome(products)
        table.border = True
        return render_template("cart.html", table=table, isemty=isemty)


@views.route('/orders', methods=['GET', 'POST'])
def orders():
    return render_template("orders.html")


@views.route('/home', methods=['GET', 'POST'])
def home():
    products = db.session.query(Product).all()
    table = ProductHome(products)
    table.border = True
    return render_template("home.html", table=table)


@views.route('/admin_tools', methods=['GET', 'POST'])
def user_list():
    if current_user.role == "Administrator":
        users = User.query.all()
        table = AdminUserEdit(users)
        table.border = True
        return render_template("userList.html", table=table)
    else:
        return redirect(url_for("views.home"))


@views.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    if current_user.role == "Administrator":
        user = User.query.filter_by(id=id).first()
        if user:
            form = UserForm(formdata=request.form, obj=user)
            if request.method == 'POST' and form.validate():
                # save edits
                save_changes_user(user, form)
                flash('User updated successfully!')
                return redirect('/admin_tools')
            return render_template('userEditForm.html', form=form)
        else:
            return 'Error loading #{id}'.format(id=id)
    else:
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
def product_list():
    if current_user.role == "Administrator":
        products = db.session.query(Product).all()
        table = AdminProductEdit(products)
        table.border = True
        return render_template("productList.html", table=table)
    else:
        return redirect(url_for("views.home"))


@views.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    if current_user.role == "Administrator":
        product = Product.query.filter_by(id=id).first()
        if product:
            form = ProductForm(formdata=request.form, obj=product)
            if request.method == 'POST' and form.validate():
                save_changes_product(product, form)
                flash('User updated successfully!')
                return redirect('/product_list')
            return render_template('productEditForm.html', form=form)
        else:
            return 'Error loading #{id}'.format(id=id)
    else:
        return redirect(url_for("views.home"))


@views.route('/delete_product/<int:id>', methods=['GET', 'POST'])
def delete_product(id):
    if current_user.role == "Administrator":

        db.session.query(Product).filter_by(id=id).delete()
        db.session.commit()
        return redirect('/product_list')
    else:
        return redirect(url_for("views.home"))


@views.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if current_user.role == "Administrator":
        form = ProductForm(request.form)
        if request.method == 'POST' and form.validate():
            try:
                db.session.add(
                    Product(form.product_name.data, form.barcode.data, form.product_type.data,
                            form.product_number.data))
                db.session.commit()
            except Exception:
                flash("product already exist", category="ProdAddErr")
                return redirect('/add_product')
            return redirect('/product_list')
        return render_template("productAddForm.html", form=form)
    else:
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
def advanced_user_tools():
    return render_template("AdvancedUserTools.html")
