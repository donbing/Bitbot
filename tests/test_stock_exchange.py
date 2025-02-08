import unittest
from src.exchanges import stock_exchanges
from src.configuration import bitbot_config, bitbot_files
from src.configuration.bitbot_files import use_config_dir
from src.configuration.bitbot_config import load_config_ini
import os
import pathlib


# 🪳 ''1h',' <- fails on weekends due to short chart duration
test_params = ['1mo', '1h', '1wk', 'random']

curdir = pathlib.Path(__file__).parent.resolve()
files = use_config_dir(os.path.join(curdir, "../"))
config_ini = load_config_ini(files)


class TestStockExchange(unittest.TestCase):
    def test_fetching_history(self):
        for candle_width in test_params:
            with self.subTest(msg=candle_width):
                self.run_test(candle_width)

    def run_test(self, candle_width):
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
        config = bitbot_config.BitBotConfig(mock_config, {})
        excange = stock_exchanges.Exchange(config)

        data = excange.fetch_history()
        num_candles = len(data.candle_data)

        we_got_candles = num_candles > 0
        self.assertTrue(we_got_candles, msg=f'got {num_candles} candles for {stock}')
