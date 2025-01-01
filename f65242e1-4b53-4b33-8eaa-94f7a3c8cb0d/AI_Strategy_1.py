from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Initialize with the ticker you want to focus on
        self.ticker = "TQQQ" 

    @property
    def assets(self):
        # List of assets the strategy will trade
        return [self.ticker]

    @property
    def interval(self):
        # Time interval at which data is considered, in this case every hour
        return "1hour"

    def run(self, data):
        # Main logic to execute each time the strategy runs

        # Compute RSI for TQQQ
        rsi_values = RSI(self.ticker, data["ohlcv"], length=14) # RSI computed over 14 periods by default
        
        # Checking the latest RSI value, ensuring there is at least one value 
        if rsi_values and len(rsi_values) > 0:
            latest_rsi = rsi_values[-1]
            log(f"Latest RSI for {self.ticker}: {latest_rsi}")

            # Decision making based on RSI
            if latest_rsi < 30:
                # Considered oversold, therefore buy
                return TargetAllocation({self.ticker: 1.0})  # Allocate 100% to TQQQ
            elif latest_rsi > 70:
                # Considered overbought, therefore sell
                return TargetAllocation({self.ticker: 0})  # Do not hold TQQQ
            else:
                # RSI is in neutral zone, no action
                log("RSI in neutral zone. No action taken.")
        else:
            log("RSI data not available.")

        # If no condition is met or RSI data is missing, 
        # this strategy does not hold or reallocate any assets.
        return TargetAllocation({self.ticker: 0})