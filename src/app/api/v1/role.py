import logging

from flask_restful import reqparse, Resource

from app import models

logger = logging.getLogger(__name__)

role_parser = reqparse.RequestParser()
role_parser.add_argument('title', dest='title', type=str, location='json', required=True,
                         help='The role\'s title')


class Role(Resource):
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
        pass

    def patch(self):
        pass
