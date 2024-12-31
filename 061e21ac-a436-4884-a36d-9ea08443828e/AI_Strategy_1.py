from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, SMA
from surmount.data import Asset, OHLCV
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Focus on TQQQ for the main asset and SPY for comparison
        self.tickers = ["TQQQ", "SPY"]

    @property
    def interval(self):
        # Daily rebalance frequency as specified
        return "1day"

    @property
    def assets(self):
        return self.tickers

    def run(self, data):
        allocation_dict = {}

        # Calculate the RSI and SMA for SPY to determine market conditions
        rsi_spy = RSI("SPY", data["ohlcv"], length=10)[0]  # Simplified, should handle more safely in production
        sma_spy_200 = SMA("SPY", data["ohlcv"], length=200)[0]  # Same note as above

        # Get current SPY price vs. its 200-day SMA
        spy_price = data["ohlcv"][-1]["SPY"]["close"]  # Simplified access, assuming data existence

        # Strategy Logic Simplification:
        if spy_price > sma_spy_200:
            # Market in an uptrend, focus on TQQQ
            rsi_tqqq = RSI("TQQQ", data["ohlcv"], length=10)[0]  # Assume data exists for simplicity
            if rsi_tqqq > 79:
                allocation_dict["TQQQ"] = 0  # Assuming avoid buying if overbought
            else:
                allocation_dict["TQQQ"] = 1
        else:
            # Market in a downtrend, could consider hedging or avoiding trades
            allocation_dict["TQQQ"] = 0

        return TargetAllocation(allocation_dict)