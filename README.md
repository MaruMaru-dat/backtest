### ディレクトリ
qqq_backtest/
├── main.py              # 実行エントリーポイント
├── config.py            # パラメータ設定
├── indicators.py        # テクニカル指標計算
├── portfolio.py         # 資産・ポジション管理
├── strategies/
│   ├── base.py          # 戦略基底クラス
│   ├── main_strategy.py # Main Tradingロジック
│   └── sub_strategy.py  # Sub Tradingロジック
├── engine.py            # バックテスト本体（5分足ループ）
└── utils/
    ├── report.py        # 結果集計・グラフ出力
    └── logger.py        # 取引ログ出力

### ファイルの機能と役割
ファイル名役割config.py資金、RSI閾値、投入比率、MACD設定、期間等の定数管理indicators.pypandas/numpyを用いたRSI、MACD、リサンプリング処理portfolio.py現金、保有数、平均単価の更新、手数料未考慮の決済処理strategies/*.pyMainおよびSub固有のエントリー・エグジット・状態遷移ロジックengine.py時系列順にデータを読み込み、各戦略にシグナル判定を依頼report.py各統計指標（CAGR, MDD等）の計算とMatplotlibによる可視化