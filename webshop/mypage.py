from flask import Blueprint, render_template, g, request, url_for
import MySQLdb as mdb
from flask.ext.login import current_user
from db_utils import get_all_categories

mypage_page = Blueprint('mypage_page', __name__, template_folder='templates')

@mypage_page.route('/mypage')
def mypage(message=None):
	db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
	#db.execute('select * from User order by idUser desc')
	#rows = db.fetchall()
	return render_template('mypage.html', all_category_rows=get_all_categories(db), message=message)

@mypage_page.route('/mypage', methods=['POST'])
def edit_post():
	db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)

	try:
		db.execute(
		'update User set '
		'login=%s, '
		'password=%s, '
		'firstName=%s, '
		'lastName=%s, '
		'streetAddress=%s, '
		'postCode=%s, '
		'postTown=%s, '
		'phoneNr=%s, '
		'email=%s '
		'where idUser=%s',
		[
		request.form['text-login'],
		request.form['text-password'],
		request.form['text-firstName'],
		request.form['text-lastName'],
		request.form['text-streetAddress'],
		request.form['text-postCode'],
		request.form['text-postTown'],
		request.form['text-phoneNr'],
		request.form['text-email'],
		current_user.user_id
		]
		)
	db.connection.commit()
	except mdb.IntegrityError:
		return signup(message='User name is taken!')
	return redirect(url_for('mypage_page.mypage'))