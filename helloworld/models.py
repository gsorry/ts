import re
import os
import click
from flask import current_app
from flask.cli import with_appcontext
from sqlalchemy import create_engine
from marshmallow import fields
from marshmallow import validate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from passlib.apps import custom_app_context as password_context

db = SQLAlchemy()
ma = Marshmallow()


class ModelAddUpdateDelete():
    def add(self, model):
        db.session.add(model)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, model):
        db.session.delete(model)
        return db.session.commit()


class User(db.Model, ModelAddUpdateDelete):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    fullname = db.Column(db.String(255))

    def __init__(self, email):
        self.email = email

    def verify_password(self, password):
        return password_context.verify(password, self.password)

    def check_password_strength_and_hash_if_ok(self, password):
        if len(password) < 8:
            return 'The password is too short. Please, specify a password with at least 8 characters.', False
        if len(password) > 32:
            return 'The password is too long. Please, specify a password with no more than 32 characters.', False
        if re.search(r'[A-Z]', password) is None:
            return 'The password must include at least one uppercase letter.', False
        if re.search(r'[a-z]', password) is None:
            return 'The password must include at least one lowercase letter.', False
        if re.search(r'\d', password) is None:
            return 'The password must include at least one number.', False
        self.password = password_context.hash(password)
        return '', True


class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    email = fields.String(required=True, validate=validate.Email)
    fullname = fields.String(required=True, validate=validate.Length(3))

    class Meta:
        fields = ('id', 'email', 'fullname')


@click.command('init-db')
@with_appcontext
def init_db_command():
    with open(os.path.join(os.path.dirname(__file__), 'schema.sql'), 'rb') as f:
        _schema_sql = f.read().decode('utf8')
    with current_app.app_context():
        engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
        raw_connection = engine.raw_connection()
        raw_connection.executescript(_schema_sql)
    click.echo('Initialized the database.')
