import numpy as np

class RsiIndicator:
    
    def RSI(self, series, period):
        delta = series.diff().dropna()
        ups = delta * 0
        downs = ups.copy()
        ups[delta > 0] = delta[delta > 0]
        downs[delta < 0] = -delta[delta < 0]
        ups[ups.index[period-1]] = np.mean(ups[:period])
        ups = ups.drop(ups.index[:(period-1)])
        downs[downs.index[period-1]] = np.mean(downs[:period])
        downs = downs.drop(downs.index[:(period-1)])
        rs = ups.ewm(com=period-1, adjust=False).mean() / downs.ewm(com=period-1, adjust=False).mean()
        return 100 - 100 / (1 + rs)