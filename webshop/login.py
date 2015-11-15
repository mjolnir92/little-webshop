from flask import Blueprint, render_template, request, g, redirect, url_for
import MySQLdb as mdb

from flask.ext.login import login_user, logout_user
from user import User
from db_utils import get_all_categories

login_page = Blueprint('login_page', __name__, template_folder='templates')


@login_page.route('/login')
def login(show_message=False):
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    return render_template('login.html', all_category_rows=get_all_categories(db), show_message=show_message)


@login_page.route('/login', methods=['POST'])
def login_post():
    user = User.get(request.form['text-username'])
    if user and user.password == request.form['text-password']:
        login_user(user)
        return redirect(url_for('home'))
    else:
        return login(show_message=True)


@login_page.route('/logout')
def logout():
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    logout_user()
    return render_template('login.html', all_category_rows=get_all_categories(db))
