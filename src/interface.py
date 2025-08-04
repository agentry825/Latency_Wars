# interface.py

import pandas as pd
import json
from trading_bots import bot_a_smart_ml, bot_b_simple_momentum

def analyse_trades(trades):
    profits = []
    wins = 0

    for t in trades:
        if t['predicted_direction'] == 1:
            profit = t['exec_price'] - t['predict_price']
        else:
            profit = t['predict_price'] - t['exec_price']
        
        profits.append(profit)
        if profit > 0:
            wins += 1

    total_profit = sum(profits)
    avg_profit = total_profit / len(profits) if profits else 0
    win_rate = wins / len(profits) if profits else 0

    return {
        'total_profit': total_profit,
        'num_trades': len(profits),
        'avg_profit': avg_profit,
        'win_rate': win_rate
    }

def run_evaluation(csv_path: str, latencies: list[int]) -> dict:
    df = pd.read_csv(csv_path)
    prices = df['price'].values

    bot_b_pnl = bot_b_simple_momentum(prices)

    results = []

    for latency in latencies:
        pnl, trades = bot_a_smart_ml(prices, latency_ticks=latency)
        stats = analyse_trades(trades)

        results.append({
            "latency": latency,
            "pnl": pnl,
            "num_trades": stats["num_trades"],
            "avg_profit": stats["avg_profit"],
            "win_rate": stats["win_rate"]
        })

    return {
        "bot_b_pnl": bot_b_pnl,
        "bot_a_results": results
    }
