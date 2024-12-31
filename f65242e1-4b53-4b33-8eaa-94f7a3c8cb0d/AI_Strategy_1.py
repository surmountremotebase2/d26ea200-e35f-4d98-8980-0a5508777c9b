from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        # Define assets of interest
        self.assets_list = ["BIL", "IBTK", "SPY", "SHY", "SOXL", "SOXS", "SQQQ", "TECL"]

    @property
    def interval(self):
        # Define the data interval
        return "1day"

    @property
    def assets(self):
        # Return assets involved in strategy
        return self.assets_list

    def run(self, data):
        # Initialize allocation dictionary
        allocation_dict = dict.fromkeys(self.assets_list, 0)

        # Retrieve RSI indicators
        rsi_bil = RSI("BIL", data, 5)
        rsi_ibtk = RSI("IBTK", data, 7)
        rsi_spy = RSI("SPY", data, 6)

        # Decision logic based on RSI comparisons
        if rsi_bil[-1] < rsi_ibtk[-1]:
            if rsi_spy[-1] > 75:
                # If SPY's RSI is above 75, allocate to SHY
                allocation_dict["SHY"] = 1.0
            else:
                # Otherwise, allocate to SOXL
                allocation_dict["SOXL"] = 1.0
        else:
            # In this branch, we can elaborate similar logic for the SBND and HIBL
            # comparison or any other asset's analysis as per original strategy seed.
            # Such specific allocations are left as placeholders for further expansion.
            pass

        # Ensure allocation does not exceed 100% of the portfolio
        total_allocation = sum(allocation_dict.values())
        if total_allocation > 1.0:
            allocation_dict = {k: v / total_allocation for k, v in allocation_dict.items()}

        return TargetAllocation(allocation_dict)