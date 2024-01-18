from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text

from db import db
from models import User




def register(username, password, is_admin=False):
    hash_value = generate_password_hash(password)
    try:
        new_user = User(username=username, password=hash_value, is_admin=is_admin)  # Vaihda 'User' -> 'users'
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        print(f"Error during registration: {e}")
        return False
    return True



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
