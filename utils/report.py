import numpy as np
import pandas as pd

def generate_report(results_df, initial_cash):
    final_equity = results_df['total_equity'].iloc[-1]
    total_return = (final_equity / initial_cash - 1) * 100
    
    # CAGR計算
    days = (results_df.index[-1] - results_df.index[0]).days
    cagr = ((final_equity / initial_cash) ** (365.0 / days) - 1) * 100
    
    # MDD計算
    rolling_max = results_df['total_equity'].cummax()
    drawdown = (results_df['total_equity'] - rolling_max) / rolling_max
    mdd = drawdown.min() * 100
    
    print(f"--- バックテスト結果 ---")
    print(f"総リターン: {total_return:.2f}%")
    print(f"CAGR: {cagr:.2f}%")
    print(f"最大ドローダウン: {mdd:.2f}%")
    # TODO: シャープレシオ、勝率等の詳細統計の実装
    return drawdown