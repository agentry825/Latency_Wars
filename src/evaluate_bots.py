import pandas as pd
import matplotlib.pyplot as plt
import csv
from tabulate import tabulate
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


def evaluate_bots(prices):
    print("Running Bot B (Fast Dumb Momentum)...")
    pnl_bot_b = bot_b_simple_momentum(prices)
    print(f"Bot B final PnL: {pnl_bot_b:.2f}\n")

    latencies = [1, 5, 10, 20, 50, 100, 150, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    results = []

    table_data = []

    for latency in latencies:
        pnl, trades = bot_a_smart_ml(prices, latency_ticks=latency)
        stats = analyse_trades(trades)

        results.append({'latency': latency, 'pnl': pnl, 'stats': stats})

        # Prepare row for table
        table_data.append([
            latency,
            f"{pnl:.2f}",
            stats['num_trades'],
            f"{stats['avg_profit']:.4f}",
            f"{stats['win_rate']:.2%}"
        ])

        if latency == 100:
            with open('bot_a_trades_latency_100.csv', 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=trades[0].keys())
                writer.writeheader()
                writer.writerows(trades)
            print("Trade log saved to 'bot_a_trades_latency_100.csv'\n")

    # Print nicely formatted table of Bot A results
    headers = ["Latency (ticks)", "PnL", "Number of Trades", "Avg Profit/Trade", "Win Rate"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

    # Plot performance
    plt.figure(figsize=(10, 6))
    plt.plot([r['latency'] for r in results], [r['pnl'] for r in results],
             marker='o', label='Bot A (Smart ML) PnL by Latency')
    plt.axhline(pnl_bot_b, color='r', linestyle='--', label='Bot B (Fast Dumb) PnL')
    plt.xlabel('Latency (ticks)')
    plt.ylabel('Final PnL')
    plt.title('Bot Performance Comparison')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    data_path = "../data/synthetic_ticks.csv"
    print(f"Loading data from {data_path}")

    df = pd.read_csv(data_path)
    prices = df['price'].values

    evaluate_bots(prices)
