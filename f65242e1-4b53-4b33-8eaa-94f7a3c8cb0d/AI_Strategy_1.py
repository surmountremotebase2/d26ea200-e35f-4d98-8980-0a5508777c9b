from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    @property
    def assets(self):
        return ["TQQQ"]

    @property
    def interval(self):
        # Using daily intervals for RSI calculation
        return "1day"

    def run(self, data):
        # Initializing allocation with no position
        tqqq_stake = 0
        
        # Calculating the 10-day RSI for TQQQ
        rsi_values = RSI("TQQQ", data["ohlcv"], 10)
        
        if rsi_values is not None and len(rsi_values) > 1:
            # Retrieving the RSI values for today and yesterday
            rsi_today = rsi_values[-1]
            rsi_yesterday = rsi_values[-2]
            
            log(f"RSI Today for TQQQ: {rsi_today}, RSI Yesterday: {rsi_yesterday}")

            # Implement trading logic based on RSI
            # Example: Buy if RSI is below 30 (oversold), Sell if above 70 (overbought), Hold otherwise
            if rsi_today < 30:
                tqqq_stake = 1 # Buy
            elif rsi_today > 70:
                tqqq_stake = 0 # Sell
                
            # For simplicity, no handling of hold strategy (tqqq_stake remains as initialized for hold condition)

        return TargetAllocation({"TQQQ": tqqq_stake})