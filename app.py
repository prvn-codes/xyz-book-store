
from flask import Flask, render_template, request, redirect, url_for
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'mysql'
app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_PORT'] = 3306


mysql.init_app(app)
conn = mysql.connect()

with open("./db/init.sql",'r') as file1:
    sql_cmds = file1.read()

sql_cmds1 = sql_cmds.split(";")

for i in range(0,len(sql_cmds1)-1):
    query = sql_cmds1[i] + ';'
    cursor = conn.cursor()
    cursor.execute(query)
conn.commit() 
conn.close()
app.config['MYSQL_DATABASE_DB'] = 'xyzbookstore'
conn = mysql.connect()

app.secret_key = "super secret key"

@app.route("/home")
def home_route():
    return render_template('home.html')


@app.route("/stocks")
def stocks_route():
    return render_template('stocks.html')

@app.route("/add_stock",methods=['GET','POST'])
def add_stock_route():
    conn = mysql.connect()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        book_name = request.form['book_name']
        book_desc = request.form['book_desc']
        author_info = request.form['author_info']
        stock = request.form['stock']
        print(book_name + " " + book_desc + " " + author_info)
        query = f"INSERT INTO book_stock(book_name,book_desc,author_info,stock) VALUES('{book_name}','{book_desc}','{author_info}','{stock}');"
        cursor.execute(query)
        conn.commit()
    cursor.close()
    conn.close()
    return render_template('add_stocks.html')

@app.route("/update_stock",methods=['GET','POST'])
def update_stock_route():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM book_stock;')
    results = cursor.fetchall()
    if request.method == 'POST':
        book_name = request.form['select_book_name']
        new_stock = request.form['stock_count']
        cursor.execute("select stock from book_stock where book_name='"+book_name+"';")
        old_stock = cursor.fetchone()
        stock = int(new_stock)
        if old_stock:
            stock = old_stock[0] + int(new_stock)
        query = "UPDATE book_stock SET stock = "+str(stock)+" WHERE book_name = '" + book_name +"';"
        cursor.execute(query)
        conn.commit()
        print(query)
    cursor.close()
    conn.close()
    return render_template('update_stocks.html',book_stock=results)

@app.route("/view_stock")
def search_stock_route():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM book_stock;')
    results = cursor.fetchall()
    print(results)
    return render_template('view_stocks.html',book_stock=results)


@app.route("/billing",methods=['GET','POST'])
def billing_route():
    if request.method == 'POST':
        conn = mysql.connect()
        cursor = conn.cursor()
        books = request.form['books_list']
        price_ = request.form['price_list']
        query = "INSERT INTO bill(books,price) VALUES('"+books+"','"+price_+"');"
        #print(query)
        cursor.execute(query)
        conn.commit()
        return redirect(url_for('print_bill_route'))
    return render_template('billing.html')


@app.route('/print_bill')
def print_bill_route():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select * from bill")
    results = cursor.fetchall()
    result = results[len(results)-1]
    books = result[1].split(",")
    price_ = result[2].split(",")
    bills = list()
    total = 0
    print("=>",len(books),books)
    for i in range(0,len(books)):
         bills.append(list((books[i],price_[i])))
         total += int(price_[i])
    bills.append(list(("Total",total)))     
    return render_template('print_bill.html',bills=bills)


@app.route("/lending")
def lending_route():
    return render_template('lending.html')


@app.route("/membership")
def membership_route():
    return render_template('membership.html')

@app.route("/add_member",methods=['GET','POST'])
def add_member_route():
    if request.method == 'POST':
        conn = mysql.connect()
        cursor = conn.cursor()
        mname = request.form['member_name']
        memail = request.form['member_email']
        duration = request.form['duration']
        print(f"INSERT INTO membership(mname,email,duration) values('{mname}','{memail}'.'{duration}')")
        cursor.execute(f"INSERT INTO membership(mname,email,duration) values('{mname}','{memail}',{duration})")
        conn.commit()
    return render_template('add_member.html')

@app.route('/update_member',methods=['POST','GET'])
def update_member_route():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM membership;')
    results = cursor.fetchall()
    if request.method == 'POST':
        mem_name = request.form['select_memeber_name']
        duration = request.form['duration']
        cursor.execute("select duration from membership where mname='"+mem_name+"';")
        old_duration = cursor.fetchone()
        duration = int(duration)
        if old_duration:
            duration = old_duration[0] + int(duration)
        query = "UPDATE membership SET duration = "+str(duration)+" WHERE mname = '" + mem_name +"';"
        cursor.execute(query)
        conn.commit()
        print(query)
    cursor.close()
    conn.close()
    return render_template('update_member.html',members=results)

@app.route("/view_members",methods=['POST','GET'])
def view_member_route():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM membership;')
    results = cursor.fetchall()
    return render_template('view_members.html',members=results)

@app.route("/")
def index_route():
    return render_template('index.html')

if __name__ == '__main__':
  app.run(debug=True,host='0.0.0.0',port=80)