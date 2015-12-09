from flask import Blueprint, render_template, g, request
import MySQLdb as mdb
from db_utils import get_all_categories

from flask.ext.login import current_user

asset_page = Blueprint('asset_page', __name__, template_folder='templates')


class Review():
    def __init__(self, db, review_row):
        self.id = review_row['idReview']
        self.rating = review_row['rating']
        self.comment = review_row['comment']
        db.execute('select firstName, lastName from User where idUser=%s', [review_row['User_idUser']])
        user = db.fetchall()[0]
        self.user_name = user['firstName'] + " " + user['lastName']
        self.user_id = long(review_row['User_idUser'])


def user_id_valid(user_id):
    return long(current_user.user_id) == long(user_id)


@asset_page.route('/asset_page/<asset_id>', defaults={'asset_id': None})
@asset_page.route('/asset_page/<asset_id>')
def display_asset(asset_id):
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)

    db.execute('select * from Asset where idAsset=%s', [asset_id])
    asset_rows = db.fetchall()
    nav_category_id = asset_rows[0]['Category_idCategory']

    db.execute('select name from Category where idCategory=(%s)', [nav_category_id])
    nav_category_name = db.fetchall()[0]['name']

    db.execute('select * from Review where Asset_idAsset=(%s)', [asset_id])
    review_rows = db.fetchall()
    reviews = []
    current_user_review = None
    for row in review_rows:
        review = Review(db, row)
        if not current_user.is_anonymous and long(current_user.user_id) == long(row['User_idUser']):
            current_user_review = review
        else:
            reviews.append(review)

    return render_template('asset_page.html',
                           all_category_rows=get_all_categories(db),
                           nav_category_id=nav_category_id,
                           nav_category_name=nav_category_name,
                           asset_row=asset_rows[0],
                           reviews=reviews,
                           current_user_review=current_user_review)


@asset_page.route('/asset_add_review/<asset_id>', defaults={'asset_id': None, 'user_id': None}, methods=['POST'])
@asset_page.route('/asset_add_review/<asset_id>/<user_id>', methods=['POST'])
def add_review(asset_id, user_id):
    if not user_id_valid(user_id):
        abort(401)

    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    db.execute('select idReview from Review where User_idUser=(%s) and  Asset_idAsset=%s', [user_id, asset_id])
    current_review = db.fetchall()

    if not current_review:
        db.execute('insert into Review (rating, comment, User_idUser, Asset_idAsset) values (%s,%s,%s,%s)',
                   [request.form['text-rating'], request.form['text-comment'], user_id, asset_id])
        db.connection.commit()
    else:
        db.execute('update Review set rating=%s, comment=%s where User_idUser=%s and Asset_idAsset=%s',
                   [request.form['text-rating'], request.form['text-comment'], user_id, asset_id])
        db.connection.commit()

    return display_asset(asset_id)


@asset_page.route('/asset_remove_review/<asset_id>', defaults={'asset_id': None, 'user_id': None}, methods=['POST'])
@asset_page.route('/asset_remove_review/<asset_id>/<user_id>', methods=['POST'])
def remove_review(asset_id, user_id):
    if not user_id_valid(user_id):
        abort(401)
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    db.execute('delete from Review where User_idUser=%s and Asset_idAsset=%s', (user_id, asset_id))
    db.connection.commit()
    return display_asset(asset_id)
