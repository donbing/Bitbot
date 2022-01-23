import sys, os, unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from src import stock_exchanges
from src.configuration import bitbot_config

class test_stock_exchange(unittest.TestCase):
    def test_fetcing_history(self):
        mock_config = {"currency":{"stock_symbol":"AAPL"}}
        excange = stock_exchanges.Exchange(bitbot_config.BitBotConfig(mock_config))
        data = excange.fetch_history()
        self.assertIsNotNone(data)