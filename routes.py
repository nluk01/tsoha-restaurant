from app import app, db
from flask import render_template, request, redirect, session, url_for, g
from flask_login import login_required
from users import register, login
from models import Restaurant, Add_group
from flask_login import current_user



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
        user = login(username, password)
        if user:
            session["username"] = username
            session["is_admin"] = user
            return redirect("/")
        else:
            return render_template("error.html", message="Wrong username or password.")




@app.route("/logout")
def logout_route():
    session.clear()
    return redirect("/")





# Ravintola-jutut

@app.route("/admin/add_group", methods=["GET", "POST"])
@login_required
def add_group():
    if request.method == "POST":
        pass


@app.route("/admin/add_restaurant", methods=["GET", "POST"])
@login_required
def add_restaurant():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        group_ids = request.form.getlist("groups") 

        new_restaurant = Restaurant(name=name, description=description)

        for group_id in group_ids:
            group = Add_group.query.get(group_id)
            if group:
                new_restaurant.groups.append(group)

        db.session.add(new_restaurant)
        db.session.commit()

        groups = Add_group.query.all()
        return render_template("add_restaurant.html", groups=groups)




@app.route("/admin/remove_restaurant/<int:restaurant_id>")
@login_required
def remove_restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)

    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()

    return redirect(url_for("index"))
