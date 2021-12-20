from sqlalchemy.dialects.postgresql import UUID

from uuid import uuid4
from app import db


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    title = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f'id: {self.id}, title: {self.title}'

    @classmethod
    def get_all(cls):
        roles = cls.query.all()
        roles_dict = [{'id': str(role.id), 'title': str(role.title)} for role in roles]
        return roles_dict

    @classmethod
    def is_role_exist(cls, role_fields: dict):
        """
        Проверка на существование роли

        :param role_fields:
        :return:
        """
        title = role_fields['title']
        role = Role.query.filter_by(title=title).one_or_none()
        if role:
            return True
        return False

    @classmethod
    def create(cls, role_fields):
        role = Role(**role_fields)
        db.session.add(role)
        db.session.commit()
        return role
