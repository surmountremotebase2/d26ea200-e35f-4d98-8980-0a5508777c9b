from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, SMA
from surmount.data import Asset
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the tickers of interest based on the provided defsymphony strategy
        self.tickers = ["SPY", "TQQQ", "UVXY", "SPXL", "TECL", "SQQQ", "BSV"]
        self.data_list = [Asset(i) for i in self.tickers]
    
    @property
    def interval(self):
        # Set the interval to daily as per the rebalance frequency indicated
        return "1day"
    
    @property
    def assets(self):
        return self.tickers
    
    @property
    def data(self):
        return self.data_list
    
    def run(self, data):
        allocation_dict = {}
        
        # Get the current prices and calculate the moving averages
        current_price_SPY = data["ohlcv"][-1]["SPY"]["close"]
        moving_average_SPY_200 = SMA("SPY", data["ohlcv"], 200)[-1]
        
        # Determine the conditions for selecting TQQQ or alternative ETFs
        if current_price_SPY > moving_average_SPY_200:
            rsi_TQQQ = RSI("TQQQ", data["ohlcv"], 10)[-1]
            if rsi_TQQQ > 79:
                allocation_dict["UVXY"] = 1.0
            else:
                rsi_SPXL = RSI("SPXL", data["ohlcv"], 10)[-1]
                if rsi_SPXL > 80:
                    allocation_dict["UVXY"] = 1.0
                else:
                    allocation_dict["TQQQ"] = 1.0
        else:
            rsi_TQQQ = RSI("TQQQ", data["ohlcv"], 10)[-1]
            if rsi_TQQQ < 31:
                allocation_dict["TECL"] = 1.0
            else:
                rsi_SPY = RSI("SPY", data["ohlcv"], 10)[-1]
                if rsi_SPY < 30:
                    allocation_dict["SPXL"] = 1.0
                else:
                    rsi_UVXY = RSI("UVXY", data["ohlcv"], 10)[-1]
                    if rsi_UVXY > 74:
                        allocation_dict["UVXY"] = 1.0
                    else:
                        # Simplified decision for else condition
                        allocation_dict["TQQQ"] = 1.0
        
        # Ensure only one allocation is selected for simplicity and compliance
        selected_asset = max(allocation_dict, key=allocation_dict.get)
        for ticker in self.tickers:
            allocation_dict[ticker] = 1.0 if ticker == selected_asset else 0.0
        
        return TargetAllocation(allocation_dict)