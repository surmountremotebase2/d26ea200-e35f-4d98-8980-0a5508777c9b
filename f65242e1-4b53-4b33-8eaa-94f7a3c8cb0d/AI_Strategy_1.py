from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    
    @property
    def assets(self):
        # Specifies TQQQ as the asset of interest
        return ["TQQQ"]
    
    @property
    def interval(self):
        # Sets data interval to '1day' for daily RSI evaluation
        return "1day"

    def run(self, data):
        # Calculate RSI over 14 days, which is a common period for RSI calculation
        rsi_values = RSI("TQQQ", data["ohlcv"], 14)
        
        if len(rsi_values) < 2:
            # If there's insufficient data for RSI calculation, do not allocate
            log("Insufficient data for RSI calculation")
            return TargetAllocation({})
        
        # RSI values for the most recent two days
        yesterday_rsi = rsi_values[-2]
        today_rsi = rsi_values[-1]
        
        log(f"Yesterday's RSI: {yesterday_rsi}, Today's RSI: {today_rsi}")
        
        if today_rsi > yesterday_rsi:
            # If today's RSI is greater than yesterday's, allocate 100% to TQQQ
            log("RSI is increasing, allocating 100% to TQQQ")
            allocation = 1.0
        else:
            # If today's RSI is not greater, allocate 0% to TQQQ
            log("RSI is not increasing, allocating 0% to TQQQ")
            allocation = 0.0
            
        return TargetAllocation({"TQQQ": allocation})