import datetime
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

from app import db


class UserRole(db.Model):
    __tablename__ = 'user_role'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user_auth.id'), unique=True, nullable=False)
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('role.id'))
    created_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
