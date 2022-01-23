import unittest, pathlib, os, sys, uuid
from os.path import join as pjoin
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from src import bitbot
from src.configuration.bitbot_files import use_config_dir 
from src.configuration.bitbot_config import load_config_ini 

# check config files 
curdir = pathlib.Path(__file__).parent.resolve()
files = use_config_dir(pjoin(curdir, "../"))

def load_config():
    config = load_config_ini(files.config_ini)
    config.set('display', 'output', 'disk')
    return config


# load config
test_params = [
    ("MS, defaults", "", "", "MSFT", "1", "false", "false", "1mo"),
    ("APPLE, defaults", "", "", "AAPL", "1", "false", "false", "3mo"),
]

class test_rendering_chart(unittest.TestCase):
    def test_render(self):
        config = load_config()
        for name, exchange, token, stock, overlay, expand, volume, candle_width in test_params:
            with self.subTest(msg=name):
                image_file_name = f'{name}.png'
                config.set('currency', 'stock_symbol', stock)
                config.set('currency', 'exchange', exchange)
                config.set('currency', 'instrument', token)
                config.set('display', 'overlay_layout', overlay)
                config.set('display', 'expanded_chart', expand)
                config.set('display', 'show_volume', volume)
                config.set('display', 'candle_width', candle_width)
                config.set('display', 'disk_file_name', image_file_name)
                exchange = bitbot.BitBot(config, files)
                exchange.run()
                #os.system(f"code {image_file_name}")
