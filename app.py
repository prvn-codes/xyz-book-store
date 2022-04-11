from flask import Flask, render_template
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root@123'
app.config['MYSQL_DATABASE_DB'] = 'xyzbookstore'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306


mysql.init_app(app)
conn = mysql.connect()

app.secret_key = "super secret key"

@app.route("/home")
def home_route():
    return render_template('home.html')


@app.route("/stocks")
def stocks_route():
    
    return render_template('stocks.html')

@app.route("/add_stock")
def add_stock_route():
    
    return render_template('add_stocks.html')

@app.route("/update_stock")
def update_stock_route():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM book_stock;')
    results = cursor.fetchall()
    return render_template('update_stocks.html',book_stock=results)

@app.route("/search_stock")
def search_stock_route():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM book_stock;')
    results = cursor.fetchall()
    return render_template('search_stocks.html',book_stock=results)


@app.route("/billing")
def billing_route():
    return render_template('billing.html')


@app.route("/lending")
def lending_route():
    return render_template('lending.html')


@app.route("/membership")
def membership_route():
    return render_template('membership.html')


@app.route("/")
def index_route():
    return render_template('index.html')

if __name__ == '__main__':
  app.run(debug=True,port=80)