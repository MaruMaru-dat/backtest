import numpy as np

class Config:
    SYMBOL = "QQQ"
    PERIOD_YEARS = 5
    INITIAL_CASH = 1000.0
    ALLOC_X = 700.0  # Main
    ALLOC_Y = 300.0  # Sub
    
    RSI_PERIOD = 14
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    
    # Main Trading Config
    MAIN_BUY_LEVELS = [
        {"rsi": 30, "ratio": 0.15},
        {"rsi": 25, "ratio": 0.15},
        {"rsi": 20, "ratio": 0.25},
        {"rsi": 15, "ratio": 0.25},
        {"rsi": 10, "ratio": 0.20},
    ]
    MAIN_SELL_LEVELS = [
        {"rsi": 65, "sell_ratio": 0.15},
        {"rsi": 70, "sell_ratio": 0.20},
        {"rsi": 75, "sell_ratio": 0.40},
    ]
    MAIN_STOP_LOSS = -0.15
    MAIN_TIME_EXIT_DAYS = 7

    # Sub Trading Config
    SUB_BUY_LEVELS = [
        {"rsi": 40, "ratio": 0.10},
        {"rsi": 37, "ratio": 0.20},
        {"rsi": 35, "ratio": 0.30},
        {"rsi": 33, "ratio": 0.40},
    ]
    SUB_SELL_LEVELS = [
        {"rsi": 58, "sell_ratio": 0.15},
        {"rsi": 60, "sell_ratio": 0.20},
        {"rsi": 63, "sell_ratio": 0.40},
    ]