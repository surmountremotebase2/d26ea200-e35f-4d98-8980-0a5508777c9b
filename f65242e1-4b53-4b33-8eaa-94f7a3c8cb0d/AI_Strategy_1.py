from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the ticker of interest
        self.tickers = ["XYZ"]

    @property
    def assets(self):
        # List of assets this strategy will trade
        return self.tickers

    @property
    def interval(self):
        # Data interval for the strategy (daily in this example)
        return "1day"

    def run(self, data):
        # Check the current RSI of the asset
        rsi = RSI("XYZ", data["ohlcv"], 14)  # RSI with a window of 14 days
        
        # Access current holdings for "XYZ"
        current_holdings = data["holdings"].get("XYZ", 0)
        
        # Decision making based on RSI and current holdings
        if rsi[-1] < 30 and current_holdings == 0:
            # RSI < 30 might indicate that the asset is oversold, consider buying
            allocation_dict = {"XYZ": 1}  # Allocating 100% to buying XYZ
            log("Buying XYZ, as its RSI is below 30, indicating potential oversold conditions.")
        elif 30 <= rsi[-1] <= 70:
            # If RSI is between 30 and 70, hold the position
            allocation_dict = {"XYZ": current_holdings}  # No change in allocation
            log("Holding current position in XYZ as its RSI indicates neutral conditions.")
        elif rsi[-1] > 70 and current_holdings > 0:
            # RSI > 70 might indicate that the asset is overbought, consider selling
            allocation_dict = {"XYZ": 0}  # Selling all holdings of XYZ
            log("Selling XYZ, as its RSI is above 70, indicating potential overbought conditions.")
        else:
            # Default case to hold the current position if none of the above conditions meet
            allocation_dict = {"XYZ": current_holdings}
            log("No clear trading signal. Holding current position.")

        return TargetAllocation(allocation_dict)