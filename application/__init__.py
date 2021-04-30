from flask import Flask
app = Flask(__name__)

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
        return "Placeholder API"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=105)
