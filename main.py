import os
from flask import Flask, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from DBManager import DBManager
from werkzeug.security import generate_password_hash, check_password_hash
from admin.admin import admin

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
    email = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500))
    reg_date = db.Column(db.DateTime, default=datetime.utcnow())


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    authors = db.Column(db.String(300))
    description = db.Column(db.Text, nullable=True)
    length = db.Column(db.Integer)
    price = db.Column(db.Float)
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


# def connect_db():
#     """Соединение с базой данных"""
#     conn = sqlite3.connect(app.config['DATABASE'],
#                            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
#     conn.row_factory = sqlite3.Row
#     return conn
#
#
# def create_db():
#     """Вспомагательная функция для создания базы данных"""
#     db = connect_db()
#     with app.open_resource('createDB.sql', mode='r') as f:
#         db.cursor().executescript(f.read())
#     db.commit()
#     db.close()
#
#
# def get_db():
#     """Соединение с БД, если оно еще не установлено"""
#     if not hasattr(g, 'link_db'):
#         g.link_db = connect_db()
#     return g.link_db
#
#
# dBase = None
# @app.before_request
# def before_request():
#     """Открытие соединения с БД при получении запроса"""
#     global dBase
#     db = get_db()
#     dBase = DBManager(db)
#
#
# @app.teardown_appcontext
# def close_db(error):
#     """Закрытие соединения с БД при завершении обработки запроса"""
#     if hasattr(g, 'link_db'):
#         g.link_db.close()

all_genres = []
@app.before_request
def get_header_genres():
    """Функция подгрузки всех жанров для шапки"""
    global all_genres
    try:
        all_genres = Genres.query.order_by(Genres.name).all()
    except Exception as e:
        print(e.args)


# @app.route('/book-image/<int:book_id>')

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
    if request.method == "POST":
        pass
    return render_template("register.html", all_genres=all_genres)


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
