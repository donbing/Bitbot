import threading
import time
import unittest
from http.server import HTTPServer
from urllib import request
import json
from handlers import CcxtExchangesHandler


class TestCcxtWebServer(unittest.TestCase):

    def setUp(self):
        self.server = None
        self.port = 21341
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
        query_string = 'exchange=bitmex&instrument=BTC/USD&candle_width=5m'
        req = request.Request(f"http://localhost:{self.port}/?{query_string}")
        req.add_header('accept', 'application/json')
        response = request.urlopen(req)
        charset = response.headers.get_content_charset(failobj="utf-8")
        foo = response.read().decode(charset)
        json_data = json.loads(foo)
        self.assertEqual(json_data['instrument'], "BTC/USD")
        self.assertGreater(len(json_data['candle_data']), 0)
        self.assertEqual(json_data['exchange'], 'bitmex')


if(__name__ == '__main__'):
    unittest.main()
