import yfinance

class Exchange():
    def __init__(self, config):
        self.config = config

    def fetch_history(self):
        ticker = yfinance.Ticker(self.config.stock_symbol())
        history =ticker.history(interval='1d', period='1mo')
        return history
