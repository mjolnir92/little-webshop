# -*- coding: utf-8 -*-
from flask import g
import MySQLdb as mdb

from flask.ext.login import UserMixin


class UserNotFoundError(Exception):
    pass


# Simple user class based on UserMixin
# http://flask-login.readthedocs.org/en/latest/_modules/flask/ext/login.html#UserMixin
class User(UserMixin):
    def __init__(self, login):
        db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
        db.execute('select * from `User` where login=(%s) limit 1', [login])
        entries = db.fetchall()
        if not entries:
            raise UserNotFoundError()
        entry = entries[0]
        self.id = login
        self.user_id = long(entry['idUser'])
        self.login = login
        self.password = entry['password']
        self.first_name = entry['firstName']
        self.last_name = entry['lastName']
        self.street_address = entry['streetAddress']
        self.postal_code = entry['postCode']
        self.postal_town = entry['postTown']
        self.phone = entry['phoneNr']
        self.email = entry['email']
        self.admin = entry['admin'] is 1

    @classmethod
    def get(self, login):
        '''Return user instance of id, return None if not exist'''
        try:
            return self(login)
        except UserNotFoundError:
            return None
