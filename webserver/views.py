from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import db, User

# from . import db


views = Blueprint('views', __name__)


@views.route('/myAccount', methods=['GET', 'POST'])
def my_acc():
    return render_template("account.html")


@views.route('/orders', methods=['GET', 'POST'])
def orders():
    return render_template("orders.html")


@views.route('/home', methods=['GET', 'POST'])
def home():
    return render_template("home.html")


@views.route('/user_list', methods=['GET', 'POST'])
def user_list():
    users = User.query.all()
    return render_template("userList.html", users=users)


@views.route('/editForm', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        user = User.query.filter_by(id=id).first()
        return render_template("editForm.html", user=user)
    else:
        users = User.query.all()
        return render_template("userList.html", users=users)


@views.route('/orders_list', methods=['GET', 'POST'])
def orders_list():
    return render_template("userList.html")


@views.route('/AdvancedUserTools', methods=['GET', 'POST'])
def advanced_user_tools():
    return render_template("AdvancedUserTools.html")
