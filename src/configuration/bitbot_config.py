import os
import configparser
from .log_decorator import info_log
from os.path import join as pjoin


@info_log
def load_config_ini(config_files):
    config = configparser.ConfigParser()
    config.read(config_files.config_ini, encoding='utf-8')
    return BitBotConfig(config, config_files)


# 🙈 encapsulate horrid config vars
class BitBotConfig():
    def __init__(self, config, config_files):
        self.config = config
        self.config_files = config_files

    # 🏦 currency options
    def exchange_name(self):
        return self.config["currency"]["exchange"]

    def instrument_name(self):
        return self.config["currency"]["instrument"]

    def stock_symbol(self):
        return self.config['currency']['stock_symbol']

    def portfolio_size(self):
        try:
            return self.config.getfloat('currency', 'holdings', fallback=0)
        except ValueError:
            return 0

    def chart_since(self):
        return self.config.get('currency', 'chart_since', fallback=None)

    def set_currency(self, formData):
        for key in ['exchange', 'instrument', 'stock_symbol', 'holdings']:
            self.config["currency"][key] = formData[key]
        self.save()

    # 📈 display options
    def use_inky(self):
        dont_write_to_disk = os.getenv('BITBOT_OUTPUT') != 'disk'
        do_write_to_inky = self.config["display"]["output"] == "inky"
        return dont_write_to_disk and do_write_to_inky

    def get_price_action_comments(self, direction):
        return self.config.get('comments', direction).split(',')

    def border_type(self):
        return self.config["display"]["border"]

    def overlay_type(self):
        return self.config["display"]["overlay_layout"]

    def show_timestamp(self):
        return self.config["display"]["timestamp"]

    def expand_chart(self):
        return self.config["display"]["expanded_chart"] == 'true'

    def toggle_expanded_chart(self, new_state):
        self.config["display"]["expanded_chart"] = new_state

    def show_volume(self):
        return self.config["display"]["show_volume"] == 'true'

    def toggle_volume(self, new_state):
        self.config["display"]["show_volume"] = new_state

    def refresh_rate_minutes(self):
        return float(self.config['display']['refresh_time_minutes'])

    def display_rotation(self):
        return int(self.config['display']['rotation'])

    def output_file_name(self):
        return self.config['display']['disk_file_name']

    def candle_width(self):
        return self.config['display']['candle_width']

    def show_ip(self):
        return self.config['display']['show_ip']

    def set_display(self, formData):
        for key in ['border', 'overlay_layout', 'timestamp', 'expanded_chart', 'show_volume', 'show_ip', 'refresh_time_minutes', 'candle_width']:
            self.config["display"][key] = formData.get(key, 'false')
        self.save()

    # 🖼️ picture frame mode
    def toggle_photo_mode(self, enabled_state, cycle_state):
        self.config['picture_frame_mode']["enabled"] = enabled_state
        self.config['picture_frame_mode']["cycle_pictures"] = cycle_state

    def photo_mode_enabled(self):
        return self.config['picture_frame_mode']["enabled"] == 'true'

    def cycle_pictures_enabled(self):
        return self.config['picture_frame_mode']["cycle"] == 'true'

    def set_photo_image_file(self, unique_file_id):
        unique_file_name = f'{unique_file_id}.png'
        self.set('picture_frame_mode', 'picture_file_name', unique_file_name)
        return self.photo_image_file()

    def photo_image_file(self):
        return pjoin(
            self.config_files.photos_folder,
            self.config['picture_frame_mode']['picture_file_name']
        )

    # 🐞 debug helpers
    def shoud_show_image_in_vscode(self):
        return os.getenv('BITBOT_SHOWIMAGE') == 'true'

    def is_test_run(self):
        return os.getenv('TESTRUN') == 'true'

    # ⚙️ config management options
    def set(self, section, key, value):
        self.config.set(section, key, value)

    def reload(self):
        self.config.read(self.config_files.config_ini, encoding='utf-8')

    def save(self):
        with open(self.config_files.config_ini, 'w') as f:
            self.config.write(f)

    # 🌱 intro setup
    def on_first_run(self, action):
        if self.config["first_run"]['enabled'] == "true":
            action()
            self.set('first_run', 'enabled', "false")
            self.save()

    def intro_background(self):
        return pjoin(
            self.config_files.resource_folder,
            self.config['first_run']['intro_background_image']
        )
