from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, SMA
from surmount.data import Asset
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["TQQQ", "UVXY", "TECL", "SPXL", "SQQQ"]
        self.spy = "SPY"

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    def run(self, data):
        allocation_dict = {}

        # SPY as a market indicator
        spy_rsi = RSI("SPY", data["ohlcv"], length=10)[-1]
        spy_price = data["ohlcv"][-1]["SPY"]["close"]
        spy_ma200 = SMA("SPY", data["ohlcv"], length=200)[-1]

        if spy_price > spy_ma200:  # Bull market condition
            tqqq_rsi = RSI("TQQQ", data["ohlcv"], length=10)[-1]
            if tqqq_rsi > 79:
                allocation_dict["UVXY"] = 1.0  # Shift to UVXY in overheated conditions
            else:
                allocation_dict["TQQQ"] = 1.0  # Prefer TQQQ for growth
        else:  # Bear market or correction condition
            spy_rsi = RSI("SPY", data["ohlcv"], length=10)[-1]
            if spy_rsi < 30:
                allocation_dict["SPXL"] = 1.0  # Opt for SPXL in a recovering SPY situation
            else:
                uvxy_rsi = RSI("UVXY", data["ohlcv"], length=10)[-1]
                if uvxy_rsi > 74:
                    allocation_dict["UVXY"] = 1.0  # Increase UVXY allocation in volatility
                else:
                    allocation_dict["TECL"] = 1.0  # Shift to TECL as a tech-sector bet

        return TargetAllocation(allocation_dict)