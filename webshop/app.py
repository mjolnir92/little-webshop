from flask import Flask, g, render_template
from flask_mail import Mail
import MySQLdb as mdb

from flask.ext.login import LoginManager
from browse import browse_page
from signup import signup_page
from login import login_page
from basket import basket_page
from db_utils import get_all_categories
from user import User

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(browse_page)
app.register_blueprint(signup_page)
app.register_blueprint(login_page)
app.register_blueprint(basket_page)

HOST = 'localhost'
DEBUG = True
SECRET_KEY = 'IaWie5geraiciW6w'
USERNAME = 'little-webshop'
PASSWORD = 'little-webshop-password-123'
DATABASE = 'little_webshop'

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'dazieGh3@gmail.com'
MAIL_PASSWORD = ''

app.config.from_object(__name__)
mail = Mail(app)


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
        g.mail = mail
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
