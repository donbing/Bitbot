from inky.auto import auto
from http.server import BaseHTTPRequestHandler, HTTPServer
from PIL import Image


class StoreHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        html = "<form method='post'><input type='file'/><input type='submit'></form>"
        # html response
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html)))
        self.end_headers()
        self.wfile.write(bytes(html, "utf8"))

    def do_POST(self):
        inky_display = auto()
        length = self.headers['content-length']
        data = self.rfile.read(int(length))
        image = Image.open(data)
        inky_display.set_image(image)
        inky_display.show()

        self.send_response(200)


# start the webserver
server = HTTPServer(('', 8081), StoreHandler)
server.serve_forever()
