from flask import g, flash, url_for, redirect, render_template, request, session
from app import app 
from restaurants import  delete_review, get_reviews_with_users, add_restaurant, get_all_restaurants, delete_restaurant, get_restaurant_by_id, update_restaurant, add_group, get_all_groups, update_restaurant_groups, get_restaurant_groups

import users, restaurants


@app.route("/")
def index():
    all_restaurants = get_all_restaurants()
    all_groups = get_all_groups() 
    admin = session.get("admin", False)
    return render_template("index.html", all_restaurants=all_restaurants, all_groups=all_groups, admin=admin)


#Kirjautumisjutut
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        admin = "admin" in request.form
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1, admin):
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
    users.logout()
    return redirect("/")





#Ravintolajutut
@app.route("/add_restaurant", methods=["GET", "POST"])
def add_restaurant_route():
    if request.method == "GET":
        all_groups = get_all_groups()
        return render_template("add_restaurant.html", all_groups=all_groups)
    elif request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        location = request.form["location"]
        groups = request.form.getlist("groups")
        if add_restaurant(name, description, location, groups):
            return redirect("/")
        else:
            return render_template("error.html", message="Ravintolan lisääminen epäonnistui")


#Ravintolan tietojen muokkaus
@app.route("/edit_restaurant/<int:restaurant_id>", methods=["GET", "POST"])
def edit_restaurant_route(restaurant_id):
    if request.method == "GET":
        restaurant = get_restaurant_by_id(restaurant_id)
        if restaurant:
            all_groups = get_all_groups()
            restaurant_groups = get_restaurant_groups(restaurant_id)
            return render_template("edit_restaurant.html", restaurant=restaurant, all_groups=all_groups, restaurant_groups=restaurant_groups)
        else:
            flash("Restaurant not found", "error")
            return redirect(url_for("index"))
    elif request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        location = request.form["location"]
        groups = request.form.getlist("groups")
        if update_restaurant(restaurant_id, name, description, location, groups):
            flash("Restaurant information updated successfully", "success")
            return redirect(url_for("index"))
        else:
            flash("Failed to update restaurant information", "error")
            return redirect(url_for("edit_restaurant_route", restaurant_id=restaurant_id))


#Ravintolan poistaminen
@app.route("/delete_restaurant/<int:restaurant_id>", methods=["POST"])
def delete_restaurant_route(restaurant_id):
    if "username" not in session or not users.admin(session["username"]):
        return redirect(url_for("login"))  

    if delete_restaurant(restaurant_id):
        flash("Restaurant deleted successfully", "success")
    else:
        flash("Failed to delete restaurant", "error")

    return redirect(url_for("index"))






#Ryhmän lisääminen
@app.before_request
def before_request():
    g.all_groups = get_all_groups()


@app.route("/add_group", methods=["GET", "POST"])
def add_group_route():
    if request.method == "POST":
        name = request.form["name"]
        created_by = session.get("user_id")  
        success = add_group(name, created_by)
        if success:
            g.all_groups = get_all_groups()
            return redirect("/")
        else:
            return render_template("error.html", message="Failed to add group")
    else:
        return render_template("add_group.html")
    

#Ravintolan tietojen muokkaus
@app.route("/update_restaurant_groups/<int:restaurant_id>", methods=["POST"])
def update_restaurant_groups_route(restaurant_id):
    if request.method == "POST":
        groups = request.form.getlist("groups")
        if update_restaurant_groups(restaurant_id, groups):
            return redirect("/")
        else:
            return render_template("error.html", message="Ravintolan ryhmien päivitys epäonnistui")




#Arvostelun lisääminen
@app.route("/reviews/<int:restaurant_id>")
def reviews(restaurant_id):
    reviews = get_reviews_with_users(restaurant_id)
    return render_template("reviews.html", restaurant_id=restaurant_id, reviews=reviews)

#Arvostelun poistaminen
@app.route("/delete_review/<int:review_id>", methods=["GET"])
def delete_review_route(review_id):
    if "username" not in session:
        flash("You must be logged in to delete a review", "error")
        return redirect(url_for("login"))

    # Tarkistetaan, että käyttäjä voi poistaa arvostelun
    review = get_reviews_with_users(review_id)
    if not review:
        flash("Review not found", "error")
        return redirect(url_for("index"))
    if session["username"] != review[0]["username"]:
        flash("You can only delete your own reviews", "error")
        return redirect(url_for("index"))

    # Poistetaan arvostelu tietokannasta
    if delete_review(review_id):
        flash("Review deleted successfully", "success")
    else:
        flash("Failed to delete review", "error")

    return redirect(url_for("reviews", restaurant_id=review[0]["restaurant_id"]))


#Arvostelujen tarkastelu
@app.route("/add_review/<int:restaurant_id>", methods=["POST"])
def add_review(restaurant_id):
    if request.method == "POST":
        if session.get("username"):
            user_id = session["user_id"]
            review_text = request.form.get("review_text")
            rating = int(request.form.get("rating"))
            if restaurants.add_review(restaurant_id, user_id, review_text, rating):
                flash("Review added successfully", "success")
            else:
                flash("Failed to add review", "error")
            return redirect(url_for("reviews", restaurant_id=restaurant_id))
        else:
            flash("You must be logged in to add a review", "error")
            return redirect(url_for("login"))

        
