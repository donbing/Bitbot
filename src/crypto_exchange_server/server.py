#!/usr/bin/env python3

from http.server import HTTPServer
from handlers import CcxtExchangesHandler

# start the webserver
server = HTTPServer(('', 8081), CcxtExchangesHandler)
server.serve_forever()
