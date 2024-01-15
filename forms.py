from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, RadioField, SubmitField, IntegerField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Regexp


class AdminLoginForm(FlaskForm):
    login = StringField("Логин", validators=[DataRequired()])
    psw = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class BookForm(FlaskForm):
    name = StringField(
        "Название",
        validators=[DataRequired(), Length(max=300, message="Название должно содержать меньше 300 символов")])
    authors = StringField(
        "Автор(-ы)",
        validators=[DataRequired(), Length(max=300, message="Автор должен содержать меньше 300 символов")])
    description = TextAreaField(
        "Описание",
        validators=[DataRequired(), Length(max=1500, message="Описание превышает 1500 символов")])
    length = IntegerField(
        "Количество страниц",
        validators=[DataRequired(), NumberRange(min=1, max=10000, message="Значение должно быть целым от 1 до 10000")])
    price = IntegerField(
        "Цена",
        validators=[DataRequired(), NumberRange(min=0, max=999999, message="Цена должна быть положительным и целым числом")]
    )
    is_available = BooleanField("Продается")
    source = FileField(
        "Источник",
        validators=[Regexp('^[^\/]{1,50}\.(pdf|txt|mobi|fb3)$', message="Неверный формат файла")])
    image = FileField(
        "Превью",
        validators=[Regexp('^[^\/]{1,50}\.(jpg|png)$', message="Неверный формат файла")]
    )
    submit = SubmitField("Добавить")
