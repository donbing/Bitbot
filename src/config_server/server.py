import os
import pathlib
import uuid
from configuration.bitbot_files import BitBotFiles
from configuration.bitbot_config import load_config_ini
from flask import Flask, render_template, request, redirect
from PIL import Image


app = Flask(__name__)


def find_config_directory_path():
    default_config_dir = "/home/chris/bitbot/config/"
    env_config_dir = os.getenv("BITBOT__CONFIG_DIR")
    return env_config_dir or default_config_dir


# 🗂️ get all files in config directory
config_dir = find_config_directory_path()
config_file_paths = [
    file
    for file in os.listdir(config_dir)
    if os.path.isfile(os.path.join(config_dir, file))]


def get_file(file):
    print(file)
    return os.path.join(config_dir, config_files_ending_with(file)[0])


def config_files_ending_with(ending):
    return list(filter(lambda file: file.endswith(ending), os.listdir(config_dir)))


# 🗂️ list style and config files in config dir
style_files = config_files_ending_with("mplstyle")
ini_files = config_files_ending_with("ini")


base_dir = os.path.join(pathlib.Path(__file__).parent.resolve(), '../')

files_config = BitBotFiles(base_dir)

app_config = load_config_ini(files_config)


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
        file_path = get_file(file)
        with open(file_path, 'w') as fh:
            fh.write(request.form['file'])
        return redirect(request.url)
    else:
        file_path = get_file(file)
        with open(file_path) as fh:
            return render_template('file.html', file=fh.read(), file_name=file)


@app.route('/modes/picture', methods=['POST'])
def picture_mode():
    photo_mode_toggleState, = request.form.get('enabled', ['false'])
    image_file = request.files['image_file'][0]
    app_config.toggle_photo_mode(photo_mode_toggleState)
    if(photo_mode_toggleState == 'true' and image_file):
        picture = Image.open(file.read(), mode='r')
        picture_file = app_config.set_photo_image_file(uuid.uuid4().hex)
        picture.save(picture_file, format="png")
    app_config.save()
