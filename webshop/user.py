from flask import g
from flask.ext.login import UserMixin
import MySQLdb as mdb

class UserNotFoundError(Exception):
    pass

# Simple user class base on UserMixin
# http://flask-login.readthedocs.org/en/latest/_modules/flask/ext/login.html#UserMixin
class User(UserMixin):
    '''Simple User class'''
    USERS = {
        # username: password
        'john': 'john',
        'mary': 'mary'
    }

    def __init__(self, id):
        getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
        if not id in self.USERS:
            raise UserNotFoundError()
        self.id = id
        self.password = self.USERS[id]

    @classmethod
    def get(self_class, id):
        '''Return user instance of id, return None if not exist'''

        try:
            return self_class(id)
        except UserNotFoundError:
            return None