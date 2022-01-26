from inky.auto import auto
from http.server import BaseHTTPRequestHandler, HTTPServer
from PIL import Image
import io
import cgi


# 🎨 create a limited pallete image for converting our chart image
def quantise_inky(display_image):
    palette_img = Image.new("P", (1, 1))
    white_black_red = (255, 255, 255, 0, 0, 0, 255, 0, 0)
    palette_img.putpalette(white_black_red + (0, 0, 0) * 252)
    return display_image.convert('RGB').quantize(palette=palette_img)


class StoreHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        html = '''
            <form method='post' enctype='multipart/form-data'>
                <input type='file' name='image_file'/>
                <input type='submit'>
            </form>'''

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html)))
        self.end_headers()
        self.wfile.write(bytes(html, "utf8"))

    def do_POST(self):
        inky_display = auto()
        content_type, pdict = cgi.parse_header(
            self.headers['content-type'])

        # boundary data needs to be encoded in a binary format
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")

        if content_type == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)

        image = Image.open(io.BytesIO(fields['image_file'][0]), mode='r')
        image = image.resize((400, 300))
        inky_display.set_image(quantise_inky(image))
        inky_display.show()

        self.send_response(200)


# start the webserver
server = HTTPServer(('', 8081), StoreHandler)
server.serve_forever()
