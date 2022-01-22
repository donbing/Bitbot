import os, configparser
from src.log_decorator import info_log

@info_log
def load_config_ini(config_ini_path):
    config = configparser.ConfigParser()
    config.read(config_ini_path, encoding='utf-8')
    return BitBotConfig(config)

# encapsulate horrid config vars
class BitBotConfig():
    def __init__(self, config):
        self.config = config

    def exchange_name(self):
        return self.config["currency"]["exchange"]

    def instrument_name(self):
        return self.config["currency"]["instrument"]

    def use_inky(self):
        return os.getenv('BITBOT_OUTPUT') != 'disk' and self.config["display"]["output"] == "inky"

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
    
    def set(self, section, key, value):
        self.config.set(section, key, value)
        
    def reload(self, config_ini_path):
        self.config.read(config_ini_path, encoding='utf-8')
    
    def refresh_rate_minutes(self):
        return float(self.config['display']['refresh_time_minutes'])