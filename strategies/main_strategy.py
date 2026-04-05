from config import Config  # この行を追加

class MainStrategy:
    def __init__(self, position):
        self.pos = position
        self.hit_thresholds = set()
        self.state = "NORMAL" # NORMAL, REACHED_75, REACHED_70_UP
        
    def check(self, row):
        # row: 現在の5分足データ (rsi_1h, rsi_1h_prev, rsi_5m, macd_hist_5m, close)
        
        # --- 買いロジック ---
        for lv in Config.MAIN_BUY_LEVELS:
            thr = lv['rsi']
            # 交差判定 (1時間RSIが閾値を下から上へ)
            if row['rsi_1h_prev'] < thr <= row['rsi_1h']:
                if thr not in self.hit_thresholds:
                    if row['rsi_5m'] <= 40 and row['macd_hist_5m'] > 0:
                        amount = Config.ALLOC_X * lv['ratio']
                        if self.pos.buy(row['close'], amount, row.name, f"1H_RSI_{thr}_CrossUp"):
                            self.hit_thresholds.add(thr)

        # --- 売りロジック ---
        # 損切り判定
        if self.pos.shares > 0:
            # 価格損切り
            if (row['close'] / self.pos.avg_price - 1) <= Config.MAIN_STOP_LOSS:
                self.pos.sell(row['close'], 1.0, row.name, "STOP_LOSS_PRICE")
                self.reset_state()
            # 時間損切り
            elif (row.name - self.pos.entry_date).days >= Config.MAIN_TIME_EXIT_DAYS:
                self.pos.sell(row['close'], 1.0, row.name, "STOP_LOSS_TIME")
                self.reset_state()

        # 段階利確・状態遷移
        if self.pos.shares > 0:
            # 5分足条件チェック
            micro_sell = row['rsi_5m'] >= 60 and row['macd_hist_5m'] < 0
            
            # 通常利確
            if micro_sell:
                if row['rsi_1h'] >= 75:
                    self.state = "REACHED_75"
                    self.pos.sell(row['close'], 0.40, row.name, "RSI_75_PARTIAL")
                elif row['rsi_1h'] >= 70:
                    self.state = "REACHED_70_UP"
                    self.pos.sell(row['close'], 0.20, row.name, "RSI_70_PARTIAL")
                elif row['rsi_1h'] >= 65:
                    self.pos.sell(row['close'], 0.15, row.name, "RSI_65_PARTIAL")

            # 分岐パターン
            if self.state == "REACHED_75":
                if row['rsi_1h'] >= 80:
                    self.pos.sell(row['close'], 1.0, row.name, "PATTERN2_ALL_SELL")
                    self.reset_state()
                elif row['rsi_1h'] <= 75:
                    self.pos.sell(row['close'], 0.30, row.name, "PATTERN1_FALL_75")
                    if row['rsi_1h'] <= 70:
                        self.pos.sell(row['close'], 1.0, row.name, "PATTERN1_FALL_70")
                        self.reset_state()

    def reset_state(self):
        self.hit_thresholds.clear()
        self.state = "NORMAL"
        
class MainStrategy:
    def __init__(self, position):
        self.pos = position
        self.hit_thresholds = set()
        self.state = "NORMAL" # NORMAL, REACHED_75, REACHED_70_UP
        
    def check(self, row):
        # row: 現在の5分足データ (rsi_1h, rsi_1h_prev, rsi_5m, macd_hist_5m, close)
        # TODO: MACDヒストグラムの方向性定義（正の値なら買い方向とする）
        
        # --- 買いロジック ---
        for lv in Config.MAIN_BUY_LEVELS:
            thr = lv['rsi']
            # 交差判定 (1時間RSIが閾値を下から上へ)
            if row['rsi_1h_prev'] < thr <= row['rsi_1h']:
                if thr not in self.hit_thresholds:
                    if row['rsi_5m'] <= 40 and row['macd_hist_5m'] > 0:
                        amount = Config.ALLOC_X * lv['ratio']
                        if self.pos.buy(row['close'], amount, row.name, f"1H_RSI_{thr}_CrossUp"):
                            self.hit_thresholds.add(thr)

        # --- 売りロジック ---
        # 損切り判定
        if self.pos.shares > 0:
            # 価格損切り
            if (row['close'] / self.pos.avg_price - 1) <= Config.MAIN_STOP_LOSS:
                self.pos.sell(row['close'], 1.0, row.name, "STOP_LOSS_PRICE")
                self.reset_state()
            # 時間損切り (TODO: 営業日定義)
            elif (row.name - self.pos.entry_date).days >= Config.MAIN_TIME_EXIT_DAYS:
                self.pos.sell(row['close'], 1.0, row.name, "STOP_LOSS_TIME")
                self.reset_state()

        # 段階利確・状態遷移
        if self.pos.shares > 0:
            # 5分足条件チェック
            micro_sell = row['rsi_5m'] >= 60 and row['macd_hist_5m'] < 0
            
            # 通常利確
            if micro_sell:
                if row['rsi_1h'] >= 75:
                    self.state = "REACHED_75"
                    self.pos.sell(row['close'], 0.40, row.name, "RSI_75_PARTIAL")
                elif row['rsi_1h'] >= 70:
                    self.state = "REACHED_70_UP"
                    self.pos.sell(row['close'], 0.20, row.name, "RSI_70_PARTIAL")
                elif row['rsi_1h'] >= 65:
                    self.pos.sell(row['close'], 0.15, row.name, "RSI_65_PARTIAL")

            # 分岐パターン
            if self.state == "REACHED_75":
                if row['rsi_1h'] >= 80:
                    self.pos.sell(row['close'], 1.0, row.name, "PATTERN2_ALL_SELL")
                    self.reset_state()
                elif row['rsi_1h'] <= 75:
                    self.pos.sell(row['close'], 0.30, row.name, "PATTERN1_FALL_75")
                    if row['rsi_1h'] <= 70:
                        self.pos.sell(row['close'], 1.0, row.name, "PATTERN1_FALL_70")
                        self.reset_state()

    def reset_state(self):
        self.hit_thresholds.clear()
        self.state = "NORMAL"