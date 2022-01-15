import pathlib
import os
import os.path
from os.path import join as pjoin
import cgi
from http.server import BaseHTTPRequestHandler, HTTPServer

class StoreHandler(BaseHTTPRequestHandler):
    curdir = pathlib.Path(__file__).parent.resolve()
    store_path = pjoin(curdir, '../', 'config.ini')
    log_path = pjoin(curdir, '../', 'debug.log')
    
    def do_GET(self):
        with open(self.store_path) as store_file:
            # html for config editor
            html = '''
                <!DOCTYPE html>
                <html>
                <head>
                    <meta content="text/html;charset=utf-8" http-equiv="Content-Type">
                    <meta content="utf-8" http-equiv="encoding">
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css">
                </head>
                <body>
                    <h1>BitBot crypto-ticker config</h1>
                    <form method="post">
                '''
            html += '<textarea name="configfile" rows="20" cols="80">' + str(store_file.read()) + '</textarea>'
            html += '''
                        <div><input type="submit" value="Save and Reboot"></input></div>
                    </form>
                    '''
            # display log info if it exists
            if os.path.isfile(self.log_path):
                with open(self.log_path) as log_file:
                    html += '<h1>LOG</h1><textarea name="configfile" rows="20" cols="80">' + str(log_file.read()) + '</textarea>'

            html += '''
                </body>
                </html>
                    '''
            # html response
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html)))
            self.end_headers()
            self.wfile.write(bytes(html, "utf8"))
            os.system('sudo reboot now')    

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