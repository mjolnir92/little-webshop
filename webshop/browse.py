from flask import Blueprint, render_template, request, g
import MySQLdb as mdb

from db_utils import get_all_categories

browse_page = Blueprint('browse_page', __name__, template_folder='templates')


@browse_page.route('/browse/<categoryName>', defaults={'idAsset': None})
@browse_page.route('/browse/<categoryName>/<idAsset>')
def display_category(categoryName=None, idAsset=None):
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)

    if not categoryName:
        db.execute('select * from AssetCategory limit 1')
        first_category = db.fetchall()
        print first_category
        categoryName = first_category[0]["categoryName"]
        print categoryName

    db.execute('select idCategory from AssetCategory where categoryName=(%s)', [categoryName])
    category_id = db.fetchall()[0]["idCategory"]
    categorized_items = []
    db.execute('select * from Asset where AssetCategory_idCategory=(%s)', [category_id])
    assets_in_category = db.fetchall()
    categorized_items.append((categoryName, assets_in_category))
    return render_template('browse.html', category_id=category_id,
                           category_rows=get_all_categories(db), \
                           categorized_items=categorized_items)


@browse_page.route('/browse/delete_asset/<categoryName>', defaults={'idAsset': None}, methods=['POST'])
@browse_page.route('/browse/delete_asset/<categoryName>/<idAsset>', methods=['POST'])
def delete_asset(categoryName, idAsset=None):
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    db.execute('delete from Asset where idAsset=(%s)', [idAsset])
    db.connection.commit()
    return display_category(categoryName)


@browse_page.route('/browse/delete_category/<categoryName>', defaults={'idAssetCategory': None}, methods=['POST'])
@browse_page.route('/browse/delete_category/<categoryName>/<idAssetCategory>', methods=['POST'])
def delete_category(categoryName, idAssetCategory=None):
    print idAssetCategory
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    db.execute('delete from AssetCategory where idCategory=(%s)', [idAssetCategory])
    db.connection.commit()
    return display_category()


@browse_page.route('/browse/add_asset/<categoryName>', methods=['POST'])
def add_asset(categoryName):
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    db.execute('select idCategory from AssetCategory where categoryName=(%s)', [request.form['select-category']])
    category_id = db.fetchall()[0]['idCategory']
    db.execute('insert into Asset '
               '(name, price, amountInStore, imagePath, AssetCategory_idCategory)'
               ' values '
               '(%s, %s, %s, %s, %s)',
               [
                   request.form['text-name'],
                   request.form['text-price'],
                   request.form['text-amountInStore'],
                   request.form['text-imagePath'],
                   category_id
               ])
    db.connection.commit()
    return display_category(categoryName)


@browse_page.route('/browse/add_category/<categoryName>', methods=['POST'])
def add_asset_category(categoryName):
    db = getattr(g, 'db', None).cursor(mdb.cursors.DictCursor)
    db.execute('insert into AssetCategory (categoryName) values (%s)', [request.form['text-categoryName']])
    db.connection.commit()
    return display_category(categoryName)
