import logging

from flask_restful import reqparse, Resource

from app import models

logger = logging.getLogger(__name__)

role_parser = reqparse.RequestParser()
role_parser.add_argument('title', dest='title', type=str, location='json', required=True,
                         help='The role\'s title')

role_editor_parser = reqparse.RequestParser()
role_editor_parser.add_argument('title', dest='title', type=str, location='json', required=True,
                                help='The role\'s current title')
role_editor_parser.add_argument('new_title', dest='new_title', type=str, location='json', required=True,
                                help='The role\'s new title')


class Role(Resource):
    # FIXME возвращаемые значения возможно стоит вынести в отдельный пакет
    def post(self):
        args = role_parser.parse_args()
        if models.Role.is_role_exist(args):
            return {'message': 'role already exists'}, 409
        models.Role.create(args)
        return {'message': 'role created'}, 201

    def get(self):
        roles = models.Role.get_all()
        return {'roles': roles}, 200

    def delete(self):
        args = role_parser.parse_args()
        title = args['title']
        role = models.Role.query.filter_by(title=title).one_or_none()
        if not role:
            return {'message': 'role does not exist'}, 409
        models.Role.delete(role)
        return {'message': 'role deleted'}, 200

    def patch(self):
        args = role_editor_parser.parse_args()
        role = models.Role.is_role_exist(args)
        if not role:
            return {'message': 'role does not exist'}, 409
        models.Role.update(args)
        return {'message': 'role updated'}, 200
