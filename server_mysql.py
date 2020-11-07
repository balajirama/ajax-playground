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
    flash("I just flashed", "success")
    return render_template("index.html")

@app.route("/slow_response")
def slow_response():
    for i in range(10000000):
        i+=1
    return render_template("partial.html")

usernames = [{'username': 'balaji'}, {'username': 'eliza'}]

def existing_username(namestr):
    for record in usernames:
        if record['username'] == namestr:
            return True
    return False

@app.route("/_username", methods=['POST'])
def _username():
    long_enough = len(request.form['username']) >= 5
    is_available = not existing_username(request.form['username'])
    return render_template("partials/_username.html", long_enough=long_enough, is_available=is_available)

def is_complex_password(text):
    return my_utils.AT_LEAST_ONE_NUM_REGEX.match(text) and my_utils.AT_LEAST_ONE_CAP_REGEX.match(text)

@app.route('/_password', methods=['POST'])
def _password():
    long_enough = len(request.form['password']) >= 8
    complex_enough = is_complex_password(request.form['password'])
    return render_template("partials/_password.html", long_enough=long_enough, complex_enough=complex_enough)

@app.route('/_confirm', methods=['POST'])
def _confirm():
    confirmation = request.form['password'] == request.form['confirm']
    return render_template("partials/_confirm.html", confirmation=confirmation)

@app.route('/usersearch')
def usersearch():
    searchinp = request.args.get('search')
    searchoutp = []
    for i in range(10):
        searchoutp.append({'text': 'Funny how you search for '+searchinp, 'link': '/link/'+str(i)})
    return render_template("partials/search_result.html", searchoutp=searchoutp)

if __name__ == "__main__":
    app.run(debug=True)
