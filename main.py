import yfinance as yf
from config import Config
from indicators import calculate_indicators
from engine import BacktestEngine
from utils.report import generate_report

def main():
    # データ取得 (TODO: 5分足の5年間データ取得元。yfinanceは1ヶ月制限あり)
    print("データ取得中...")
    df = yf.download(Config.SYMBOL, period="1mo", interval="5m") # テスト用
    
    # 指標計算
    df = calculate_indicators(df)
    df = df.dropna()
    
    # バックテスト実行
    engine = BacktestEngine(df)
    results = engine.run()
    
    # レポート表示
    generate_report(results, Config.INITIAL_CASH)
    
    # 履歴保存
    # results.to_csv("backtest_results.csv")

if __name__ == "__main__":
    main()