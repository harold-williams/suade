import re
from flask import Flask, request

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
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
            return "Placeholder API"
        else:
            return "Invalid Date</br>Format: YYYY-MM-DD"
        
        
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1')
