import pandas as pd
from portfolio import Position
from strategies.main_strategy import MainStrategy
from strategies.sub_strategy import SubStrategy
from config import Config

class BacktestEngine:
    def __init__(self, df):
        self.df = df
        self.pos_main = Position(Config.ALLOC_X)
        self.pos_sub = Position(Config.ALLOC_Y)
        self.strat_main = MainStrategy(self.pos_main)
        self.strat_sub = SubStrategy(self.pos_sub)
        self.results = []

    def run(self):
        for index, row in self.df.iterrows():
            # 各戦略の判定実行
            self.strat_main.check(row)
            self.strat_sub.check(row)
            
            # 時系列の資産状況を記録
            total_equity = (self.pos_main.cash + self.pos_main.shares * row['close'] +
                            self.pos_sub.cash + self.pos_sub.shares * row['close'])
            self.results.append({
                "date": index,
                "total_equity": total_equity,
                "main_equity": self.pos_main.cash + self.pos_main.shares * row['close'],
                "sub_equity": self.pos_sub.cash + self.pos_sub.shares * row['close'],
                "close": row['close']
            })
        return pd.DataFrame(self.results).set_index("date")