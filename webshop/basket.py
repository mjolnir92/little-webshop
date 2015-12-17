# -*- coding: utf-8 -*-
import time

from flask import Blueprint, render_template, g, request, abort
import MySQLdb as mdb

from flask.ext.login import current_user
from db_utils import get_all_categories
from enum import Enum

from mail import sendBasketMail

date_time_format = '%Y-%m-%d %H:%M:%S'


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)


class BasketStatus(Enum):
    Active = 0
    Processing = 1
    Sent = 2
    Delivered = 3


basket_page = Blueprint('basket_page', __name__, template_folder='templates')


class Basket():
    def __init__(self, db, basket_row):
        self.id = basket_row['idBasket']
        self.date_time = basket_row['dateTime']
        self.status = basket_row['status']
        self.status_name = BasketStatus(self.status).name
        self.has_back_orders = False
        self.shipping = 50.0
        self.total_sum = self.shipping

        db.execute('select * from BasketRow where Basket_idBasket=%s', [self.id])
        self.rows = db.fetchall()

        for basket_row in self.rows:
            db.execute('select * from Asset where idAsset=%s', [basket_row['Asset_idAsset']])
            asset = basket_row['asset'] = db.fetchall()[0]
            basket_row['asset_order_sum'] = basket_row['amount'] * asset['price']
            self.total_sum += basket_row['asset_order_sum']
            if asset['amount'] - basket_row['amount'] < 0:
                basket_row['back_order'] = abs(asset['amount'] - basket_row['amount'])
                self.has_back_orders = True
            else:
                basket_row['back_order'] = 0


def user_id_valid(user_id):
    return long(current_user.user_id) == long(user_id)


@basket_page.route('/checkout/<user_id>', defaults={'user_id': None, 'basket_id': None}, methods=['POST'])
@basket_page.route('/checkout/<user_id>/<basket_id>', methods=['POST'])
def checkout(user_id=None, basket_id=None):
    if not user_id_valid(user_id):
        abort(401)
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    basket = Basket(db, get_active_basket(user_id))

    if len(basket.rows) > 0:
        for row in basket.rows:
            amountInBasket = row['amount']
            if amountInBasket < 0:
                # Maybe display error message?
                db.connection.rollback()
                break

            db.execute('select amount from Asset where idAsset=%s', [row['Asset_idAsset']])
            amountInStore = db.fetchall()[0]['amount']
            newAmount = amountInStore - amountInBasket
            db.execute('update Asset set amount=%s where idAsset=%s', [newAmount, row['Asset_idAsset']])

        db.execute('update Basket set status=%s where idBasket=%s', [1, basket.id])
        db.connection.commit()

        sendBasketMail(basket, current_user)

    return display_basket(user_id)


@basket_page.route('/basket/<user_id>', defaults={'user_id': None, 'selected_prev_basket_id': None})
@basket_page.route('/basket/<user_id>/<selected_prev_basket_id>')
def display_basket(user_id=None, selected_prev_basket_id=None):
    if not user_id_valid(user_id):
        abort(401)
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    active_basket = Basket(db, get_active_basket(user_id))
    previous_baskets_rows = get_previous_baskets(user_id)
    previous_baskets = []
    for basket_row in previous_baskets_rows:
        previous_baskets.append(Basket(db, basket_row))

    return render_template('basket.html',
                           active_basket=active_basket,
                           previous_baskets=previous_baskets,
                           selected_prev_basket_id=selected_prev_basket_id,
                           all_category_rows=get_all_categories(db))


@basket_page.route('/delete_basket_asset/<user_id>', defaults={'user_id': None, 'asset_id': None}, methods=['POST'])
@basket_page.route('/delete_basket_asset/<user_id>/<asset_id>', methods=['POST'])
def delete_basket_asset(user_id, asset_id):
    if not user_id_valid(user_id):
        abort(401)

    active_basket = get_active_basket(user_id)
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    db.execute('delete from BasketRow where Basket_idBasket=%s and Asset_idAsset=%s', [active_basket['idBasket'], asset_id])
    db.connection.commit()
    return display_basket(user_id)


@basket_page.route('/update_basket_asset/<user_id>', defaults={'user_id': None, 'asset_id': None}, methods=['POST'])
@basket_page.route('/update_basket_asset/<user_id>/<asset_id>', methods=['POST'])
def update_basket_asset(user_id, asset_id):
    if not user_id_valid(user_id):
        abort(401)

    active_basket = get_active_basket(user_id)
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    active_basket_id = active_basket['idBasket']
    amount = long(request.form['text-amount'])
    if amount < 1:
        amount = 1
    db.execute('update BasketRow set amount=%s where Basket_idBasket=%s and Asset_idAsset=%s',
               [amount, active_basket_id, asset_id])
    db.connection.commit()

    return display_basket(user_id)


@basket_page.route('/basket_add/<user_id>', defaults={'user_id': None, 'asset_id': None}, methods=['POST'])
@basket_page.route('/basket_add/<user_id>/<asset_id>', methods=['POST'])
def add_asset(user_id, asset_id):
    if not user_id_valid(user_id):
        abort(401)

    active_basket = get_active_basket(user_id)
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    db.execute('select * from BasketRow where Basket_idBasket=%s', [active_basket['idBasket']])
    active_basket_rows = db.fetchall()
    add_new_asset = True
    for row in active_basket_rows:
        if long(row['Asset_idAsset']) == long(asset_id):
            add_new_asset = False
            break

    active_basket_id = active_basket['idBasket']
    if add_new_asset:
        db.execute('insert into BasketRow (Asset_idAsset, amount, Basket_idBasket) values (%s,%s,%s)',
                   [asset_id, 1, active_basket_id])
        db.connection.commit()
    else:
        db.execute('select amount from BasketRow where Basket_idBasket=%s and Asset_idAsset=%s',
                   [active_basket_id, asset_id])
        new_amount = db.fetchall()[0]['amount'] + 1
        db.execute('update BasketRow set amount=%s where Basket_idBasket=%s and Asset_idAsset=%s',
                   [new_amount, active_basket_id, asset_id])
        db.connection.commit()

    return display_basket(user_id)


def get_active_basket(user_id):
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    db.execute('select * from Basket where User_idUser=%s and status=%s', (user_id, BasketStatus.Active))
    baskets = db.fetchall()
    if len(baskets) is 0:
        db.execute('insert into Basket (dateTime, status, User_idUser) values (%s, %s, %s)',
                   [time.strftime('%Y-%m-%d %H:%M:%S'), 0, user_id])
        db.connection.commit()
        return get_active_basket(user_id)
    return baskets[0]


def get_previous_baskets(user_id):
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    db.execute('select * from Basket where User_idUser=%s and status<>%s order by datetime', (user_id, BasketStatus.Active))
    return db.fetchall()
