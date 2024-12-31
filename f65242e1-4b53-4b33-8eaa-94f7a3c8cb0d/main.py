from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    
    def __init__(self):
        # Define the tickers for SPY, UPRO, and UVXY
        self.spy = "SPY"
        self.upro = "UPRO"
        self.uvxy = "UVXY"
        # RSI threshold values for buying UPRO or UVXY
        self.rsi_low = 30
        self.rsi_high = 80

    @property
    def assets(self):
        return [self.spy, self.upro, self.uvxy]

    @property
    def interval(self):
        # Use a daily interval for RSI calculation
        return "1day"

    def run(self, data):
        # Initialize a dictionary to hold the target allocations
        allocation_dict = {self.spy: 0, self.upro: 0, self.uvxy: 0}

        # Calculate the RSI for SPY
        rsi = RSI(self.spy, data["ohlcv"], 14)  # Using 14 periods for RSI calculation
        
        if len(rsi) > 0:
            current_rsi = rsi[-1]
            log(f"Current RSI for {self.spy}: {current_rsi}")
            
            if current_rsi < self.rsi_low:
                # If RSI is below 30, allocate 100% to UPRO
                allocation_dict[self.upro] = 1
            elif current_rsi > self.rsi_high:
                # If RSI is above 80, allocate 100% to UVXY
                allocation_dict[self.uvxy] = 1
            else:
                # If RSI is between 30 and 80, and not holding UPRO or UVXY, allocate 100% to SPY
                # Check for current holdings if applicable, assumed to have method .holdings() for simplicity
                if data["holdings"].get(self.upro, 0) <= 0 and data["holdings"].get(self.uvxy, 0) <= 0:
                    allocation_dict[self.spy] = 1
                
                # If holding UVXY and RSI drops below 80, sell UVXY (set allocation to 0)
                if current_rsi < self.rsi_high and allocation_dict[self.uvxy] > 0:
                    allocation_dict[self.uvxy] = 0
                
                # It's assumed we can hold only one of the assets at a time based on the strategy.
                # If above conditions don't lead to buying UPRO or UVXY, and if there're no holdings, only then buy SPY.
                if sum(allocation_dict.values()) == 0:
                    allocation_dict[self.spy] = 1

        return TargetAllocation(allocation_dict)