from os import name
from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask import session
from flask import flash
import mysql.connector


app= Flask(
    __name__,
    static_folder = "public",
    static_url_path = "/",
    )
app.secret_key='aw1/23s/4ax/34j'


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup", methods=["post"])
def signup():
    userdb = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'Skfmarch0306',
        database = 'website'
    )
    cursor = userdb.cursor()

    name = request.form['name']
    username = request.form['username']
    password = request.form['password']

    userdetails = ({
        'name' : name,
        'username' : username,
        'password' : password
    })
    
    add_user = (
        "insert into user" 
        "(name, username, password)"
        "values(%s, %s, %s)"
    )
    
    check_user = (
        "select * from user where username ={}".format(username)
    )

    cursor.execute(check_user)
    result = cursor.fetchone()

    if result != None:
        return redirect("/wrong")
    else:
        cursor.execute(add_user, (userdetails["name"], userdetails["username"], userdetails['password']))
        userdb.commit()
        cursor.close()
        userdb.close()
        return redirect('/')

@app.route("/signin", methods=["post"])
def signin():
    userdb = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'Skfmarch0306',
        database = 'website'
    )
    cursor = userdb.cursor()
    

    username = request.form['username']
    password = request.form['password']

    input = (
        username,password
    )
    
    check_login = (
        "select * from user where username ={} and password ={}".format(username,password)
    )
    cursor.execute(check_login )
    result = cursor.fetchone()

    if result is not None:
        user = request.form["username"]
        session['user'] = user
        return render_template("member.html", name = result[1])  
    else:
        return redirect(url_for("error", message="???????????????????????????"))
        

@app.route("/signout")
def signout():
    session.pop('user',None)
    return redirect(url_for('index'))

@app.route("/member")
def member():
    if "user" in session:
        user = session["user"]
        return render_template("member.html")
    else:
        return render_template("/index.html")

@app.route("/error")
def error():
    message = request.args.get("message","???????????????????????????")
    return render_template("error.html",message=message)

@app.route("/wrong")
def wrong ():
    return "?????????????????????"
app.run(port = 3000, debug = "true")