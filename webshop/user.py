from flask import g
import MySQLdb as mdb

from flask.ext.login import UserMixin


class UserNotFoundError(Exception):
    pass


# Simple user class base on UserMixin
# http://flask-login.readthedocs.org/en/latest/_modules/flask/ext/login.html#UserMixin
class User(UserMixin):
    def __init__(self, login):
        db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
        db.execute('select * from `User` where login=(%s) limit 1', [login])
        entries = db.fetchall()
        if not entries:
            raise UserNotFoundError()
        self.id = login
        self.user_id = long(entries[0]['idUser'])
        self.login = login
        self.password = entries[0]['password']
        self.first_name = entries[0]['firstName']
        self.last_name = entries[0]['lastName']
        self.admin = entries[0]['admin'] is 1

    @classmethod
    def get(self, login):
        '''Return user instance of id, return None if not exist'''
        try:
            return self(login)
        except UserNotFoundError:
            return None
