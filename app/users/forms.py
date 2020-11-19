from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length, Regexp, Email, EqualTo
from flask_babelex import _

from app.users.models import User


class RegistrationForm(FlaskForm):
    email = StringField(_('Email'), validators=[DataRequired(), Length(1, 32), Email()])
    username = StringField(_('Username'), validators=[DataRequired(), Length(1, 32),
                                                    Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                    _('Usernames must have only letters, numbers, dots or underscores'))])
    password = PasswordField('Password', validators=[DataRequired(), Length(8),
                                                     EqualTo('password_confirm',
                                                     message=_('Passwords must match.'))])
    password_confirm = PasswordField(_('Confirm password'), validators=[DataRequired()])
    submit = SubmitField(_('Register'))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(_('Email already registered.'))

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(_('Username already in use.'))


class LoginForm(FlaskForm):
    username = StringField(_('Username'), validators=[DataRequired()])
    password = PasswordField(_('Password'), validators=[DataRequired()])
    remember = BooleanField(_('Remember Me'))
    submit = SubmitField(_('Log in'))


class EditProfileForm(FlaskForm):
    name = StringField(_('Real name'), validators=[Length(0, 64)])
    location = StringField(_('Location'), validators=[Length(0, 64)])
    about_me = TextAreaField(_('About me'))
    submit = SubmitField(_('Submit'))


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(_('Old password'), validators=[DataRequired()])
    password = PasswordField(_('New password'), validators=[
        DataRequired(), Length(8), EqualTo('password2', message=_('Passwords must match.'))])
    password2 = PasswordField(_('Confirm new password'), validators=[DataRequired()])
    submit = SubmitField(_('Update Password'))


class PasswordResetRequestForm(FlaskForm):
    email = StringField(_('Email'), validators=[DataRequired(), Length(1, 32),
                                             Email()])
    submit = SubmitField(_('Reset Password'))


class PasswordResetForm(FlaskForm):
    password = PasswordField(_('New Password'), validators=[
        DataRequired(), Length(8), EqualTo('password2', message=_('Passwords must match'))])
    password2 = PasswordField(_('Confirm password'), validators=[DataRequired()])
    submit = SubmitField(_('Reset Password'))


class ChangeEmailForm(FlaskForm):
    email = StringField(_('New Email'), validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField(_('Password'), validators=[DataRequired()])
    submit = SubmitField(_('Update Email Address'))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError(_('Email already registered.'))
