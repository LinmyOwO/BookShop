import os
from flask import Flask, render_template, abort, flash, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from admin.admin import admin
from forms import *
from UserLogin import UserLogin

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

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для того, чтобы продолжить"


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    psw = db.Column(db.String(500))
    reg_date = db.Column(db.DateTime, default=datetime.utcnow())

    order = db.relationship('Orders', backref='user', lazy='dynamic')


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
    orders = db.relationship('OrdersBooks', backref='book', lazy='dynamic')


class Genres(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    books = db.relationship('BooksGenres', backref='genre', lazy='dynamic')


class BooksGenres(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    order_date = db.Column(db.DateTime, default=datetime.utcnow())

    books = db.relationship('OrdersBooks', backref='order', lazy='dynamic')


class OrdersBooks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))


def get_bought_books():
    books = []
    try:
        orders = Orders.query.filter(Orders.user_id == current_user.get_id()).all()
        for order in orders:
            res = OrdersBooks.query.filter(OrdersBooks.order_id == order.id).all()
            books.extend([row.book for row in res])
    except Exception as e:
        print(e.args)

    return books


def is_book_in_cart(book_id):
    if 'cart' in session:
        return book_id in session['cart']
    session['cart'] = []
    return False


def is_book_bought(book_id):
    books = get_bought_books()
    for book in books:
        if book.id == book_id:
            return True
    return False


all_genres = []
@app.before_request
def get_header_genres():
    """Функция подгрузки всех жанров для шапки"""
    global all_genres
    try:
        all_genres = Genres.query.order_by(Genres.name).all()
    except Exception as e:
        print(e.args)


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, Users)


@app.route('/')
def index():
    """Главная страница"""
    new_books = Books.query.order_by(Books.id.desc()).limit(4).all()
    return render_template("index.html", new_books=new_books, all_genres=all_genres)


@app.route('/about')
def about():
    """Страница 'О нас'"""
    return render_template("about.html", all_genres=all_genres)


@app.route('/stocks')
def stocks():
    """Страница 'Акции'"""
    return render_template("stocks.html", all_genres=all_genres)


@app.route('/cart')
@login_required
def cart():
    """Страница корзины"""
    books = []
    price = 0
    if 'cart' in session:
        try:
            for b_id in session['cart']:
                book = Books.query.get(b_id)
                books.append(book)
        except Exception as e:
            print(e.args)
        for book in books:
            price += book.price

    return render_template("cart.html", books=books, price=price, all_genres=all_genres)


@app.route('/add-to-cart/<int:book_id>', methods=["post"])
@login_required
def add_to_cart(book_id):
    try:
        book = Books.query.get(book_id)
        if not is_book_in_cart(book.id):
            session['cart'].append(book_id)
            session.modified = True

    except Exception as e:
        print(e.args)

    return redirect(url_for('book', book_id=book_id))


@app.route('/delete-from-cart/<int:book_id>', methods=["post"])
@login_required
def delete_from_cart(book_id):
    try:
        book = Books.query.get(book_id)
        if is_book_in_cart(book.id):
            session['cart'].remove(book_id)
            session.modified = True
    except Exception as e:
        print(e.args)

    return redirect(url_for('book', book_id=book_id))


@app.route('/buy-books', methods=["post"])
@login_required
def buy_books():
    try:
        pass
    except Exception as e:
        print(e.args)

    return redirect(url_for('profile'))


@app.route('/register', methods=["POST", "GET"])
def register():
    """Страница регистрации"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()

    if form.validate_on_submit():
        res = Users.query.filter(Users.email == form.email.data).all()
        if res:
            flash("Пользователь с таким email уже существует", "text-danger")
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
            flash("Аккаунт успешно зарегестрирован", "text-success")
            return redirect(url_for('login'))
        else:
            flash("Произошла ошибка сервера, попробуйте позже", "text-danger")

    return render_template("register.html", form=form, all_genres=all_genres)


@app.route('/login', methods=["post", "get"])
def login():
    """Страница входа"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        res = Users.query.filter(Users.email == form.email.data).all()
        if res and check_password_hash(res[0].psw, form.psw.data):
            userLogin = UserLogin().create(res[0])
            rm = form.remember.data
            login_user(userLogin, rm)
            return redirect(request.args.get('next') or url_for('index'))

        flash("Неверный логин/пароль", "text-danger")

    return render_template("login.html", form=form, all_genres=all_genres)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы успешно вышли из аккаунта", "text-success")
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    """Страница профиля"""
    books = get_bought_books()
    return render_template("profile.html", books=books, all_genres=all_genres)


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

    status = "addable"
    if is_book_in_cart(book.id):
        status = "in-cart"
    if is_book_bought(book.id):
        status = "bought"

    return render_template("book.html", status=status, book=book, genres=genres, all_genres=all_genres)


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
