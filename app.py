from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from dotenv import load_dotenv


app = Flask(__name__)


load_dotenv()
app.secret_key = getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1305@localhost/postgres"
db = SQLAlchemy(app)



import routes
