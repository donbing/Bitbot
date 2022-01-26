import threading
import time
import unittest
from http.server import HTTPServer
from urllib import request
import sys
import json
sys.path.append('.')
from src.crypto_exchange_server.handlers import CcxtExchangesHandler


class TestCcxtWebServer(unittest.TestCase):

    def setUp(self):
        self.server = None
        self.port = 21344
        self.host = ''
        self.start_server()

    def start_server(self):
        self.server = HTTPServer((self.host, self.port), CcxtExchangesHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        time.sleep(0.25)

    def stop_server(self):
        if self.server is None:
            return
        self.server.shutdown()
        self.server_thread.join()

    def tearDown(self):
        self.stop_server()

    def test_fetch_price_history(self):
        req = request.Request(f"http://localhost:{self.port}/?exchange=bitmex&instrument=BTC/USD&candle_width=5m")
        req.add_header('content-type', 'application/json')
        response = request.urlopen(req)
        foo = response.read().decode(response.headers.get_content_charset(failobj="utf-8"))
        json_data = json.loads(foo)
        self.assertEqual(json_data['instrument'], "BTC/USD")
        self.assertGreater(len(json_data['candle_data']), 0)
        self.assertEqual(json_data['exchange'], 'bitmex')
