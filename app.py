from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv

from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI']='postgres://postgres:1305@localhost:5432/postgres'



app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")