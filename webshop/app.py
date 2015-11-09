from flask import Flask, g, render_template, request
import MySQLdb

app = Flask(__name__)

HOST = 'localhost'
DEBUG = True
SECRET_KEY = 'IaWie5geraiciW6w'
USERNAME = 'little-webshop'
PASSWORD = 'little-webshop-password-123'
DATABASE = 'little_webshop'

def init_sqlite():
    """ Create a new database or clear the old one """
    g.db = get_db()
    with app.open_resource('schema-sqlite.sql', mode='r') as f:
        g.db.cursor().executescript(f.read())
    g.db.commit()

def init_mysql():
    """ Create a new database or clear the old one """
    g.db = get_db()
    with app.open_resource('schema-mysql.sql', mode='r') as f:
        for line in f:
            g.db.execute(line)
    g.db.commit()

def get_db():
    return MySQLdb.connect(host=HOST, port=2222, user=USERNAME, passwd=PASSWORD, db=DATABASE).cursor()


@app.before_request
def before_request():
    """ This is run when any page is requested """
    try:
        g.db = get_db()
    except Exception as e:
        print(e)


@app.teardown_request
def teardown_request(exception):
    """ This run when the requested page has been served """
    g.db = get_db()
    if g.db is not None:
        g.db.close()
    else:
        print("DB is null")


@app.route("/")
def home():
    """  """
    g.db = get_db()
    g.db.execute('select firstname, lastname from entries order by id desc')
    entries = g.db.fetchall()
    return render_template("home.html", entries=entries)


@app.route('/', methods=['POST'])
def home_post():
    """  """
    if "button-save" in request.form:
        g.db = get_db()
        g.db.execute('insert into entries (firstname, lastname) values (%s, %s)',
                     [request.form['text-firstname'], request.form['text-lastname']])
        g.db.connection.commit()
    elif "button-clear" in request.form:
        g.db = get_db()
        g.db.execute('delete from entries')
        g.db.connection.commit()
    return home()


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.secret_key = SECRET_KEY
    app.run(debug=True, host='127.0.0.1', port=5000)
