from flask import g
import MySQLdb as mdb

from flask.ext.login import UserMixin


class UserNotFoundError(Exception):
    pass


# Simple user class base on UserMixin
# http://flask-login.readthedocs.org/en/latest/_modules/flask/ext/login.html#UserMixin
class User(UserMixin):
    def __init__(self, id):
        db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
        db.execute('select password from Customer where login=(%s)', [id])
        entries = db.fetchall()
        if not entries:
            raise UserNotFoundError()
        self.id = id
        self.password = entries[0]['password']
        self.admin = True

    @classmethod
    def get(self, id):
        '''Return user instance of id, return None if not exist'''
        try:
            return self(id)
        except UserNotFoundError:
            return None
