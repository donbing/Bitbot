import unittest, pathlib, os, sys, configparser
from os.path import join as pjoin
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from src import bitbot, chart_data_fetcher


curdir = pathlib.Path(__file__).parent.resolve()
config_dir = pjoin(curdir, "../", 'config')

# load config
config_ini_path = pjoin(config_dir, 'config.ini')
config = configparser.ConfigParser()
config.read(config_ini_path, encoding='utf-8')

config.set('display', 'output','disk')

class test_rendering_chart(unittest.TestCase):
    def test_with_config(self):
        exchange = bitbot.chart_updater(config)
        exchange.run()
        os.system("code last_display.png")    
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