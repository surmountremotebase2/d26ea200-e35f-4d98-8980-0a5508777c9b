from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log
from surmount.data import Asset


class TradingStrategy(Strategy):
    def __init__(self):
        # Specify the tickers of interest
        self.tickers = ["BIL", "IBTK", "SPY", "SHY", "SOXL", "SOXS", "SQQQ", "TECL"]
        
    @property
    def assets(self):
        return self.tickers
    
    @property
    def interval(self):
        # Set the interval for data collection, matching the defsymphony's daily rebalance frequency
        return "1day"
    
    def run(self, data):
        # Initialize allocation dictionary
        allocation_dict = {ticker: 0 for ticker in self.tickers}
        
        # Calculate RSIs for comparison
        rsi_bil = RSI("BIL", data["ohlcv"], 5)
        rsi_ibtk = RSI("IBTK", data["ohlcv"], 7)
        rsi_spy = RSI("SPY", data["ohlcv"], 6)
        
        # Check the conditions mentioned in the strategy
        if rsi_bil and rsi_ibtk and rsi_spy:
            # Compare RSIs according to the given logic
            if rsi_bil[-1] < rsi_ibtk[-1]:
                if rsi_spy[-1] > 75:
                    allocation_dict["SHY"] = 1.0  # Allocate to SHY if SPY's RSI is above 75
                else:
                    allocation_dict["SOXL"] = 1.0  # Else, allocate to SOXL
            else:
                # This section hints at a complex conditional structure not fully detailed in the provided strategy.
                # As specifics are missing, we'll exemplify a simple RSI comparison leading to a choice between SOXS and TECL
                allocation_dict["TECL"] = 0.5  # Split allocation between SOXS and TECL as a placeholder
                allocation_dict["SOXS"] = 0.5
                
        return TargetAllocation(allocation_dict)