from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)

load_dotenv()

app.secret_key = getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')


import routes
