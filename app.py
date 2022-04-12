from flask import Flask, render_template, request
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Root@123'
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

@app.route("/update_stock",methods=['GET','POST'])
def update_stock_route():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM book_stock;')
    results = cursor.fetchall()
    if request.method == 'POST':
        book_name = request.form.get('select_book_name')
        new_stock = request.form['stock_count']
        cursor.execute("select stock from book_stock where book_name='"+book_name+"';")
        old_stock = cursor.fetchone()
        stock = old_stock[0] + int(new_stock)    
        #print(f"update book_stock set stock = {stock} where book_name = '{book_name}';")
        cursor.execute(f"update book_stock set stock = {stock} where book_name = '{book_name}';")
    return render_template('update_stocks.html',book_stock=results)

@app.route("/view_stock")
def search_stock_route():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM book_stock;')
    results = cursor.fetchall()
    return render_template('view_stocks.html',book_stock=results)


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