import sqlite3
import os
from flask import Flask, render_template

# конфигурация приложения
DATABASE = '/tmp/shop.db'
DEBUG = True
SECRET_KEY = 'o;zjoj2ksllk!?dxl14?/.,xz,sa.lflGrlw'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'shop.db')))

def connect_db():
    """Соединение с базой данных"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    """Вспомагательная функция для создания базы данных"""
    db = connect_db()
    with app.open_resource('createDB.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

@app.route('/')
def index():
    """Главная страница"""
    return render_template("index.html")

@app.route('/about')
def about():
    """Страница 'О нас'"""
    return render_template("about.html")

@app.route('/history')
def history():
    """Страница с историей заказов"""
    return render_template("history.html", orders=[])

@app.route('/cart')
def cart():
    """Страница корзины"""
    return render_template("cart.html", items=[])

@app.route('/register')
def register():
    """Страница регистрации"""
    return render_template("register.html")

@app.route('/login')
def login():
    """Страница входа"""
    return render_template("login.html")

@app.route('/profile/<int:userid>')
def profile():
    """Страница профиля"""
    return render_template("profile.html", info={})

@app.route('/book/<int:id>')
def book():
    """Страница книги"""
    return render_template("book.html", bookInfo={})

@app.route('/catalog/<category>')
def catalog():
    """Страница каталога (пока что категории)"""
    return render_template("catalog.html")


if __name__ == "__main__":
    app.run()
