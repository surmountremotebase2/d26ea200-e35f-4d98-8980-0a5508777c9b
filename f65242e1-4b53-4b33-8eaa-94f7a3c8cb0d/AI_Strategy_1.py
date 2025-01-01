from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    @property
    def assets(self):
        return ["TQQQ"]  # Specifies that our strategy is focused on TQQQ

    @property
    def interval(self):
        return "1day"  # The strategy will operate on daily intervals

    def run(self, data):
        """
        This strategy buys TQQQ if RSI is below 31 and holds it until TQQQ's price is above its 20-day moving average.
        """
        # Default TQQQ stake is 0 (not holding)
        tqqq_stake = 0

        # Calculate the RSI and Moving Average for TQQQ
        rsi = RSI("TQQQ", data["ohlcv"], length=14)  # 14-day RSI
        ma = SMA("TQQQ", data["ohlcv"], length=20)  # 20-day moving average

        # Check for the availability of the calculated indicators
        if rsi and ma and len(data["ohlcv"]) > 20:
            # Check if the latest RSI is below 31 for a buy signal
            if rsi[-1] < 31:
                log("RSI below 31, buying TQQQ")
                tqqq_stake = 1  # Set stake to 1 (100% of the portfolio)
            # Check if the current price of TQQQ is above its 20-day MA, then hold
            current_price = data["ohlcv"][-1]["TQQQ"]["close"]  # Latest closing price of TQQQ
            if current_price > ma[-1]:
                log("TQQQ price is above 20-day MA, holding TQQQ")
                tqqq_stake = 1  # Continue holding if already bought
            else:
                log("TQQQ does not meet any criteria, not holding/buying")
        else:
            log("Not enough data to execute strategy")

        return TargetAllocation({"TQQQ": tqqq_stake})