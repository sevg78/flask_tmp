from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length, Regexp, Email, EqualTo

from . models import User


class RegistrationForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired('Это поле является обязательным.'), \
        Length(1, 32), \
        Email('Неверный адрес электронной почты.')])
    username = StringField('Имя пользователя', validators=[DataRequired('Это поле является обязательным.'), \
        Length(1, 16), \
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Имена пользователей должны содержать только буквы, цифры, точки или подчеркивания.')])
    password = PasswordField('Пароль', validators=[DataRequired('Это поле является обязательным.'), \
        Length(8, message='Длина поля должна быть не менее 8 символов.'), \
        EqualTo('password_confirm', 'Пароли не совпадают.')])
    password_confirm = PasswordField('Повтор пароля', validators=[DataRequired('Это поле является обязательным.')])
    submit = SubmitField('Регистрация')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Адрес электронной почты занят.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Имя пользователя занято.')


class LoginForm(FlaskForm):
    username = StringField('Пользователь', validators=[DataRequired('Это поле является обязательным.')])
    password = PasswordField('Пароль', validators=[DataRequired('Это поле является обязательным.')])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class EditProfileForm(FlaskForm):
    name = StringField('Имя', validators=[Length(0, 64)])
    location = StringField('Местоположение', validators=[Length(0, 64)])
    about_me = TextAreaField('Обо мне')
    submit = SubmitField('Применить')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Старый пароль', validators=[DataRequired('Это поле является обязательным.')])
    password = PasswordField('Новый пароль', validators=[DataRequired('Это поле является обязательным.'), \
        Length(8, message='Длина поля должна быть не менее 8 символов.'), \
        EqualTo('password2', 'Пароли не совпадают.')])
    password2 = PasswordField('Повтор нового пароля', validators=[DataRequired('Это поле является обязательным.')])
    submit = SubmitField('Обновить пароль')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired('Это поле является обязательным.'), 
        Length(1, 32),
        Email('Неверный адрес электронной почты.')])
    submit = SubmitField('Сброс пароля')


class PasswordResetForm(FlaskForm):
    password = PasswordField('Новый пароль', validators=[DataRequired('Это поле является обязательным.'), \
        Length(8, message='Длина поля должна быть не менее 8 символов.'), \
        EqualTo('password2', 'Пароли не совпадают.')])
    password2 = PasswordField('Повтор пароля', validators=[DataRequired('Это поле является обязательным.')])
    submit = SubmitField('Сброс пароля')


class ChangeEmailForm(FlaskForm):
    email = StringField('Новая почта', validators=[DataRequired('Это поле является обязательным.'), \
        Length(1, 64), \
        Email('Неверный адрес электронной почты.')])
    password = PasswordField('Пароль', validators=[DataRequired('Это поле является обязательным.')])
    submit = SubmitField('Обновить почту')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Электронная почта уже зарегистрирована.')
