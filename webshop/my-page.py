from flask import Blueprint, render_template, g, request
import MySQLdb as mdb
from flask.ext.login import current_user

my-page_page = Blueprint('my-page_page', __name__, template_folder='templates')

@my-page_page.route('/my-page')
def my-page():
	return render_template('my-page.html')