# users.py
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from sqlalchemy import text

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
        session["user_id"] = get_user_id_by_username(username)
    except:
        return False
    return True

def get_user_id_by_username(username):
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user_id = result.scalar()
    return user_id


def login(username_input, password_input):
    sql = text("SELECT id, password, is_admin FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username_input})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password_input):
            session["user_id"] = user.id
            return True
        else:
            return False
        


def user_id():
    return session.get("user_id", 0)

def logout():
    del session["user_id"]
