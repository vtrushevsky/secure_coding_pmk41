from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
# from . import db


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@views.route('/home', methods=['GET', 'POST'])
def home():
    return render_template("home.html")
