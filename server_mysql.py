from flask import Flask, render_template, request, redirect, session, flash, get_flashed_messages
from flask_bcrypt import Bcrypt
from mysqlconnection import connectToMySQL
from datetime import datetime
import re
import os
import my_utils
app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = 'darksecret'

dbname = 'dbname'
# The following queries can be re-used or edited before use
# CRUD - Create, Read, Update, Delete
CREATE_RECORD = 'INSERT INTO table ( col1, col2, created_at, updated_at ) VALUES ( %(col1)s, %(col2)s, NOW(), NOW() )'
READ_ALL      = 'SELECT * from table'
READ_ONE      = 'SELECT * from table WHERE id=%(id)s'
UPDATE_RECORD = 'UPDATE table SET col1=%(col1)s, col2=%(col2)s, updated_at=NOW() WHERE id=%(id)s'
DELETE_RECORD = 'DELETE FROM table WHERE id=%(id)s'

@app.route("/")
def mainpage():
    print(get_flashed_messages())
    session.clear()
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
