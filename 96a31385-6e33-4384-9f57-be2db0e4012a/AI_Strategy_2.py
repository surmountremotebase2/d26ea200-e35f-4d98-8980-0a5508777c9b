from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the tickers you want to examine.
        self.tickers = ["SQQQ", "BSV"]

    @property
    def assets(self):
        # Return the list of assets this strategy concerns.
        return self.tickers

    @property
    def interval(self):
        # Set the interval for data collection; "1day" suits the 10-day RSI calculation.
        return "1day"

    def run(self, data):
        # Initialize an empty allocation dictionary.
        allocation_dict = {}
        
        # Calculate the 10-day RSI for each ticker.
        rsi_values = {ticker: RSI(ticker, data["ohlcv"], 10)[-1] for ticker in self.tickers}
        
        # Log the RSI values for monitoring.
        log(f"RSI Values: {rsi_values}")
        
        # Determine the ticker with the highest RSI value.
        target_ticker = max(rsi_values, key=rsi_values.get)
        
        # Allocate fully to the ticker with the higher RSI, assuming it indicates stronger momentum.
        allocation_dict[target_ticker] = 1.0
        
        # Return the target allocation.
        return TargetAllocation(allocation_dict)