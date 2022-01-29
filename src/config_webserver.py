import pathlib
import os
import os.path
from os.path import join as pjoin
import cgi
import io
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse as urlparse
from configuration.bitbot_files import BitBotFiles
from configuration.bitbot_config import load_config_ini
from PIL import Image

base_dir = pjoin(pathlib.Path(__file__).parent.resolve(), '../')

files_config = BitBotFiles(base_dir)

config = load_config_ini(files_config.config_ini)

editable_files = {
    "config_ini": files_config.config_ini,
    "base_style": files_config.base_style,
    "inset_style": files_config.inset_style,
    "default_style": files_config.default_style,
    "volume_style": files_config.volume_style
}


class StoreHandler(BaseHTTPRequestHandler):

    def create_image_upload_form(self):
        html = f'''
            <h1 class="collapser">📸 Photo Mode 🔃</h1>
            <form action="/image_upload" enctype='multipart/form-data' method='post'>
                <label for="enabled">Enabled:</label>
                <input type="checkbox" id="enabled" name="enabled" value="true" {"checked" if config.photo_mode_enabled() else ""}/>
                <label for="img">🖼️ Select image:</label>
                <input type="file" id="img" name="image_file" accept="image/*"/>
                <input type="submit"/>
            </form>
        '''
        return html

    def create_editor_form(self, fileKey, current_file_key):
        with open(editable_files[fileKey]) as file_handle:
            html = '<h2 class="collapser">⚙️ ' + fileKey + ' 🔃</h2>'
            html += '<form method="post" action="?fileKey=' + fileKey + '"' + ' class="' + ('open' if fileKey == current_file_key else '') + '">'
            html += '<textarea name="fileContent" rows="20" cols="80">' + str(file_handle.read()) + '</textarea>'
            html += '<div><input type="submit" value="Save"></input></div></form>'
            return html

    def do_GET(self):
        param = urlparse.parse_qs(urlparse.urlparse(self.path).query).get('fileKey', [])
        fileKey = next((x for x in param), None)
        # html for config editor
        html = '''
            <!DOCTYPE html>
            <html>
            <head>
                <meta content="text/html;charset=utf-8" http-equiv="Content-Type">
                <meta content="utf-8" http-equiv="encoding">
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css">
                <style>
                    form { display: none; }
                    form.open { display:block; }
                    .collapser { cursor: pointer; }
                </style>
                <script>
                    window.onload= function(){
                        var coll = document.getElementsByClassName("collapser");
                        for (var i = 0; i < coll.length; i++) {
                            coll[i].addEventListener("click", function() {
                                    var content = this.nextElementSibling;
                                content.style.display = content.style.display === "block" ? "none" : "block";
                            });
                        }
                    }
                </script>
            </head>
            <body>
                <h1>🤖 BitBot Crypto-Ticker Config</h1>
            '''
        for file in editable_files:
            html += self.create_editor_form(file, fileKey)

        html += self.create_image_upload_form()

        # display log info if it exists
        if os.path.isfile(files_config.log_file_path):
            with open(files_config.log_file_path) as log_file:
                html += '<h1 class="collapser">🪵 LOG 🔃</h1><textarea name="configfile" rows="20" cols="80">' + str(log_file.read()) + '</textarea>'

        html += '</body></html>'
        # html response
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html)))
        self.end_headers()
        self.wfile.write(bytes(html, "utf8"))

    def do_POST(self):
        content_type, pdict = cgi.parse_header(self.headers['content-type'])

        # handle picture frame settings
        if(content_type == 'multipart/form-data'):
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            fields = cgi.parse_multipart(self.rfile, pdict)
            photo_mode_toggleState, = fields['enabled'] or 'false'
            config.toggle_photo_mode(photo_mode_toggleState)
            if(photo_mode_toggleState == 'true'):
                picture = Image.open(io.BytesIO(fields['image_file'][0]), mode='r')
                image = picture.resize(config.display_dimensions())
                picture_file = config.photo_image_file()
                image.save(picture_file, format="png")
            config.save()
        else:
            # handle file content change
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'})

            fileKey = urlparse.parse_qs(urlparse.urlparse(self.path).query).get('fileKey', None)[0]

            # write file to disk
            with open(editable_files[fileKey], 'w') as fh:
                fh.write(form.getvalue('fileContent'))

        # redirect to get action
        self.send_response(302)
        self.send_header('Location', self.path)
        self.end_headers()


# start the webserver
server = HTTPServer(('', 8080), StoreHandler)
server.serve_forever()
