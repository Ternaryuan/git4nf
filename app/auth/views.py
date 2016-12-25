from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from . import auth
from ..models import User
from ..email import send_email
from .forms import LoginForm, RegistrationForm
from .. import db


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        if not current_user.confirmed:
            if request.endpoint[:5] != 'auth.':
                if request.endpoint != 'static':
                    return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed/')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    # TODO: auth/unconfirmed.html
    return render_template('auth/unconfirmed.html')


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        form.password.data = ''
        flash('Invalid username or password.')
    # Done: auth/login.html
    return render_template('auth/login.html', form=form)


@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        # TODO: auth/email/confirm.txt auth/email/confirm.html
        send_email([user.email], 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    form.password.data = None
    form.password_confirm.data = None
    # TODO: auth/register.html
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>/')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/resend_confirmation/')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email([current_user.email], 'Confirm Your Account', 'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))

# TODO: modify password
# TODO: reset password
# TODO: modify email address

