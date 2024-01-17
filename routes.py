from app import app
from flask import render_template, session, request, redirect

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    session["username"] = username
    return render_template('login.html')

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

# Lisätty reititys register.html-sivulle
@app.route("/register")
def register():
    return render_template("register.html")


