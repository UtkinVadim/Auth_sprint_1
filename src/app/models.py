import datetime
import uuid

from sqlalchemy.dialects.postgresql import UUID, BOOLEAN

from db import db


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    created_on = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    roles = db.relationship("RolesModel", secondary="user_roles", backref=db.backref("users", lazy="dynamic"))
    is_active = db.Column(BOOLEAN, default=True)

    def __repr__(self):
        return f'<User {self.login} {self.id}>'


class UserRolesModel(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), unique=True, nullable=False, use_list=False)
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('roles.id'))


class RolesModel(db.Model):
    __tablename__ = 'roles'
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    title = db.Column(db.String(255), unique=True, nullable=False)


class LoginHistoryModel(db.Model):
    __tablename__ = 'login_history'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    fingerprint = db.Column(db.String)
    event_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow)


def create_user(user_fields):
    """
    Создаёт пользователя в базе

    :param user_fields:
    :return:
    """
    user = Users(**user_fields)
    db.session.add(user)
    db.session.commit()
    return user


def check_user(user_fields):
    # FIXME здесь должна быть реализована проверка пароля, при условии что пароль мы в открытом виде не храним
    login = user_fields['login']
    password = user_fields['password']
    user = Users.query.filter_by(login=login).one_or_none()
    if user.password == password:
        return user
    return
