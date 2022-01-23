import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from src import stock_exchanges
from src.configuration import bitbot_config

# '1wk' <- failes for reasons as yet unknown
test_params = ["1mo", '1wk',  'random']


class test_stock_exchange(unittest.TestCase):
    def test_fetcing_history(self):
        for candle_width in test_params:
            with self.subTest(msg=candle_width):
                stock = "TSLA"
                mock_config = {
                    "currency": {
                        "stock_symbol": stock
                    },
                    "display": {
                        "candle_width": candle_width,
                        "disk_file_name": "last_display.png"
                    }
                }
                excange = stock_exchanges.Exchange(bitbot_config.BitBotConfig(mock_config))
                data = excange.fetch_history()
                self.assertTrue(len(data.candle_data) > 0, msg=f'got {len(data.candle_data)} candles for {stock}')
