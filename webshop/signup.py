from flask import Blueprint, render_template, request, g
import MySQLdb as mdb

from db_utils import get_all_categories

signup_page = Blueprint('signup_page', __name__, template_folder='templates')


@signup_page.route('/signup')
def signup():
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    db.execute('select * from Customer order by idCustomer desc')
    rows = db.fetchall()
    return render_template('signup.html', category_rows=get_all_categories(db), rows=rows)


@signup_page.route('/signup', methods=['POST'])
def signup_post():
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    statement_insert = 'insert into Customer ' \
                       '(login, password, firstName, lastName, streetAddress, postCode, postTown, phoneNr, email)' \
                       ' values ' \
                       '(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    if "button-save" in request.form:
        db.execute(statement_insert,
                   [
                       request.form['text-login'],
                       request.form['text-password'],
                       request.form['text-firstName'],
                       request.form['text-lastName'],
                       request.form['text-streetAddress'],
                       request.form['text-postCode'],
                       request.form['text-postTown'],
                       request.form['text-phoneNr'],
                       request.form['text-email']
                   ])
        db.connection.commit()
    elif "button-clear" in request.form:
        db.execute('delete from Customer')
        db.connection.commit()
    return signup()
