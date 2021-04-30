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
            
            query = f"SELECT SUM(full_price_amount - discounted_amount) FROM OrderLine JOIN Orders ON Orders.id = OrderLine.order_id WHERE discount_rate <> 0 AND DATE(Orders.created_at) = DATE(\"{date}\");"
            report.update(get_value(cursor, query, "total_discount_amount"))
            
            query = f"SELECT AVG(totals) FROM (SELECT SUM(total_amount) AS totals FROM OrderLine JOIN Orders ON Orders.id = OrderLine.order_id WHERE DATE(Orders.created_at) = DATE(\"{date}\") GROUP BY order_id);"
            report.update(get_value(cursor, query, "order_total_avg"))
            
            query = f"SELECT AVG(discount_rate) FROM OrderLine JOIN Orders ON Orders.id = OrderLine.order_id WHERE DATE(Orders.created_at) = DATE(\"{date}\");"
            report.update(get_value(cursor, query, "discount_rate_avg"))
            
            commissions = {}
            query = f"SELECT SUM(total_amount*rate) FROM OrderLine JOIN Orders ON Orders.id = OrderLine.order_id JOIN VendorCommissions ON Orders.vendor_id = VendorCommissions.vendor_id AND DATE(VendorCommissions.date) = DATE(Orders.created_at) WHERE DATE(Orders.created_at) = DATE(\"{date}\");"
            commissions.update(get_value(cursor, query, "total"))
            
            query = f"SELECT AVG(commissions) FROM (SELECT AVG(total_amount*rate) AS commissions FROM OrderLine JOIN Orders ON Orders.id = OrderLine.order_id JOIN VendorCommissions ON Orders.vendor_id = VendorCommissions.vendor_id AND DATE(VendorCommissions.date) = DATE(Orders.created_at) WHERE DATE(Orders.created_at) = DATE(\"{date}\") GROUP BY order_id);"
            commissions.update(get_value(cursor, query, "order_average"))
            
            promotions = {}
            
            query = f"SELECT id FROM Promotion;"
            cursor.execute(query)
            promos = cursor.fetchall()
            for promotion in promos:
                query = f"SELECT SUM(total_amount*rate) FROM OrderLine JOIN Orders ON Orders.id = OrderLine.order_id JOIN VendorCommissions ON Orders.vendor_id = VendorCommissions.vendor_id AND DATE(VendorCommissions.date) = DATE(Orders.created_at) WHERE DATE(Orders.created_at) = DATE(\"{date}\") AND Orders.vendor_id = \"{int(promotion[0])}\";"
                promotions.update(get_value(cursor, query, str(int(promotion[0])) ))
            
            commissions["promotions"] = promotions
            report["commissions"] = commissions
                
            return report
        else:
            return "Invalid Date</br>Format: YYYY-MM-DD"
        
        
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1')
