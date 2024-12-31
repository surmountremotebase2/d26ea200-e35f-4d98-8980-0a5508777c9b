from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):

    def __init__(self):
        # Defining the tickers this strategy will evaluate
        self.tickers = ["SQQQ", "BSV"]

    @property
    def interval(self):
        # The time interval for data - daily data is used here.
        return "1day"

    @property
    def assets(self):
        # Signals which assets we're interested in for this strategy
        return self.tickers

    def run(self, data):
        # Initialize a dict to hold the RSI values
        rsi_values = {}
        
        # Calculate the 10-day RSI for each ticker
        for ticker in self.tickers:
            # Using the RSI function provided by Surmount to calculate the 10-day RSI
            rsi_values[ticker] = RSI(ticker, data["ohlcv"], length=10)[-1] if len(data["ohlcv"]) >= 10 else None

        # Logging for debugging purposes; to monitor RSI values
        log(f"RSI Values: {rsi_values}")
        
        if all(value is None for value in rsi_values.values()):
            # If we have no RSI data for any ticker, allocate nothing
            allocation_ratio = {ticker: 0 for ticker in self.tickers}
        else:
            # Identify the asset with the highest RSI value and set its allocation to 1 (100%)
            highest_rsi_asset = max(rsi_values, key=rsi_values.get)
            allocation_ratio = {ticker: 1 if ticker == highest_rsi_asset else 0 for ticker in self.tickers}

        # Log the asset chosen for allocation
        log(f"Allocating to: {highest_rsi_asset} with highest RSI")
        return TargetAllocation(allocation_ratio)