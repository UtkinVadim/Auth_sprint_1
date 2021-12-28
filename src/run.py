from flask_alembic import Alembic
from gevent import monkey

monkey.patch_all()

import sys

from gevent.pywsgi import WSGIServer

from app import create_app, jwt
from config import SERVER_HOST, SERVER_PORT

app = create_app()
jwt.init_app(app)

if __name__ == "__main__":
    if "-d" in sys.argv:
        app.run(host="0.0.0.0", debug=True)
    else:
        http_server = WSGIServer((SERVER_HOST, SERVER_PORT), app)
        http_server.serve_forever()
