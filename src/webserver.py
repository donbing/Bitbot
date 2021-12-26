from os import curdir
from os.path import join as pjoin
import cgi
from http.server import BaseHTTPRequestHandler, HTTPServer

class StoreHandler(BaseHTTPRequestHandler):
    store_path = pjoin(curdir, '../', 'config.ini')
    
    def do_GET(self):
        with open(self.store_path) as fh:
            # html for config editor
            html = '''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta content="text/html;charset=utf-8" http-equiv="Content-Type">
                    <meta content="utf-8" http-equiv="encoding">
                </head>
                <body>
                    <h1>BitBot crypto-ticker config</h1>
                    <form method="post">
                '''
            html += '<textarea name="configfile" rows="20" cols="80">' + str(fh.read()) + '</textarea>'
            html += '''
                        <div><input type="submit"/></div>
                    </form>
                </body>
                </html>
                    '''
            # html response
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html)))
            self.end_headers()
            self.wfile.write(bytes(html, "utf8"))

    def do_POST(self):
        # form vars
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST'})

        # write config file to disk
        with open(self.store_path, 'w') as fh:
            fh.write(form.getvalue('configfile'))

        # redirect to get action
        self.send_response(302)
        self.send_header('Location', self.path)
        self.end_headers()

# start the webserver
server = HTTPServer(('', 8080), StoreHandler)
server.serve_forever()