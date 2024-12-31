from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log
from surmount.data import Asset


class TradingStrategy(Strategy):
    def __init__(self):
        # Specify the tickers of interest
        self.tickers = ["BIL", "IBTK", "SPY", "SHY", "SOXL", "SOXS", "SQQQ", "TECL", "SBND", "HIBL"]
        
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
        rsi_sbnd = RSI("SBND", data["ohlcv"], length=10)
        rsi_hibl = RSI("HIBL", data["ohlcv"], length=10)
        
        # Check the conditions mentioned in the strategy
        if rsi_bil and rsi_ibtk and rsi_spy:
        if len(rsi_sbnd) > 0 and len(rsi_hibl) > 0:
            # Compare RSIs according to the given logic
            if rsi_bil[-1] < rsi_ibtk[-1]:
                if rsi_spy[-1] > 75:
                    allocation_dict["SHY"] = 1.0  # Allocate to SHY if SPY's RSI is above 75
                else:
                    allocation_dict["SOXL"] = 1.0  # Else, allocate to SOXL   
            # Check if the last RSI value of SBND is less than the last RSI value of HIBL
            elif rsi_sbnd[-1] < rsi_hibl[-1]:
                # If true, find the ticker with the lowest 7-days RSI between SOXS and SQQQ
                rsi_soxs = RSI("SOXS", data["ohlcv"], length=7)[-1]
                rsi_sqqq = RSI("SQQQ", data["ohlcv"], length=7)[-1]
                
                # Compare and allocate
                if rsi_soxs < rsi_sqqq:
                    allocation_dict = {"SOXS": 1}
                else:
                    allocation_dict = {"SQQQ": 1}
            else:
                # Else, find the ticker with the lowest 7-days RSI between SOXL and TECL
                rsi_soxl = RSI("SOXL", data["ohlcv"], length=7)[-1]
                rsi_tecl = RSI("TECL", data["ohlcv"], length=7)[-1]
                
                # Compare and allocate
                if rsi_soxl < rsi_tecl:
                    allocation_dict = {"SOXL": 1}
                else:
                    allocation_dict = {"TECL": 1}
        else:
            log("RSI data for SBND or HIBL is not available.")
                
        return TargetAllocation(allocation_dict)