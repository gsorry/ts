#!flask/bin/python
import json
import functools
from flask import Flask, Response, session, redirect, render_template, url_for
from helloworld.flaskrun import flaskrun


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session or session['user_id'] is None:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view


application = Flask(__name__)


@application.route('/', methods=['GET'])
def index():
    return Response(render_template('index.html'), mimetype='text/html', status=200)


@application.route('/auth/register', methods=['GET', 'POST'])
def register():
    return Response(render_template('auth/register.html'), mimetype='text/html', status=200)

@application.route('/auth/login', methods=['GET', 'POST'])
def login():
    return Response(render_template('auth/login.html'), mimetype='text/html', status=200)

@application.route('/auth/logout', methods=['GET', 'POST'])
def logout():
    return redirect(url_for('login'))

@application.route('/auth/request_password', methods=['GET', 'POST'])
def request_password():
    return Response(render_template('auth/request_password.html'), mimetype='text/html', status=200)

@application.route('/auth/reset_rassword', methods=['GET', 'POST'])
def reset_rassword():
    return Response(render_template('auth/reset_rassword.html'), mimetype='text/html', status=200)

if __name__ == '__main__':
    flaskrun(application)
