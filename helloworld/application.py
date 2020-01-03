#!flask/bin/python
import os
import functools
import base64
from flask import Flask, Response
from flask import request, session, redirect, render_template, url_for, flash
from sqlalchemy import exc
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from helloworld.models import db, User
from helloworld.flaskrun import flaskrun
from helloworld.forms import UserForm, LoginForm, RequestPasswordForm, ResetPasswordForm


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session or session['user_id'] is None:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view


application = Flask(__name__)

application.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_ECHO=True,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI='sqlite:///tsapp.sqlite',
        SENDGRID_SENDER_EMAIL='gsorry@gmail.com',
        SENDGRID_API_KEY=os.environ.get('SENDGRID_API_KEY')
)


@application.route('/', methods=['GET'])
def index():
    return Response(render_template('index.html'), mimetype='text/html', status=200)


@application.route('/auth/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_form = UserForm(request.form)
        if user_form.validate():
            user = User(email=user_form.email.data)
            try:
                error_message, password_ok = user.check_password_strength_and_hash_if_ok(user_form.password.data)
                if password_ok:
                    user.fullname = user_form.fullname.data
                    user.add(user)
                    flash("You have successfully registered to tsapp application.")
                    return redirect(url_for('login'))
                else:
                    flash(error_message)
            except exc.IntegrityError:
                flash("The email address already exist. Please, specify different email address.")
        else:
            if 'email' in user_form.errors:
                flash(user_form.errors['email'][0])
            if 'password' in user_form.errors:
                flash(user_form.errors['password'][0])
            if 'fullname' in user_form.errors:
                flash(user_form.errors['fullname'][0])

    return Response(render_template('auth/register.html'), mimetype='text/html', status=200)


@application.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_form = LoginForm(request.form)
        if login_form.validate():
            user = User.query.filter_by(email=login_form.email.data).first()
            if user is not None:
                if user.verify_password(login_form.password.data):
                    session.clear()
                    session['user_id'] = user.id
                    return redirect(url_for('profile'))
                else:
                    flash("Wrong password.")
            else:
                flash("Email address does not exist.")
        else:
            if 'email' in login_form.errors:
                flash(login_form.errors['email'][0])
            if 'password' in login_form.errors:
                flash(login_form.errors['password'][0])

        return redirect(url_for('login'))

    return Response(render_template('auth/login.html'), mimetype='text/html', status=200)


@application.route('/auth/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))


@application.route('/auth/request_password', methods=['GET', 'POST'])
def request_password():
    if request.method == 'POST':
        request_password_form = RequestPasswordForm(request.form)
        if request_password_form.validate():
            user = User.query.filter_by(email=request_password_form.email.data).first()
            if user is not None:
                token = str(base64.urlsafe_b64encode(user.email.encode("utf-8")), "utf-8")
                message = Mail(
                    from_email=application.config['SENDGRID_SENDER_EMAIL'],
                    to_emails=user.email,
                    subject='tsapp reset password link',
                    html_content='Please, click on the following link to reset your password:'
                                 '<a href="{link}">{link}</a>'.format(
                        link=url_for('reset_password', token=token, _external=True))
                )
                try:
                    sg = SendGridAPIClient(application.config['SENDGRID_API_KEY'])
                    response = sg.send(message)
                    flash(
                        "Please, check your inbox. An email has been sent to you with instructions for resetting your password.")
                    return redirect(url_for('login'))
                except Exception as e:
                    flash(str(e))
            else:
                flash("This email address does not exist in our database. Please, specify different email address.")
        else:
            if 'email' in request_password_form.errors:
                flash(request_password_form.errors['email'][0])

    return Response(render_template('auth/request_password.html'), mimetype='text/html', status=200)


@application.route('/auth/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        reset_password_form = ResetPasswordForm(request.form)
        token = reset_password_form.token.data
        if reset_password_form.validate():
            email = str(base64.b64decode(token), "utf-8")
            user = User.query.filter_by(email=email).first()
            if user is not None:
                error_message, password_ok = user.check_password_strength_and_hash_if_ok(
                    reset_password_form.password.data)
                if password_ok:
                    user.update()
                    flash("You have successfully changed the password.")
                    return redirect(url_for('login'))
                else:
                    flash(error_message)
                return redirect(url_for('reset_password', token=token))
            else:
                flash("Invalid link. Please, specify different email address.")
        else:
            if 'password' in reset_password_form.errors:
                flash(reset_password_form.errors['password'][0])
            if 'token' in reset_password_form.errors:
                flash("Invalid link. Please, specify different email address.")

    token = request.args.get('token', '', type=str)
    email = str(base64.b64decode(token), "utf-8")
    user = User.query.filter_by(email=email).first()
    if user is not None:
        return Response(render_template('auth/reset_password.html'), mimetype='text/html', status=200)
    else:
        flash("Invalid link. Please, specify different email address.")
    return redirect(url_for('request_password'))


@application.route('/users/profile', methods=['GET'])
def profile():
    user = User.query.get_or_404(session['user_id'])
    return Response(render_template('users/profile.html', user=user), mimetype='text/html', status=200)


db.init_app(application)

if __name__ == '__main__':
    flaskrun(application)
