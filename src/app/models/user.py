from datetime import datetime
from uuid import uuid4

from app import db
from sqlalchemy.dialects.postgresql import UUID, BOOLEAN


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
        # FIXME ДОбавить проверку на существование пользователя в базе
        if cls.is_user_exist(user):
            return # FIXME Что должен возвращать если пользователь уже есть?
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def check_user(cls, user_fields: dict):
        """
        Идентификация и аутентификация пользователя

        :param user_fields:
        :return:
        """
        # FIXME здесь должна быть реализована проверка пароля, при условии что пароль мы в открытом виде не храним
        login = user_fields['login']
        password = user_fields['password']
        user = User.query.filter_by(login=login).one_or_none()
        if user:
            if user.password == password:
                return user
            return
        return

    def __repr__(self):
        return f'<User {self.login} {self.id}>'

    @classmethod
    def is_user_exist(cls, user_fields: dict):
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

