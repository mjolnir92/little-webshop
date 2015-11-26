from flask import Blueprint, render_template, g, request
import MySQLdb as mdb
from flask.ext.login import current_user

mypage_page = Blueprint('mypage_page', __name__, template_folder='templates')

@mypage_page.route('/mypage')
def my-page():
	return render_template('mypage.html')