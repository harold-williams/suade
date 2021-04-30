import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        print(current_app.config['DATABASE'])
        db = g._database = sqlite3.connect(current_app.config['DATABASE'])
    return db

def import_sql(filename, encoding=None):
    db = get_db()
    cursor = db.cursor()
    if encoding:
        filename = "./application/" + filename
        with open(filename, mode='r', encoding=encoding) as f:  # Using open to specify the encoding so can handle all unicode chars
            cursor.executescript(f.read())
    else:
        with current_app.open_resource(filename, mode='r') as f:
            cursor.executescript(f.read())
    db.commit()
    print(f"Initialised {filename}")


def init_db():
    db = get_db()
    cursor = db.cursor()
    import_sql('db/orders.sql')
    import_sql('db/comissions.sql')
    import_sql('db/promotions.sql')
    import_sql('db/products.sql', 'utf-8')
    import_sql('db/order_lines.sql', 'utf-8')
    import_sql('db/product_promotions.sql')

@click.command('init-db')
@with_appcontext
def initdb_command():
    print("Starting database initialisation")
    init_db()
    print('Initialised the database.')
    
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        
def init_app(app):
    app.teardown_appcontext(close_connection)
    app.cli.add_command(initdb_command)