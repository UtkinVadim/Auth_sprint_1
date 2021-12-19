from uuid import uuid4
from datetime import datetime

from app import db

from sqlalchemy.dialects.postgresql import UUID


class LoginHistory(db.Model):
    __tablename__ = 'login_history'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    fingerprint = db.Column(db.String)
    event_date = db.Column(db.DateTime(), default=datetime.utcnow)

    @classmethod
    def log_sign_in(cls, user, fingerprint):
        """
        Создаёт запись в базе об успешном логине пользователя

        :param user:
        :param fingerprint:
        :return:
        """
        log = LoginHistory(fingerprint=fingerprint, user_id=user.id)
        db.session.add(log)
        db.session.commit()
