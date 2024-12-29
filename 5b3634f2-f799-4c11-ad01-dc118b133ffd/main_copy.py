from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["TQQQ", "UVXY"]
        self.data_list = [Asset(i) for i in self.tickers]

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        # Define short-term and long-term moving averages
        short_term_window = 50
        long_term_window = 200
        
        # Fetch closing prices for the calculation of moving averages
        tqqq_closing_prices = [i["TQQQ"]["close"] for i in data["ohlcv"]]
        uvxy_closing_prices = [i["UVXY"]["close"] for i in data["ohlcv"]]
        
        # Calculate moving averages
        short_term_sma = SMA("TQQQ", {"ohlcv": data["ohlcv"]}, short_term_window)
        long_term_sma = SMA("TQQQ", {"ohlcv": data["ohlcv"]}, long_term_window)

        # Ensure enough data points are present
        if len(tqqq_closing_prices) < long_term_window or len(uvxy_closing_prices) < long_term_window:
            log("Not enough data for moving averages.")
            return TargetAllocation({})

        # Strategy Logic
        if short_term_sma[-1] > long_term_sma[-1]:
            # Bull Market, hold or buy TQQQ
            return TargetAllocation({"TQQQ": 1, "UVXY": 0})
        else:
            # Bear Market, sell TQQQ if held and buy UVXY
            return TargetAllocation({"TQQQ": 0, "UVXY": 1})