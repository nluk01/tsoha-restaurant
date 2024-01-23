from app import app
from flask import redirect, render_template, request, session
from db import db
import users



@app.route("/")
def index():
    if "username" in session:
        return render_template("index.html", username=session["username"])
    else:
        return render_template("index.html")



#Kirjautumis jutut


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        is_admin = "is_admin" in request.form 
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1, is_admin):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")
        


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")
        


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")




#Ravintola jutut




