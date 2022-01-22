import unittest, pathlib, os, sys
from os.path import join as pjoin
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from src import bitbot, crypto_exchanges
from src.configuration.bitbot_files import use_config_dir 
from src.configuration.bitbot_config import load_config_ini 

# check config files 
curdir = pathlib.Path(__file__).parent.resolve()
files = use_config_dir(pjoin(curdir, "../"))

# load config
config = load_config_ini(files.config_ini)
config.set('display', 'output', 'disk')

class test_rendering_chart(unittest.TestCase):
    def test_with_config(self):
        exchange = bitbot.chart_updater(config)
        exchange.run()
        #os.system("code last_display.png")    
        # open the file in vscode for approval

def suite():
    #chart_data = chart_data_fetcher.fetch_OHLCV_chart_data('5m', 24, 'bitmex', 'BTC/USD')
    suite = unittest.TestSuite()
    suite.addTest(test_rendering_chart('test_default_widget_size'))
    suite.addTest(test_rendering_chart('test_widget_resize'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())