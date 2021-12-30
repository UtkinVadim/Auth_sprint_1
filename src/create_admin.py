import logging

from app import db
from app.models import Role, User, UserRole
from config import SUPERUSER_EMAIL, SUPERUSER_NAME, SUPERUSER_PASSWORD

logger = logging.getLogger(__name__)


def create_admin(app):
    with app.app_context():
        admin_role: Role = Role.query.filter_by(title="admin").first()
        if not admin_role:
            admin_role: Role = Role.create(title="admin")
        user_data = {"login": SUPERUSER_NAME, "email": SUPERUSER_EMAIL, "password": SUPERUSER_PASSWORD}
        user_is_exists = User.is_login_exist(user_data)
        if user_is_exists:
            logger.info("Не удалось создать администратора, выберите другое имя.")
            return
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        UserRole.add(user.id, admin_role.id)
        logger.info("Админ создан")
