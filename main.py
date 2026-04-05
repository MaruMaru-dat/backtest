import pandas as pd
import yfinance as yf
from config import Config
from indicators import calculate_indicators
from engine import BacktestEngine
from utils.report import generate_report

def main():
    # データ取得
    print("データ取得中...")
    # ※yfinanceの5分足は過去60日分までの制限があります
    df = yf.download(Config.SYMBOL, period="1mo", interval="5m")
    
    # MultiIndex（二重カラム）の解消
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    # カラム名を小文字に統一 (Close -> close)
    df.columns = df.columns.str.lower()
    
    # 指標計算
    df = calculate_indicators(df)
    df = df.dropna()
    
    # バックテスト実行
    engine = BacktestEngine(df)
    results = engine.run()
    
    # レポート表示
    generate_report(results, Config.INITIAL_CASH)

if __name__ == "__main__":
    main()