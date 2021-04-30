import re
import sqlite3
import os
from flask import Flask, request, g
from application.db import get_db


def get_value(cursor, query, value):
    cursor.execute(query)
    num_customers = cursor.fetchall()[0][0]
    if num_customers:
        return { value : num_customers}
    else:
        return { value : 0 }

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.root_path, 'db\\database.db')
    )
    
    from . import db
    db.init_app(app)
    
    @app.route("/", methods=['GET'])
    def home():
        home_page = """
        <!DOCTYPE html>
        <html>

        <head>
            <title>Suade Api</title>
        </head>

        <body>

        <h1>Enpoint Example</h1>
        <h2>Available at: <a href='/api/report'>/api/report</a></h2>
        </body>
        </html>
        """
        return home_page

    @app.route("/api/report", methods=['GET'])
    def report_generator():
        
        date = request.args.get('date')
        if not date:
            return "No Date Provided</br>Example Query: <a href='/api/report?date=2019-09-29'>/api/report?date=2019-09-29</a>"
        valid_date = r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))'
        valid = re.search(valid_date, date)
        if valid:
            
            report = {}
            date = valid.string
            db = get_db()
            cursor = db.cursor()
            
            # The total number of customers that made an order that day.
            query = f'SELECT COUNT( DISTINCT customer_id) FROM Orders WHERE DATE(Orders.created_at) = DATE(\"{date}\");'
            report.update(get_value(cursor, query, "customers"))
                
            # The total number of items sold on that day.
            query = f"SELECT COUNT(order_id) FROM OrderLine JOIN Orders ON Orders.id = OrderLine.order_id WHERE DATE(Orders.created_at) = DATE(\"{date}\");"
            report.update(get_value(cursor, query, "items"))
            
            

                
                
            return report
        else:
            return "Invalid Date</br>Format: YYYY-MM-DD"
        
        
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1')
