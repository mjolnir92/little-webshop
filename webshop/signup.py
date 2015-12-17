# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, g, redirect, url_for
import MySQLdb as mdb

from db_utils import get_all_categories

signup_page = Blueprint('signup_page', __name__, template_folder='templates')


@signup_page.route('/signup')
def signup(message=None):
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    db.execute('select * from User order by idUser desc')
    rows = db.fetchall()
    return render_template('signup.html', all_category_rows=get_all_categories(db), rows=rows, message=message)


@signup_page.route('/signup', methods=['POST'])
def signup_post():
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)

    statement_insert = 'insert into User ' \
                       '(login, password, firstName, lastName, streetAddress, postCode, postTown, phoneNr, email)' \
                       ' values ' \
                       '(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    try:
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
    except mdb.IntegrityError:
        return signup(message='User name is taken!')

    return redirect(url_for('login_page.login'))
