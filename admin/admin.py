from flask import Blueprint, render_template, request, url_for, redirect, flash, session, g
from forms import LoginForm


admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


def login_admin():
    session['admin_logged'] = 1


def isLogged():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)


db = None
@admin.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global db
    db = g.get('link_db')


@admin.teardown_request
def teardown_request(request):
    global db
    db = None
    return request


@admin.route('/')
def index():
    return render_template('admin/index.html')


# @admin.route('/books')
# def books():
#     if not isLogged():
#         return redirect(url_for('.login'))
#
#     return render_template('admin/books.html')


@admin.route('/login', methods=["POST", "GET"])
def login():
    if isLogged():
        return redirect(url_for('.index'))

    form = LoginForm()
    return render_template('admin/login.html', form=form)

    # if request.method == "POST":
    #     if request.form['user'] == "admin" and request.form['psw'] == "12345":
    #         login_admin()
    #         return redirect(url_for('.index'))
    #     else:
    #         flash("Неверный логин/пароль", "error")

    # return render_template('admin/login.html')


@admin.route('/logout', methods=["POST", "GET"])
def logout():
    if not isLogged():
        return redirect(url_for('.login'))

    logout_admin()

    return redirect(url_for('.login'))
