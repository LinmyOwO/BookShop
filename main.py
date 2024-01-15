import os
from flask import Flask, render_template, abort, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from admin.admin import admin
from forms import *

# конфигурация приложения
DATABASE = '/tmp/shop.db'
DEBUG = True
SECRET_KEY = '7bee6651532c3c31a57bca7b6ccbcd36894f874e'

SQLALCHEMY_DATABASE_URI = 'sqlite:///shop.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'shop.db')))

app.register_blueprint(admin, url_prefix='/admin')

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    psw = db.Column(db.String(500))
    reg_date = db.Column(db.DateTime, default=datetime.utcnow())


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    authors = db.Column(db.String(300))
    description = db.Column(db.Text, nullable=True)
    length = db.Column(db.Integer)
    price = db.Column(db.Integer)
    is_available = db.Column(db.Boolean, default=False)
    source_url = db.Column(db.String(100), nullable=True)
    image_url = db.Column(db.String(100), nullable=True)

    genres = db.relationship('BooksGenres', backref='book', lazy='dynamic')


class Genres(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    books = db.relationship('BooksGenres', backref='genre', lazy='dynamic')


class BooksGenres(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))


all_genres = []
@app.before_request
def get_header_genres():
    """Функция подгрузки всех жанров для шапки"""
    global all_genres
    try:
        all_genres = Genres.query.order_by(Genres.name).all()
    except Exception as e:
        print(e.args)


@app.route('/')
def index():
    """Главная страница"""
    return render_template("index.html", all_genres=all_genres)


@app.route('/about')
def about():
    """Страница 'О нас'"""
    return render_template("about.html", all_genres=all_genres)


@app.route('/history')
def history():
    """Страница с историей заказов"""
    return render_template("history.html", orders=[], all_genres=all_genres)


@app.route('/cart')
def cart():
    """Страница корзины"""
    return render_template("cart.html", items=[], all_genres=all_genres)


@app.route('/register', methods=["POST", "GET"])
def register():
    """Страница регистрации"""
    form = RegisterForm()

    if form.validate_on_submit():
        res = Users.query.filter(Users.email == form.email.data).all()
        if res:
            flash("Пользователь с таким email уже существует")
            return render_template("register.html", form=form, all_genres=all_genres)

        data_loaded = False
        try:
            hash = generate_password_hash(form.psw.data)
            u = Users(
                username=form.username.data,
                email=form.email.data,
                psw=hash
            )
            db.session.add(u)
            db.session.commit()

            data_loaded = True
        except Exception as e:
            print(e.args)

        if data_loaded:
            flash("Аккаунт успешно зарегестрирован")
            return redirect(url_for('login'))
        else:
            flash("Произошла ошибка сервера, попробуйте позже")

    return render_template("register.html", form=form, all_genres=all_genres)


@app.route('/login')
def login():
    """Страница входа"""
    return render_template("login.html", all_genres=all_genres)


@app.route('/profile/<int:userid>')
def profile():
    """Страница профиля"""
    return render_template("profile.html", all_genres=all_genres)


@app.route('/book/<int:book_id>')
def book(book_id):
    """Страница книги"""
    res = None
    try:
        res = BooksGenres.query.filter(BooksGenres.book_id == book_id).order_by(BooksGenres.book_id.desc()).all()
    except Exception as e:
        print(e.args)

    if not res:
        abort(404)

    book = res[0].book
    genres = [row.genre for row in res]
    return render_template("book.html", book=book, genres=genres, all_genres=all_genres)


@app.route('/catalog/<int:genre_id>')
def catalog(genre_id):
    """Страница жанра"""
    res = None
    try:
        res = BooksGenres.query.filter(BooksGenres.genre_id == genre_id).order_by(BooksGenres.book_id.desc()).all()
    except Exception as e:
        print(e.args)

    if not res:
        abort(404)
    genre = res[0].genre.name
    books = [row.book for row in res]

    return render_template("catalog.html", books=books, genre=genre, all_genres=all_genres)


# @app.errorhandler(404)
# def pageNotFound(error):
#     return render_template("page404.html")


if __name__ == "__main__":
    app.run()
