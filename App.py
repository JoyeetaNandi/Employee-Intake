from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import pymysql
import mysql.connector
#from App import data


# establishing the connection
conn = mysql.connector.connect(user = "root", password = "rootPassword", host = 'localhost')
## connect to the database
#connection = pymysql.connect(host = 'localhost', user = 'root', password = 'rootPassword', database = 'Client_Management_System')
cursor = conn.cursor()
# create the database
#cursor.execute("CREATE DATABASE IF NOT EXISTS crud")
connection = pymysql.connect(host = 'localhost', user = 'root', password = 'rootPassword', database = 'CMS')



app = Flask(__name__)
app.secret_key = "Secret Key"

#SqlAlchemy Database Configuration With Mysql
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:rootPassword@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize the db
db = SQLAlchemy(app)


class EmployeeList(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
 
 
    def __init__(self, name, email, phone):
 
        self.name = name
        self.email = email
        self.phone = phone

db.create_all()
#Creating model table for our CRUD database
#class Data(db.Model):
   # id = db.Column(db.Integer, primary_key = True)
   # name = db.Column(db.String(100))
   # email = db.Column(db.String(100))
   # phone = db.Column(db.String(100))
 
 
    #def __init__(self, name, email, phone):
 
        #self.name = name
       # self.email = email
      #  self.phone = phone

#db.create_all()

@app.route('/')
def Index():
    showData = EmployeeList.query.all()
    return render_template("index.html", allEmployees = showData)

#this route is for inserting data to mysql database via html forms
@app.route('/add', methods = ['POST'])
def insert():
 
    if request.method == 'POST':
 
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
 
 
        employeeListData = EmployeeList(name, email, phone)
        db.session.add(employeeListData)
        db.session.commit()
 
        flash("Employee Inserted Successfully")
 
        return redirect(url_for('Index'))


#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
def update():
 
    if request.method == 'POST':
        updateEmployeeData = EmployeeList.query.get(request.form.get('id'))
 
        updateEmployeeData.name = request.form['name']
        updateEmployeeData.email = request.form['email']
        updateEmployeeData.phone = request.form['phone']
 
        db.session.commit()
        flash("Employee Updated Successfully")
 
        return redirect(url_for('Index'))
 
 
 
 
#This route is for deleting our employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    deleteEmployeeData = EmployeeList.query.get(id)
    db.session.delete(deleteEmployeeData)
    db.session.commit()
    flash("Employee Deleted Successfully")
 
    return redirect(url_for('Index'))

if __name__== "__main__":
    app.debug = True
    #app.run(host='192.168.0.173', port=11420)
    app.run()