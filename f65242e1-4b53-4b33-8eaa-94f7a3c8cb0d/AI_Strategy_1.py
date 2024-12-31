from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # List of tickers to be included in the strategy
        self.tickers = ["QQQ", "SPY", "BSV", "UVXY"]
        # Setting up a standard period length for RSI calculation
        self.rsi_length = 14
    
    @property
    def assets(self):
        # The assets that this strategy is interested in
        return self.tickers

    @property
    def interval(self):
        # Data interval for RSI calculation, assuming daily data is used
        return "1day"
    
    def run(self, data):
        # Initialize a dictionary to store RSI values for each asset
        rsi_values = {}
        for ticker in self.tickers:
            # Calculating RSI for the ticker
            rsi = RSI(ticker, data["ohlcv"], self.rsi_length)
            if rsi is not None and len(rsi) > 0:
                # Store the latest RSI value
                rsi_values[ticker] = rsi[-1]
        
        # Find the ticker with the highest RSI value
        if rsi_values:
            highest_rsi_ticker = max(rsi_values, key=rsi_values.get)
            log(f"Highest RSI is for {highest_rsi_ticker} with a value of {rsi_values[highest_rsi_ticker]}")
            # Setting target allocation for the asset with the highest RSI
            allocation_dict = {ticker: 1.0 if ticker == highest_rsi_ticker else 0 for ticker in self.tickers}
        else:
            # If no RSI values are calculatable (e.g., lack of data), no allocation is made
            log("No valid RSI values found. Skipping allocation.")
            allocation_dict = {ticker: 0 for ticker in self.tickers}
        
        return TargetAllocation(allocation_dict)