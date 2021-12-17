import datetime
import uuid

from sqlalchemy.dialects.postgresql import UUID, BOOLEAN

from db import db


class UsersPrivateInfoModel(db.Model):
    __tablename__ = 'users_private_info'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    created_on = db.Column(db.DateTime(), default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<User {self.login}>'


class UsersModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_info = db.relationship('UsersPrivateInfoModel', backref='private_info', uselist=False)
    is_active = db.Column(BOOLEAN)
    # role_id = db.relationship('Roles', backref='users')
