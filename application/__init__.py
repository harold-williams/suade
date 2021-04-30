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

class Report:
    
    def __init__(self, date, cursor):
        self.report = {}
        self.commissions = {}
        self.promotions = {}
        self.date = date
        self.cursor = cursor    
        
    def get_customers(self):
        # The total number of customers that made an order that day.
        query = f'SELECT COUNT( DISTINCT customer_id) FROM Orders WHERE DATE(Orders.created_at) = DATE(\"{self.date}\");'
        self.report.update(get_value(self.cursor, query, "customers"))
        
    def get_items(self):
        # The total number of items sold on that day.
        query = f"SELECT COUNT(order_id) FROM OrderLine JOIN Orders ON Orders.id = OrderLine.order_id WHERE DATE(Orders.created_at) = DATE(\"{self.date}\");"
        self.report.update(get_value(self.cursor, query, "items"))

    def get_total_discount(self):
        query = f"SELECT SUM(full_price_amount - discounted_amount) FROM OrderLine JOIN Orders ON Orders.id = OrderLine.order_id WHERE discount_rate <> 0 AND DATE(Orders.created_at) = DATE(\"{self.date}\");"
        self.report.update(get_value(self.cursor, query, "total_discount_amount"))

    def get_order_total_avg(self):
        query = f"SELECT AVG(totals) FROM (SELECT SUM(total_amount) AS totals FROM OrderLine JOIN Orders ON Orders.id = OrderLine.order_id WHERE DATE(Orders.created_at) = DATE(\"{self.date}\") GROUP BY order_id);"
        self.report.update(get_value(self.cursor, query, "order_total_avg"))
    
    def get_discount_rate_avg(self):    
        query = f"SELECT AVG(discount_rate) FROM OrderLine JOIN Orders ON Orders.id = OrderLine.order_id WHERE DATE(Orders.created_at) = DATE(\"{self.date}\");"
        self.report.update(get_value(self.cursor, query, "discount_rate_avg"))
        
    def get_commission_total(self):
        query = f"SELECT SUM(total_amount*rate) FROM OrderLine JOIN Orders ON Orders.id = OrderLine.order_id JOIN VendorCommissions ON Orders.vendor_id = VendorCommissions.vendor_id AND DATE(VendorCommissions.date) = DATE(Orders.created_at) WHERE DATE(Orders.created_at) = DATE(\"{self.date}\");"
        self.commissions.update(get_value(self.cursor, query, "total"))
            
    def get_commission_avg(self):
        query = f"SELECT AVG(commissions) FROM (SELECT AVG(total_amount*rate) AS commissions FROM OrderLine JOIN Orders ON Orders.id = OrderLine.order_id JOIN VendorCommissions ON Orders.vendor_id = VendorCommissions.vendor_id AND DATE(VendorCommissions.date) = DATE(Orders.created_at) WHERE DATE(Orders.created_at) = DATE(\"{self.date}\") GROUP BY order_id);"
        self.commissions.update(get_value(self.cursor, query, "order_average"))
            
    def get_promotions(self):
        query = f"SELECT id FROM Promotion;"
        cursor = self.cursor
        cursor.execute(query)
        promos = cursor.fetchall()
        for promotion in promos:
            query = f"SELECT SUM(total_amount*rate) FROM OrderLine JOIN Orders ON Orders.id = OrderLine.order_id JOIN VendorCommissions ON Orders.vendor_id = VendorCommissions.vendor_id AND DATE(VendorCommissions.date) = DATE(Orders.created_at) WHERE DATE(Orders.created_at) = DATE(\"{self.date}\") AND Orders.vendor_id = \"{int(promotion[0])}\";"
            self.promotions.update(get_value(cursor, query, str(int(promotion[0])) ))
            
    def construct_new_report(self):
        self.report = {}
        self.commissions = {}
        self.promotions = {}
        self.get_customers()
        self.get_items()
        self.get_total_discount()
        self.get_order_total_avg()
        self.get_discount_rate_avg()
        self.get_commission_total()
        self.get_commission_avg()
        self.get_promotions()
        self.commissions["promotions"] = self.promotions
        self.report["commissions"] = self.commissions
        return self.report

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
            
            date = valid.string
            db = get_db()
            cursor = db.cursor()
            
            report = Report(date, cursor)
            return report.construct_new_report()
        else:
            return "Invalid Date</br>Format: YYYY-MM-DD"
        
        
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1')
