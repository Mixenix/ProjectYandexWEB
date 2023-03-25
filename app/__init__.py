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


# migrate = Migrate(app, db)
bootstrap = Bootstrap(app)


class PostForm(FlaskForm):
    body = TextAreaField("What's on your mind?", validators=[DataRequired()])
    submit = SubmitField("Submit")

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



@app.route("/blog", methods=["GET", "POST"])
def blog():
    form = PostForm()
    if form.validate_on_submit():
        # session["post"] = form.body.data
        db_sess = db_session.create_session()
        blog = Blogs(content=form.body.data)
        db_sess.add(blog)
        db_sess.commit()
        db_sess.close()
        return redirect(url_for("blog"))
    db_sess = db_session.create_session()
    query = db_sess.query(Blogs)
    blogs = query.order_by(Blogs.created_at.desc())
    return render_template(
        "blog.html",
        items=blogs,
        form=form
    )

@app.route('/blog/<int:id>', methods=['GET', 'POST'])
def edit_blogs(id: int):
    form = BlogForm()
    db_sess = db_session.create_session()
    blogs = db_sess.query(Blogs).filter(Blogs.id == id).first()
    if request.method == "GET":
        if blogs:
            form.content.data = blogs.content
        else:
            abort(404)
    if form.validate_on_submit():
        if blogs:
            blogs.content = form.content.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('edit.html', form=form,
                           title='Редактирование поста')

@app.route('/blog/<int:id>/delete', methods=['GET', 'POST'])
def blog_delete(id: int):
    db_sess = db_session.create_session()
    blogs = db_sess.query(Blogs).filter(Blogs.id == id).first()
    if blogs:
        db_sess.delete(blogs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route("/projects")
def projects():
    design_projects = [
        "Chicago Latino Film Festival/chicago.png",
        "GORGEOUS/gorgeousposter.png",
        "Liquid Effect/liquid.png",
        "something latin/sedatmaurismetus.png",
        "Jun 29/ver2.png",
        "enSage/recvrd.png"
    ]
    python_projects = [
        "Flappy Bird/flappy.jpg",
        "World Clock/worldclock.png",
    ]
    projects_names = [
        design_projects,
        python_projects
    ]

    page = request.args.get("page")
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    return render_template(
        "projects.html",
        title="Projects",
        url=os.getenv("URL"),
        projects=projects_names,
        pag=page,
    )


@app.route("/condition", methods=["GET"])
def condition():
    return "excellent working"


@app.route("/register", methods=("GET", "POST"))
def register():
    return "Register Page not created yet", 501


@app.route("/login", methods=("GET", "POST"))
def login():
    return "Login Page not created yet", 501



