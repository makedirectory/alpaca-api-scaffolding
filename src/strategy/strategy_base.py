class StrategyBase:
    def __init__(self):
        pass
    
    def run_strategy(self):
        # This is a base class for trading strategies. Actual strategy implementations should override this function.
        raise NotImplementedError
