from flask import (
    Blueprint,
    request,
    flash,
    redirect,
    url_for,
    current_app,
    render_template,
    render_template_string,
    jsonify,
)
import json
from datetime import datetime
from flask_login import login_required, login_user, logout_user, current_user
from app.users.forms import LoginForm, RegistrationForm, EditProfileForm, ChangePasswordForm, \
                            PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm
from app.users.models import User
from app.database import db
from app.users.mail import send_email

module = Blueprint('users', __name__)


@module.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@module.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed_at:
        return redirect(url_for('users.index'))
    return render_template('users/unconfirmed.html')


@module.route('/')
@module.route('/index')
def index():
    return render_template('users/index.html')


''''        --== OLD ==--
@module.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('users.index')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('users/OLD_login_user.html', login_form=form)
'''


@module.route('/login_modal', methods=['GET', 'POST'])
def login_modal():
    if current_user.is_authenticated:
        return redirect(url_for('users.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember.data)
            return jsonify(status='ok')
        return jsonify(status='Invalid username or password.')
    return render_template('users/_login_user.html', login_form=form)


@module.route('/log')
def log():
    if current_user.is_authenticated:
        return redirect(url_for('users.index'))
    return render_template('users/log.html')


@module.route('/reg')
def reg():
    if current_user.is_authenticated:
        return redirect(url_for('users.index'))
    return render_template('users/reg.html')


@module.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('users.index'))


@module.route('/register_modal', methods=['GET', 'POST'])
def register_modal():
    if current_user.is_authenticated:
        return redirect(url_for('users.index'))
    form =RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            send_email(user.email, 'Confirm Your Account',
                       'users/email/confirm', user=user, token=token)
            flash('A confirmation email has been sent to you by email.')
            login_user(user)
            return jsonify(status='ok')
        else:
            data = json.dumps(form.errors, ensure_ascii=False)
            return jsonify(data)
    return render_template('users/_register_user.html', register_user_form=form)


'''                 --== OLD ==--
@module.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.index'))
    form =RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'users/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('users.log'))
    return render_template('users/OLD_register_user.html', register_user_form=form)
'''


@module.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed_at is not None:
        return redirect(url_for('users.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('users.index'))


@module.route('/confirm')
@login_required
def resend_confirmation():
    if current_user.confirmed_at:
        return redirect(url_for('users.index'))
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
                                    'users/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('users.index'))


@module.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if current_user.confirmed_at is None:
        return redirect(url_for('users.unconfirmed'))
    return render_template('users/user.html', user=user)


@module.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('users.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('users/edit_profile.html', edit_profile_form=form)


@module.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('users.user', username=current_user.username))
        else:
            flash('Invalid password.')
    return render_template('users/change_password.html', change_password_form=form)


@module.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'users/email/reset_password',
                       user=user, token=token)
        flash('An email with instructions to reset your password has been '
              'sent to you.')
        return redirect(url_for('users.index'))
    return render_template('users/reset_password_request.html', password_reset_request_form=form)


@module.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('users.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('users.log'))
        else:
            return redirect(url_for('users.index'))
    return render_template('users/reset_password.html', password_reset_form=form)


@module.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data.lower()
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address',
                       'users/email/change_email', user=current_user, token=token)
            flash('An email with instructions to confirm your new email '
                  'address has been sent to you.')
            return redirect(url_for('users.index'))
        else:
            flash('Invalid email or password.')
    return render_template("users/change_email.html", change_email_form=form)


@module.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
    return redirect(url_for('users.index'))


@module.route('/test/test/test')
@login_required
def test():
    return render_template_string('ku, nah {}'.format(current_user.username))
