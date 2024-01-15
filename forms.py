from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, RadioField, SubmitField, IntegerField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Regexp


class RegisterForm(FlaskForm):
    username = StringField(
        "Имя",
        validators=[DataRequired(), Length(min=2, max=100, message="Длина должна быть в пределах от 2 до 100 символов")]
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(message="Email введен некорректно"),
                    Length(min=4, max=100, message="Длина должна быть в пределах от 4 до 100 символов")]
    )
    psw = PasswordField(
        "Пароль",
        validators=[DataRequired(), Length(min=2, max=100, message="Длина должна быть в пределах от 2 до 100 символов")]
    )
    psw_check = PasswordField(
        "Повторите пароль",
        validators=[DataRequired(), EqualTo('psw', message="Пароли не совпадают")]
    )
    submit = SubmitField("Зарегестрироваться")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(message="Email некорректен")])
    psw = PasswordField("Пароль", validators=[DataRequired()])
    remember = BooleanField("Запомнить меня", default=False)
    submit = SubmitField("Войти")


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
