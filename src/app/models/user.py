import hashlib
from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID, BOOLEAN

from app import db
from config import SALT


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    roles = db.relationship("Role", secondary="user_role", backref=db.backref("user", lazy="dynamic"))
    is_active = db.Column(BOOLEAN, default=True)

    @classmethod
    def create(cls, user_fields: dict):
        """
        Создаёт пользователя в базе

        :param user_fields:
        :return:
        """
        user = User(**user_fields)
        user.password = cls.password_hasher(user_fields['password'], SALT)
        if cls.is_user_exist(user_fields):
            return  # FIXME Что должен возвращать если пользователь уже есть?
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def check_user(cls, user_fields: dict) -> Optional[db.Model]:
        """
        Идентификация и аутентификация пользователя

        :param user_fields:
        :return:
        """
        login = user_fields['login']
        password = user_fields['password']
        user = User.query.filter_by(login=login).one_or_none()
        if user:
            if user.password == cls.password_hasher(password, SALT):
                return user
            return
        return

    def __repr__(self):
        return f'<User {self.login} {self.id}>'

    @classmethod
    def is_user_exist(cls, user_fields: dict) -> bool:
        """
        Проверка на существование пользователя

        :param user_fields:
        :return:
        """
        login = user_fields['login']
        user = User.query.filter_by(login=login).one_or_none()
        if user:
            return True
        return False

    @classmethod
    def password_hasher(cls, password: str, salt: str, hash_name: str = 'sha256', iterations: int = 100000,
                        encoding: str = 'utf-8') -> str:
        """
        Создаёт хэш от пароля который будет храниться в базе
        дока: https://docs.python.org/3.9/library/hashlib.html#hashlib.pbkdf2_hmac

        :param password:
        :param salt:
        :param hash_name:
        :param iterations:
        :param encoding:
        :return:
        """

        password_salted_hash = hashlib.pbkdf2_hmac(hash_name, password.encode(encoding), salt.encode(encoding),
                                                   iterations)
        return password_salted_hash
