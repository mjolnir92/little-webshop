import time

from flask import Blueprint, render_template, g, request
import MySQLdb as mdb
import math

from db_utils import get_all_categories


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)


BasketStatus = enum('OPEN', 'PROCESSING', 'SENT', 'DELIVERED')

basket_page = Blueprint('basket_page', __name__, template_folder='templates')


@basket_page.route('/basket/<user_id>', defaults={'user_id': None})
@basket_page.route('/basket/<user_id>')
def display_basket(user_id=None, order_id=None):
    # TODO: auth
    open_basket = get_open_basket(user_id)

    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    db.execute('select * from BasketRow where Basket_idBasket=%s', [open_basket['idBasket']])
    open_basket_rows = db.fetchall()

    # Append the Asset rows to the Basket rows
    basket_total_sum = 0
    basket_back_orders = False
    for basket_row in open_basket_rows:
        db.execute('select * from Asset where idAsset=%s', [basket_row['Asset_idAsset']])
        asset = basket_row['asset'] = db.fetchall()[0]
        # Prices
        basket_row['asset_order_sum'] = basket_row['amount'] * asset['price']
        basket_total_sum += basket_row['asset_order_sum']
        # Back order
        if asset['amount'] - basket_row['amount'] < 0:
            basket_row['back_order'] =  abs(asset['amount'] - basket_row['amount'])
            basket_back_orders = True
        else:
            basket_row['back_order'] = 0
    basket_shipping = 50.0
    return render_template('basket.html',
                           all_category_rows=get_all_categories(db),
                           basket=open_basket_rows,
                           basket_shipping=basket_shipping,
                           basket_total_sum=basket_total_sum + basket_shipping,
                           basket_back_orders=basket_back_orders)


@basket_page.route('/delete_basket_asset/<user_id>', defaults={'user_id': None, 'asset_id': None}, methods=['POST'])
@basket_page.route('/delete_basket_asset/<user_id>/<asset_id>', methods=['POST'])
def delete_basket_asset(user_id, asset_id):
    # TODO: auth, check asset_id
    open_basket = get_open_basket(user_id)
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    db.execute('delete from BasketRow where Basket_idBasket=%s and Asset_idAsset=%s', [open_basket['idBasket'], asset_id])
    db.connection.commit()
    return display_basket(user_id)


@basket_page.route('/update_basket_asset/<user_id>', defaults={'user_id': None, 'asset_id': None}, methods=['POST'])
@basket_page.route('/update_basket_asset/<user_id>/<asset_id>', methods=['POST'])
def update_basket_asset(user_id, asset_id):
    # TODO: auth, check asset_id
    open_basket = get_open_basket(user_id)
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    open_basket_id = open_basket['idBasket']
    amount = long(request.form['text-amount'])
    if amount < 1:
        amount = 1
    db.execute('update BasketRow set amount=%s where Basket_idBasket=%s and Asset_idAsset=%s',
               [amount, open_basket_id, asset_id])
    db.connection.commit()

    return display_basket(user_id)


@basket_page.route('/basket_add/<user_id>', defaults={'user_id': None, 'asset_id': None}, methods=['POST'])
@basket_page.route('/basket_add/<user_id>/<asset_id>', methods=['POST'])
def add_asset(user_id, asset_id):
    # TODO: auth, check asset_id
    open_basket = get_open_basket(user_id)
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    db.execute('select * from BasketRow where Basket_idBasket=%s', [open_basket['idBasket']])
    open_basket_rows = db.fetchall()
    add_new_asset = True
    for row in open_basket_rows:
        if long(row['Asset_idAsset']) == long(asset_id):
            add_new_asset = False
            break

    open_basket_id = open_basket['idBasket']
    if add_new_asset:
        db.execute('insert into BasketRow (Asset_idAsset, amount, Basket_idBasket) values (%s,%s,%s)',
                   [asset_id, 1, open_basket_id])
        db.connection.commit()
    else:
        db.execute('select amount from BasketRow where Basket_idBasket=%s and Asset_idAsset=%s',
                   [open_basket_id, asset_id])
        new_amount = db.fetchall()[0]['amount'] + 1
        db.execute('update BasketRow set amount=%s where Basket_idBasket=%s and Asset_idAsset=%s',
                   [new_amount, open_basket_id, asset_id])
        db.connection.commit()

    return display_basket(user_id)


def get_open_basket(user_id):
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    db.execute('select * from Basket where User_idUser=%s and status=%s', (user_id, BasketStatus.OPEN))
    baskets = db.fetchall()
    if len(baskets) is 0:
        db.execute('insert into Basket (dateTime, status, User_idUser) values (%s, %s, %s)',
                   [time.strftime('%Y-%m-%d %H:%M:%S'), 0, user_id])
        db.connection.commit()
        return get_open_basket(user_id)
    return baskets[0]
