import pandas as pd
import pandas_ta as ta

def calculate_indicators(df_5m):
    # 5分足指標
    df_5m['rsi_5m'] = ta.rsi(df_5m['close'], length=14)
    macd = ta.macd(df_5m['close'], fast=12, slow=26, signal=9)
    df_5m['macd_hist_5m'] = macd['MACDh_12_26_9']
    
    # 1時間足リサンプリング (未来参照を避けるため、後ほどループ内で計算or処理が必要)
    # 本実装では計算効率のため事前に計算し、1H足の確定タイミングを5M足にマップする
    df_1h = df_5m['close'].resample('1H').last().ffill()
    rsi_1h = ta.rsi(df_1h, length=14)
    
    # 5分足側に1時間足RSIをマッピング
    df_5m['rsi_1h'] = rsi_1h.reindex(df_5m.index, method='ffill')
    df_5m['rsi_1h_prev'] = df_5m['rsi_1h'].shift(12) # 1時間前(5m*12)との比較用
    
    return df_5m