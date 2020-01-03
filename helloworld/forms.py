from wtforms import Form
from wtforms import StringField
from wtforms import PasswordField
from wtforms import validators


class UserForm(Form):
    email = StringField('email', [validators.Length(max=255), validators.Email()])
    password = PasswordField('password', [validators.Length(min=8, max=32)])
    fullname = StringField('fullname', [validators.Length(min=3, max=255)])


class LoginForm(Form):
    email = StringField('email', [validators.Length(max=255), validators.Email()])
    password = PasswordField('password')


class RequestPasswordForm(Form):
    email = StringField('email', [validators.Length(max=255), validators.Email()])

class ResetPasswordForm(Form):
    password = PasswordField('password', [validators.Length(min=8, max=32)])
    token = StringField('token', [validators.Length(min=2)])
