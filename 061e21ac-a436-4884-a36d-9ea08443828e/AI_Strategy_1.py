from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the tickers we're interested in
        self.tickers = ["SBND", "HIBL", "SOXS", "SQQQ", "SOXL", "TECL"]
    
    @property
    def interval(self):
        # Use daily data
        return "1day"
    
    @property
    def assets(self):
        # Assets that the strategy will trade
        return self.tickers
    
    def run(self, data):
        # Initialize an empty allocation dictionary
        allocation_dict = {}
        
        # Calculate the 10-days RSI for SBND and HIBL
        rsi_sbnd = RSI("SBND", data["ohlcv"], length=10)
        rsi_hibl = RSI("HIBL", data["ohlcv"], length=10)

        if len(rsi_sbnd) > 0 and len(rsi_hibl) > 0:
            # Check if the last RSI value of SBND is less than the last RSI value of HIBL
            if rsi_sbnd[-1] < rsi_hibl[-1]:
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