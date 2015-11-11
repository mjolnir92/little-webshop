from flask import Flask, g, render_template, request
import MySQLdb as mdb

app = Flask(__name__)

HOST = 'localhost'
DEBUG = True
SECRET_KEY = 'IaWie5geraiciW6w'
USERNAME = 'little-webshop'
PASSWORD = 'little-webshop-password-123'
DATABASE = 'little_webshop'


def connect_db():
    return mdb.connect(host=HOST, port=2222, user=USERNAME, passwd=PASSWORD, db=DATABASE)


@app.before_request
def before_request():
    """ This is run when any page is requested """
    try:
        g.db = connect_db()
    except Exception as e:
        print e


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
    return render_template('about.html')


@app.route("/")
def home():
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    db.execute('select * from AssetCategory order by idCategory desc')
    category_rows = db.fetchall()
    categorized_items = []
    for category_row in category_rows:
        db.execute('select * from Asset where AssetCategory_idCategory=(%s)', [category_row["idCategory"]])
        assets_in_category = db.fetchall()
        categorized_items.append( (category_row["categoryName"], assets_in_category) )
    return render_template('home.html', category_rows=category_rows, categorized_items=categorized_items)


@app.route('/', methods=['POST'])
def home_post():
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    if "button-save-category" in request.form:
        db.execute('insert into AssetCategory (categoryName) values (%s)',
                   [request.form['text-categoryName']])
        db.connection.commit()
    if "button-save-asset" in request.form:
        db.execute('select idCategory from AssetCategory where categoryName=(%s)',
                   [request.form['select-category']])
        idCategory = db.fetchall()[0]['idCategory']
        db.execute( 'insert into Asset '
                    '(name, price, amountInStore, imagePath, AssetCategory_idCategory)'
                    ' values '
                    '(%s, %s, %s, %s, %s)',
                   [
                       request.form['text-name'],
                       request.form['text-price'],
                       request.form['text-amountInStore'],
                       request.form['text-imagePath'],
                       idCategory
                   ])
        db.connection.commit()
    elif "button-clear-asset" in request.form:
        db.execute('delete from Asset')
    elif "button-clear-category" in request.form:
        db.execute('delete from Category')
    db.connection.commit()
    return home()


@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/signup')
def signup():
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    db.execute('select * from Customer order by idCustomer desc')
    rows = db.fetchall()
    return render_template('signup.html', rows=rows)


@app.route('/signup', methods=['POST'])
def signup_post():
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    print("signup")
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


if __name__ == '__main__':
    app.secret_key = SECRET_KEY
    app.run(debug=True, host='127.0.0.1', port=5000)
