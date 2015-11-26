from flask import Blueprint, render_template, g, request
import MySQLdb as mdb
from flask.ext.login import current_user
from db_utils import get_all_categories

mypage_page = Blueprint('mypage_page', __name__, template_folder='templates')

@mypage_page.route('/mypage')
def mypage():
	db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
	return render_template('mypage.html', all_category_rows=get_all_categories(db))