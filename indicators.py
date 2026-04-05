import pandas as pd

def calculate_indicators(df_5m):
    """
    pandasのみを使用してRSIとMACDを計算する。
    pandas-taを完全に排除したコード。
    """
    
    # --- RSIの計算ロジック ---
    def compute_rsi(series, period=14):
        delta = series.diff()
        up = delta.clip(lower=0)
        down = -1 * delta.clip(upper=0)
        # Wilder's Smoothing (指数移動平均)
        ema_up = up.ewm(com=period - 1, adjust=False).mean()
        ema_down = down.ewm(com=period - 1, adjust=False).mean()
        rs = ema_up / ema_down
        return 100 - (100 / (1 + rs))

    # --- MACDの計算ロジック ---
    def compute_macd_hist(series, fast=12, slow=26, signal=9):
        ema_fast = series.ewm(span=fast, adjust=False).mean()
        ema_slow = series.ewm(span=slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        return macd_line - signal_line

    # 5分足の指標算出
    df_5m['rsi_5m'] = compute_rsi(df_5m['close'], period=14)
    df_5m['macd_hist_5m'] = compute_macd_hist(df_5m['close'])
    
    # 1時間足のリサンプリングと指標算出
    df_1h_close = df_5m['close'].resample('1H').last().ffill()
    rsi_1h = compute_rsi(df_1h_close, period=14)
    
    # 5分足側に1時間足RSIをマッピング
    df_5m['rsi_1h'] = rsi_1h.reindex(df_5m.index, method='ffill')
    # 1時間前(5分足12本分)との比較用
    df_5m['rsi_1h_prev'] = df_5m['rsi_1h'].shift(12)
    
    return df_5m