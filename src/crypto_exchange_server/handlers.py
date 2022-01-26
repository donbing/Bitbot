from http.server import BaseHTTPRequestHandler
import json
import urllib.parse as urlparse
from src.crypto_exchanges import Exchange

exchanges = Exchange()


def get_json(handler, query):
    handler.send_response(200)
    handler.send_header('Content-Type', 'application/json')
    handler.end_headers()
    try:
        price_history = exchanges.fetch_history(
            exchange_name=query["exchange"][0],
            instrument=query["instrument"][0],
            candle_width=query["candle_width"][0]
        )
        json_str = json.dumps(price_history.__dict__)
    except Exception as e:
        json_str = str(e)

    handler.wfile.write(json_str.encode(encoding='utf-8'))


def get_html(handler, query):
    html = '''
        <form method='post' enctype='multipart/form-data'>
            <input type='file' name='image_file'/>
            <input type='submit'>
        </form>'''

    handler.send_response(200)
    handler.send_header("Content-type", "text/html; charset=utf-8")
    handler.send_header("Content-Length", str(len(html)))
    handler.end_headers()
    handler.wfile.write(bytes(html, "utf8"))


def unsupported_media_type(handler):
    handler.send_response(415)
    handler.end_headers()


class CcxtExchangesHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        content_type = self.headers['content-type']
        url_query = urlparse.urlparse(self.path)
        queries = urlparse.parse_qs(url_query.query)

        if(content_type == 'application/json'):
            get_json(self, queries)
        elif(content_type == 'text/html'):
            get_html(self, queries)
        else:
            unsupported_media_type(self)
