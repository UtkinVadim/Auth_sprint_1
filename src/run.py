from gevent import monkey

monkey.patch_all()

import sys

from app import app
from config import SERVER_HOST, SERVER_PORT
from gevent.pywsgi import WSGIServer

if __name__ == '__main__':
    if "-d" in sys.argv:
        app.run(debug=True)
    else:
        http_server = WSGIServer((SERVER_HOST, SERVER_PORT), app)
        http_server.serve_forever()
