import os
import configparser
from .log_decorator import info_log


@info_log
def load_config_ini(config_ini_path):
    config = configparser.ConfigParser()
    config.read(config_ini_path, encoding='utf-8')
    return BitBotConfig(config, config_ini_path)


# encapsulate horrid config vars
class BitBotConfig():
    def __init__(self, config, path):
        self.config = config
        self.config_path = path

    def exchange_name(self):
        return self.config["currency"]["exchange"]

    def instrument_name(self):
        return self.config["currency"]["instrument"]

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

    def show_volume(self):
        return self.config["display"]["show_volume"] == 'true'

    def display_dimensions(self):
        return (
            int(self.config["display"]["width"]),
            int(self.config["display"]["height"])
        )

    def set(self, section, key, value):
        self.config.set(section, key, value)

    def reload(self, config_ini_path):
        self.config.read(config_ini_path, encoding='utf-8')

    def refresh_rate_minutes(self):
        return float(self.config['display']['refresh_time_minutes'])

    def display_rotation(self):
        return int(self.config['display']['rotation'])

    def shoud_show_image_in_vscode(self):
        return os.getenv('BITBOT_SHOWIMAGE') == 'true'

    def is_test_run(self):
        return os.getenv('TESTRUN') == 'true'

    def stock_symbol(self):
        return self.config['currency']['stock_symbol']

    def portfolio_size(self):
        try:
            return self.config.getfloat('currency', 'holdings', fallback=0)
        except ValueError:
            return 0

    def output_file_name(self):
        return self.config['display']['disk_file_name']

    def candle_width(self):
        return self.config['display']['candle_width']

    def save(self):
        with open(self.config_path, 'w') as f:
            self.config.write(f)

    # 🎞️ photo frame mode
    def toggle_photo_mode(self, newState):
        self.config['picture_frame_mode']["enabled"] = newState
    
    def photo_mode_enabled(self):
        return self.config['picture_frame_mode']["enabled"] == 'true'

    def photo_image_file(self):
        return self.config['picture_frame_mode']["picture_file_name"]
