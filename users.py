import os
from flask import session
from db import db
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text


def register(username, password, is_admin=False):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, is_admin) VALUES (:username, :password, :is_admin)"
        db.session.execute(text(sql), {"username": username, "password": hash_value, "is_admin": is_admin})
        db.session.commit()
    except Exception as e:
        print(f"Error during registration: {e}")
        return False
    return login(username, password)




def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["username"] = username  
            session["user_id"] = user.id
            return True
        else:
            return False



def user_id():
    return session.get("user_id", 0)


def logout():
    del session["user_id"]
