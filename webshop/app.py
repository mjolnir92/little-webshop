from flask import Flask, g, render_template, request, flash, url_for, redirect
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user
from browse import browse_page
from signup import signup_page
from login import login_page
from db_utils import get_all_categories

import MySQLdb as mdb
from user import User

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


app.register_blueprint(browse_page)
app.register_blueprint(signup_page)
app.register_blueprint(login_page)


HOST = 'localhost'
DEBUG = True
SECRET_KEY = 'IaWie5geraiciW6w'
USERNAME = 'little-webshop'
PASSWORD = 'little-webshop-password-123'
DATABASE = 'little_webshop'

@login_manager.user_loader
def load_user(id):
    return User.get(id)

def connect_db():
    return mdb.connect(host=HOST, port=2222, user=USERNAME, passwd=PASSWORD, db=DATABASE)


@app.before_request
def before_request():
    """ This is run when any page is requested """
    try:
        g.db = connect_db()
    except Exception as e:
        print e

@login_manager.user_loader
def load_user(userid):
	return User.get(userid)

@app.teardown_request
def teardown_request(exception):
    """ This run when the requested page has been served """
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
    else:
        print "DB was null!"


@app.route('/about')
def about():
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    return render_template('about.html', all_category_rows=get_all_categories(db))


@app.route("/")
def home():
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    return render_template('home.html', all_category_rows=get_all_categories(db))

if __name__ == '__main__':
    app.secret_key = SECRET_KEY
    app.run(debug=True, host='192.168.1.2', port=5000)
    # app.run(debug=True, host='127.0.0.1', port=5000)
