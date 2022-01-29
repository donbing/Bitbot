from flask import Flask, render_template
import os

app = Flask(__name__)


def find_config_directory_path():
    default_config_dir = "../../config"
    env_config_dir = os.getenv("BITBOT__CONFIG_DIR")
    return env_config_dir or default_config_dir


@app.route('/')
def index():
    config_dir = find_config_directory_path()
    config_file_paths = [file for file in os.listdir(config_dir) if os.path.isfile(os.path.join(config_dir, file))]

    style_files = list(filter(lambda file: file.endswith("mplstyle"), config_file_paths))
    ini_files = list(filter(lambda file: file.endswith("ini"), config_file_paths))
    return render_template(
        'index.html',
        style_files=style_files,
        ini_files=ini_files)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
