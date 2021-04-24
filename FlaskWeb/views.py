"""
Routes and views for the flask application.
"""
# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, request
from FlaskWeb import app
import sqlite3 as sql


data = "./FlaskWeb/data/student.db"

@app.route('/')
@app.route('/home')
def home():
    conn = sql.connect(data)
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("select * from 'stu'")
    rows = cur.fetchall()
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Student List',
        rows = rows,
        year=datetime.now().year, 
    )
    conn.close()

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year, 
        message='Your contact page.'
    )

@app.route('/add_student')
def add_student():
    """Renders the about page."""
    return render_template(
        'add_student.html',
        year=datetime.now().year,
    )

@app.route('/del_student')
def del_student():
    """Renders the about page."""
    return render_template(
        'del_student.html',
        title='Delete Student',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/addrecore', methods = ['POST','GET'])
def addrecore ():
    msg ="Nothing to do"
    if request.method == 'POST':
      try:
         nm = str.upper(request.form['Name'])  
         em = str.upper(request.form['email'])
         date = request.form['dob']
         add = str.upper(request.form['home'])
         sco = float(request.form['score'])
         conn = sql.connect(data)
         cur = conn.cursor()
         sco = round(sco,1)
         cur.execute(
             'INSERT INTO stu (Name,Email,DoB,Home,Score)'
             'VALUES (?,?,?,?,?)',
             (nm,em,date,add,sco) 
         )
         conn.commit()
         msg = "Record successfully added"
      except:
         conn.rollback()
         msg = "error in insert operation"

      finally:
         return render_template("result.html",message = msg)
         conn.close()

@app.route('/modrecore', methods = ['POST','GET'])
def modrecore ():
    msg ="Nothing to do"
    if request.method == 'POST':
      try:
         id = request.form["_ID"]
         nm = str.upper(request.form['Name'])  
         em = str.upper(request.form['email'])
         date = request.form['dob']
         add = str.upper(request.form['home'])
         sco = float(request.form['score'])
         conn = sql.connect(data)
         cur = conn.cursor()
         sco = round(sco,1)
         cur.execute(
             'Update stu set Name = ?, Email = ?, DoB = ?, Home =?, Score = ? Where ID = ?;',
             (nm,em,date,add,sco,id) 
         )
         conn.commit()
         msg = "Record successfully update"
      except:
         conn.rollback()
         msg = "error in update operation"

      finally:
         return render_template("result.html",message = msg)
         conn.close()


@app.route('/mod_stu', methods = ['POST','GET'])
def mod_stu():
    """Renders the about page."""
    msg ="Nothing to do"
    if request.method == 'POST':
        act = request.form['action']
        id = request.form['_ID']
        conn = sql.connect(data)
        conn.row_factory = sql.Row
        cur = conn.cursor()
        if act == "Delete":
            try:
                cur.execute(
                    'delete from stu where ID = ?',
                    (id) 
                )
                conn.commit()
                msg = "Record successfully deleted"
            except:
                conn.rollback()
                msg = "error in insert operation"
            finally:
                return render_template("result.html",message = msg)
                conn.close()
        else:
            cur.execute(
                'select * from stu where ID = ?',
                (id)
                )
            rows = cur.fetchall()
            return render_template("mod_student.html", rows=rows,year=datetime.now().year,)
