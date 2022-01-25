import threading
import time
import unittest
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('it works!')


class TestRequests(unittest.TestCase):

    def test_single_request(self):
        server = HTTPServer(("127.0.0.1", 13345), MyHandler)
        server_thread = threading.Thread(target=server.serve_forever)
        # Also tried this:
        #server_thread.setDaemon(True)
        server_thread.start()
        # Wait a bit for the server to come up
        time.sleep(1)
        print(urllib.request.urlopen("http://localhost:12345/").read())
        
        server_thread.stop()
