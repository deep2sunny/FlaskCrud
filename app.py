from flask import Flask,render_template,request,redirect,url_for,flash
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = 'flash message'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'tiger'
app.config['MYSQL_DB'] = 'crudapplication'

mysql = MySQL(app)


@app.route('/')
def index():

    cur = mysql.connection.cursor()
    cur.execute("select * from students")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html',students=data)

#Insert data to DB
@app.route('/insert',methods=['POST'])
def insert():


    if request.method == 'POST':
        flash('Data Inserted Successfully')
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO students (name,email,phone) values (%s,%s,%s)',(name,email,phone))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

#Update data to DB
@app.route('/update',methods=['POST','GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute("""update students 
        set name=%s, email=%s, phone=%s
        where id=%s
        
        
        """,(name,email,phone,id_data))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

#Delete data from DB
@app.route('/delete/<string:id_data>',methods=['GET'])
def delete(id_data):

    cur = mysql.connection.cursor()
    cur.execute(f'DELETE from students where id={id_data}')
    mysql.connection.commit()
    flash("Record Has Been Deleted Successfully")
    cur.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)