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
    ("MSFT 1mo defaults", "", "", "MSFT", "1", "false", "false", "1mo", ""),
    ("APPLE 3mo defaults", "", "", "AAPL", "1", "false", "false", "3mo", ""),

    ("bitmex BTC 5m defaults", "bitmex", "BTC/USD", "", "1", "false", "false", "5m", ""),
    ("bitmex BTC 1h defaults", "bitmex", "BTC/USD", "", "1", "false", "false", "1h", ""),
    ("bitmex BTC 1d defaults", "bitmex", "BTC/USD", "", "1", "false", "false", "1d", ""),
    ("BTC HOLDINGS", "bitmex", "BTC/USD", "", "1", "false", "false", "1d", "100"),

    ("bitmex ETH 5m defaults", "bitmex", "ETH/USD", "", "1", "false", "false", "5m", ""),
    ("bitmex ETH 1h defaults", "bitmex", "ETH/USD", "", "1", "false", "false", "1h", ""),
    ("bitmex ETH 1d defaults", "bitmex", "ETH/USD", "", "1", "false", "false", "1d", ""),

    ("cryptocom CRO 5m defaults", "cryptocom", "CRO/USDC", "", "1", "false", "false", "5m", ""),
    ("cryptocom CRO 1h defaults", "cryptocom", "CRO/USDC", "", "1", "false", "false", "1h", ""),
    ("cryptocom CRO 1d defaults", "cryptocom", "CRO/USDC", "", "1", "false", "false", "1d", ""),
]

os.makedirs('tests/images/', exist_ok=True)

class TestRenderingMeta(type):
    def __new__(mcs, name, bases, dict):

        def gen_test(name, exch, token, stock, overlay, expand, volume, candle_width, holdings):
            def test(self):
                config = load_config()
                image_file_name = f'tests/images/{name}.png'
                config.set('currency', 'stock_symbol', stock)
                config.set('currency', 'exchange', exch)
                config.set('currency', 'instrument', token)
                config.set('currency', 'holdings', holdings)
                config.set('display', 'overlay_layout', overlay)
                config.set('display', 'expanded_chart', expand)
                config.set('display', 'show_volume', volume)
                config.set('display', 'candle_width', candle_width)
                config.set('display', 'disk_file_name', image_file_name)
                exchange = bitbot.BitBot(config, files)
                exchange.run()
                #os.system(f"code {image_file_name}")

            return test

        for name, exchange, token, stock, overlay, expand, volume, candle_width, holdings in test_params:
            test_name = "test_%s" % name
            dict[test_name] = gen_test(name, exchange, token, stock, overlay, expand, volume, candle_width, holdings)
        return type.__new__(mcs, name, bases, dict)

class ChartRenderingTests(unittest.TestCase, metaclass=TestRenderingMeta):
    __metaclass__ = TestRenderingMeta