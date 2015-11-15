from flask import Blueprint, render_template, request, g, redirect, url_for
import MySQLdb as mdb

from flask.ext.login import login_user, logout_user
from user import User
from db_utils import get_all_categories

basket_page = Blueprint('basket_page', __name__, template_folder='templates')

@basket_page.route('/browse/<>', defaults={'order_by': 'name', 'order': 'asc'})
@basket_page.route('/browse/<category_id>/<order_by>/<order>')
def display_basket():

    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)

    return render_template('basket.html', all_category_rows=get_all_categories(db))
