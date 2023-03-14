import os
from .models import db_session
from .models.Blogs import Blogs
from flask import (
    Flask,
    render_template,
    send_from_directory,
    redirect,
    url_for,
    session,
    request,
    abort
)
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
import smtplib
from werkzeug.security import generate_password_hash, check_password_hash


basedir = os.path.abspath(os.path.dirname(__file__))

db_session.global_init('./app/db/datab.db')
app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
bootstrap = Bootstrap(app)


class BlogForm(FlaskForm):
    content = TextAreaField("Содержание")
    submit = SubmitField('Применить')


@app.route("/")
def index():
    return render_template(
        "index.html", title="Amir Safin", url=os.getenv("URL")
    )


@app.route("/contact")
def contact():
    return render_template("contacts.html", title="Contact", url=os.getenv("URL"))


@app.route("/condition", methods=["GET"])
def condition():
    return "excellent working"
