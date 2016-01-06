# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, g
import MySQLdb as mdb
from flask.ext.login import current_user
from db_utils import get_all_categories

browse_page = Blueprint('browse_page', __name__, template_folder='templates')


def validate_order_by(order_by):
    if order_by in ('name', 'price', 'amount'):
        return order_by
    return 'name'


def validate_order(order):
    if order in ('asc', 'desc'):
        return order
    return 'asc'


@browse_page.route('/browse/<category_id>', defaults={'order_by': 'name', 'order': 'asc'})
@browse_page.route('/browse/<category_id>/<order_by>/<order>')
def display_category(category_id=None, order_by='name', order='asc', error_message=None):
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    try:
        long(category_id)
    except:
        category_id = None
    if not category_id:
        db.execute('select * from Category order by name asc limit 1')
        first_category = db.fetchall()
        category_id = first_category[0]["idCategory"]

    db.execute('select name from Category where idCategory=(%s)', [category_id])
    nav_category_name = db.fetchall()[0]['name']
    nav_category_id = category_id

    order_by = validate_order_by(order_by)
    order = validate_order(order)
    db.execute('select * from Asset where Category_idCategory=%s order by %s %s' % (nav_category_id, order_by, order))
    nav_category_asset_row_list = db.fetchall()
    return render_template('browse.html',
                           error_message=error_message,
                           order=order,
                           order_by=order_by,
                           nav_category_id=nav_category_id,
                           nav_category_name=nav_category_name,
                           nav_category_asset_row_list=nav_category_asset_row_list,
                           all_category_rows=get_all_categories(db))


@browse_page.route('/browse/update_asset/<category_id>', defaults={'asset_id': None}, methods=['POST'])
@browse_page.route('/browse/update_asset/<category_id>/<asset_id>', methods=['POST'])
def update_asset(category_id, asset_id):
    if current_user.admin:
        db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
        db.execute('update Asset set '
                   'name=%s, '
                   'price=%s, '
                   'amount=%s, '
                   'imagePath=%s, '
                   'Category_idCategory=%s '
                   'where idAsset=%s',
                   [
                       request.form['text-name'],
                       request.form['text-price'],
                       request.form['text-amount'],
                       request.form['text-imagePath'],
                       request.form['select-category'],
                       asset_id
                   ])
        db.connection.commit()

    return display_category(category_id)


@browse_page.route('/browse/delete_asset/<category_id>', defaults={'asset_id': None}, methods=['POST'])
@browse_page.route('/browse/delete_asset/<category_id>/<asset_id>', methods=['POST'])
def delete_asset(category_id, asset_id=None):
    if current_user.admin:
        db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
        db.execute('delete from Asset where idAsset=(%s)', [asset_id])
        db.connection.commit()
    return display_category(category_id)


@browse_page.route('/browse/delete_category/<category_id>', methods=['POST'])
def delete_category(category_id):
    if current_user.admin:
        try:
            db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
            db.execute('delete from Category where idCategory=(%s)', [category_id])
            db.connection.commit()
        except mdb.IntegrityError as e:
            return display_category(category_id, error_message="Category must be empty before removal.")
    return display_category()


@browse_page.route('/browse/add_asset/<category_id>', methods=['POST'])
def add_asset(category_id):
    if current_user.admin:
        db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
        db.execute('insert into Asset '
                   '(name, price, amount, imagePath, Category_idCategory)'
                   ' values '
                   '(%s, %s, %s, %s, %s)',
                   [
                       request.form['text-name'],
                       request.form['text-price'],
                       request.form['text-amount'],
                       request.form['text-imagePath'],
                       request.form['select-category']
                   ])
        db.connection.commit()
    return display_category(category_id)


@browse_page.route('/browse/add_category/<category_id>', methods=['POST'])
def add_category(category_id):
    if current_user.admin:
        if len(request.form['text-category_name']) > 0:
            db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
            db.execute('insert into Category (name) values (%s)', [request.form['text-category_name']])
            db.connection.commit()
            db.execute('select * from Category order by idCategory desc limit 1')
            return display_category(str(db.fetchall()[0]['idCategory']))

    return display_category(category_id)
