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
    #import models  # испорт нужен для создания таблиц
    db.create_all()  # по идее одноразовая операция чтобы создать таблицы

    # подключение ресурсов, можно перенести в api/v1/users
    api_app.add_resource(api.v1.user.UserInfo, url_generator(postfix='user_info'))
    api_app.add_resource(api.v1.user.UserRegistration, url_generator(postfix='user'))
    api_app.add_resource(api.v1.user.UserSignUp, url_generator(postfix='user/sign_up'))
    app.run()


if __name__ == '__main__':
    main()

# curl  http://127.0.0.1:5000/api/v1/user/sign_up -XPOST -d '{"login": "test", "email": "test@test", "password": "password"}' -H 'Content-Type: application/json'