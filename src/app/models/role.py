from app import db

from sqlalchemy.dialects.postgresql import UUID


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    title = db.Column(db.String(255), unique=True, nullable=False)
