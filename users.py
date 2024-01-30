from flask import session
from db import db
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text


#Kirjautumis jutut

def register(username, password, admin=False):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password, :admin)"
        db.session.execute(text(sql), {"username": username, "password": hash_value, "admin": admin})
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error during registration: {e}")
        return False



def login(username, password):
    sql = text("SELECT id, password, admin FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    users = result.fetchone()
    if not users:
        return False
    else:
        if check_password_hash(users.password, password):
            session["username"] = username  
            session["user_id"] = users.id
            session["admin"] = users.admin 
            return True
        else:
            return False

def admin(username):
    if username and session.get("admin"):
        return True
    return False



def user_id():
    return session.get("user_id", 0)


def logout():
    if "username" in session:
        del session["username"]
    if "user_id" in session:
        del session["user_id"]

