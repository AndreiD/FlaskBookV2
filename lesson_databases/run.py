#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado
from tornado import autoreload
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.log import enable_pretty_logging
from tornado.wsgi import WSGIContainer

from application import app

enable_pretty_logging()

PORT = 1337

# ------- PRODUCTION CONFIG -------
# http_server = HTTPServer(WSGIContainer(app))
# http_server.bind(PORT)
# http_server.start(0)
# ioloop = tornado.ioloop.IOLoop().instance()
# autoreload.start(ioloop)
# ioloop.start()


# ------- DEVELOPMENT CONFIG -------

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(PORT)
ioloop = tornado.ioloop.IOLoop().instance()
autoreload.start(ioloop)
ioloop.start()