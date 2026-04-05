from config import Config

class SubStrategy:
    def __init__(self, position):
        self.pos = position
        self.hit_thresholds = set()
        self.state = "NORMAL" # NORMAL, REACHED_63, REACHED_60_UP

    def check(self, row):
        # --- 買いロジック ---
        for lv in Config.SUB_BUY_LEVELS:
            thr = lv['rsi']
            if row['rsi_1h_prev'] < thr <= row['rsi_1h']:
                if thr not in self.hit_thresholds:
                    if row['rsi_5m'] <= 40 and row['macd_hist_5m'] > 0:
                        amount = Config.ALLOC_Y * lv['ratio']
                        if self.pos.buy(row['close'], amount, row.name, f"SUB_1H_RSI_{thr}_CrossUp"):
                            self.hit_thresholds.add(thr)

        # --- 売りロジック ---
        if self.pos.shares > 0:
            micro_sell = row['rsi_5m'] >= 60 and row['macd_hist_5m'] < 0
            
            # 通常利確
            if micro_sell:
                if row['rsi_1h'] >= 63:
                    self.state = "REACHED_63"
                    self.pos.sell(row['close'], 0.40, row.name, "SUB_RSI_63_PARTIAL")
                elif row['rsi_1h'] >= 60:
                    self.state = "REACHED_60_UP"
                    self.pos.sell(row['close'], 0.20, row.name, "SUB_RSI_60_PARTIAL")
                elif row['rsi_1h'] >= 58:
                    self.pos.sell(row['close'], 0.15, row.name, "SUB_RSI_58_PARTIAL")

            # 分岐パターン
            if self.state in ["REACHED_63", "REACHED_60_UP"]:
                if row['rsi_1h'] >= 65:
                    self.pos.sell(row['close'], 1.0, row.name, "SUB_PATTERN2_ALL_SELL")
                    self.reset_state()
                elif self.state == "REACHED_63" and row['rsi_1h'] <= 60:
                    self.pos.sell(row['close'], 0.30, row.name, "SUB_PATTERN1_FALL_60")
                    self.state = "FALLING"
                elif self.state == "FALLING" and row['rsi_1h'] <= 58:
                    self.pos.sell(row['close'], 1.0, row.name, "SUB_PATTERN1_FALL_58")
                    self.reset_state()

    def reset_state(self):
        self.hit_thresholds.clear()
        self.state = "NORMAL"