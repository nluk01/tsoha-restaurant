from app import app, db
from flask import render_template, request, redirect, session, url_for
from flask_login import login_required
from users import register, login, login_required


from models import Restaurant


@app.route("/")
def index():
    return render_template("index.html")




@app.route("/register", methods=["GET", "POST"])
def register_route():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        is_admin = request.form.get("is_admin") == "on"

        if password != password2:
            return render_template("error.html", message="Passwords didn't match, try again.")
        if register(username, password, is_admin):
            return redirect(url_for("login_route"))
        else:
            return render_template("error.html", message="Registeration failed.")




@app.route("/login", methods=["GET", "POST"])
def login_route():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if login(username, password):
            session["username"] = username
            return redirect("/")
        else:
            return render_template("error.html", message="Wrong username or password.")

@app.route("/logout")
def logout_route():
    session.clear()
    return redirect("/")




# Ravintola-jutut

@app.route("/add_restaurant", methods=["GET", "POST"])
@login_required
def add_restaurant():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]

        new_restaurant = Restaurant(name=name, description=description)
        db.session.add(new_restaurant)
        db.session.commit()

    return redirect(url_for("index"))



@app.route("/remove_restaurant/<int:restaurant_id>")
@login_required
def remove_restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)

    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()

    return redirect(url_for("index"))