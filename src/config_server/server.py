import io
import os
import pathlib
import time
import uuid
from configuration.bitbot_files import BitBotFiles
from configuration.bitbot_config import load_config_ini
from flask import Flask, render_template, request, redirect, url_for
from PIL import Image


app = Flask(__name__)

# 🗂️ setup config
base_dir = os.path.join(pathlib.Path(__file__).parent.resolve(), '../../')
files_config = BitBotFiles(base_dir)
app_config = load_config_ini(files_config)


def config_files_ending_with(ending):
    return list(filter(lambda f: f.endswith(ending), files_config.all_files.keys()))


# 🗂️ list style and config files
style_files = config_files_ending_with("mplstyle")
ini_files = config_files_ending_with("ini")


@app.route('/')
def index():
    return render_template(
        'index.html',
        style_files=style_files,
        ini_files=ini_files,
        config=app_config)


@app.route('/file/<file>', methods=['POST', 'GET'])
def file(file):
    if request.method == 'POST':
        file_path = files_config.all_files.get(file)
        with open(file_path, 'w') as fh:
            fh.write(request.form['file'])
        return redirect(request.url)
    else:
        file_path = files_config.all_files.get(file)
        with open(file_path) as fh:
            return render_template('file.html', file=fh.read(), file_name=file)


@app.route('/modes/picture', methods=['POST'])
def picture_mode():
    photo_mode_state = request.form.get('enable_picture_mode') or 'false'
    image_file = request.files['image_file']
    app_config.toggle_photo_mode(photo_mode_state)
    if(photo_mode_state == 'true' and image_file):
        picture = Image.open(io.BytesIO(image_file.read()), mode='r')
        picture_file = app_config.set_photo_image_file(uuid.uuid4().hex)
        picture.save(picture_file, format="png")
    app_config.save()
    return redirect(url_for('index'))


@app.route('/logs')
def logs():
    def generate():
        with open(files_config.log_file_path) as f:
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.1)
                    continue

                yield line

    return app.response_class(generate(), mimetype='text/plain')
