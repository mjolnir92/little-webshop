# -*- coding: utf-8 -*-
def get_all_categories(db):
    db.execute('select * from Category order by name asc')
    return db.fetchall()
