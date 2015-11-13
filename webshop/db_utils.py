
def get_all_categories(db):
    db.execute('select * from AssetCategory order by categoryName asc')
    return db.fetchall()
