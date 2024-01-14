from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    login = StringField("Логин", validators=[DataRequired()])
    psw = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class BookForm(FlaskForm):
    name = TextAreaField("Название", validators=[DataRequired(), Length(max=300, message="Слишком длинное название")])

