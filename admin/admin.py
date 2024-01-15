from flask import Blueprint, render_template, url_for, redirect, session, request, flash
from forms import AdminLoginForm, BookForm


admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


def login_admin():
    session['admin_logged'] = 1


def isLogged():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)


@admin.route('/')
def index():
    if not isLogged():
        return redirect(url_for('.login'))
    return render_template('admin/index.html')


@admin.route('/newbook')
def new_book():
    if not isLogged():
        return redirect(url_for('.login'))

    form = BookForm()

    return render_template('admin/newbook.html', form=form)


@admin.route('/login', methods=["POST", "GET"])
def login():
    if isLogged():
        return redirect(url_for('.index'))

    form = AdminLoginForm()
    if form.validate_on_submit():
        if form.login.data == "admin" and form.psw.data == "12345":
            login_admin()
            return redirect(request.args.get('next') or url_for('.index'))
        else:
            flash("Неверный логин/пароль")

    return render_template('admin/login.html', form=form)


@admin.route('/logout', methods=["POST", "GET"])
def logout():
    if not isLogged():
        return redirect(url_for('.login'))

    logout_admin()

    return redirect(url_for('.login'))
