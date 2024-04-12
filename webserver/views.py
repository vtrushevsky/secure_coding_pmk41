from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user

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


@views.route('/AdminTools', methods=['GET', 'POST'])
def admin_tools():
    return render_template("AdminTools.html")


@views.route('/AdvancedUserTools', methods=['GET', 'POST'])
def advanced_user_tools():
    return render_template("AdvancedUserTools.html")
