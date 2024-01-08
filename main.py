from flask import Flask, render_template


app = Flask(_name__)

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
