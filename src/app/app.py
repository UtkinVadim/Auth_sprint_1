from flask import Flask
from flask_restful import Api

import api.v1.user
from db import init_db, db

app = Flask(__name__)
api_app = Api(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


# перенести в utils
def url_generator(postfix: str, prefix: str = '/api', version: str = 'v1', separator: str = '/', ):
    return separator.join([prefix, version, postfix])


def main():
    init_db(app)
    app.app_context().push()
    db.create_all()  # по идее одноразовая операция чтобы создать базу и таблицы

    # подключение ресурсов, можно перенести в api/v1/users
    api_app.add_resource(api.v1.user.UserInfo, url_generator(postfix='user_info'))
    api_app.add_resource(api.v1.user.UserRegistration, url_generator(postfix='user'))
    app.run()


if __name__ == '__main__':
    main()
