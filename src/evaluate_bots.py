import pandas as pd                      
import matplotlib.pyplot as plt          
import csv                              
from trading_bots import bot_a_smart_ml, bot_b_simple_momentum  
#Import the two trading bot functions from your trading_bots module


def analyse_trades(trades):
    #Analyse the detailed trade logs and calculate stats:
    #- total profit
    #- number of trades
    #- average profit per trade
    #- win rate (percentage of profitable trades)

    profits = []  #List to hold profit from each trade
    wins = 0      #Count of profitable trades
    
    for t in trades:  #Loop through each trade in the log
        #Determine profit based on predicted direction:
        #If predicted to go up (1), profit = exit price - entry price
        #If predicted down (0), profit = entry price - exit price (short profit)
        if t['predicted_direction'] == 1:
            profit = t['exec_price'] - t['predict_price']
        else:
            profit = t['predict_price'] - t['exec_price']
        
        profits.append(profit)  #Add trade profit to list
        
        if profit > 0:         #If trade was profitable increment win count
            wins += 1          

    total_profit = sum(profits)                   #Sum of all trade profits
    avg_profit = total_profit / len(profits) if profits else 0  #Average profit per trade
    win_rate = wins / len(profits) if profits else 0           #Fraction of profitable trades

    #Return calculated stats as a dictionary
    return {
        'total_profit': total_profit,
        'num_trades': len(profits),
        'avg_profit': avg_profit,
        'win_rate': win_rate
    }


def evaluate_bots(prices):
    """
    Run and compare Bot B (fast dumb) and Bot A (smart with latency).
    Print detailed stats and plot performance.
    """
    print("Running Bot B (Fast Dumb Momentum)...")
    pnl_bot_b = bot_b_simple_momentum(prices)  #Run Bot B on the price data
    print(f"Bot B final PnL: {pnl_bot_b:.2f}\n")  #Print Bot B final profit & loss

    latencies = [1, 5, 10, 20, 50, 100, 150, 200, 300, 400, 500, 600, 700, 800, 900, 1000]  #List of latency values to test for Bot A
    results = []     #List to store results for each latency

    for latency in latencies:        #Loop over each latency setting
        print(f"Running Bot A (Smart ML) with latency {latency} ticks...")
        pnl, trades = bot_a_smart_ml(prices, latency_ticks=latency)  
        #Run Bot A with current latency, get final pnl and trade log
        
        stats = analyse_trades(trades)  #Analyse detailed trade stats
        
        #Store latency, pnl, and stats in results for later plotting
        results.append({'latency': latency, 'pnl': pnl, 'stats': stats})

        #Print a summary of results for this latency
        print(f"Latency: {latency} ticks | PnL: {pnl:.2f} | "
              f"Trades: {stats['num_trades']} | Avg profit: {stats['avg_profit']:.4f} | Win rate: {stats['win_rate']:.2%}\n")

        #For latency=100, export the trade log to CSV for inspection
        if latency == 100:
            with open('bot_a_trades_latency_100.csv', 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=trades[0].keys())
                writer.writeheader()
                writer.writerows(trades)
            print("Trade log saved to 'bot_a_trades_latency_100.csv'\n")

    #Plot the final PnL for Bot A vs latency
    plt.figure(figsize=(10, 6))
    plt.plot([r['latency'] for r in results], [r['pnl'] for r in results],
             marker='o', label='Bot A (Smart ML) PnL by Latency')
    #Add horizontal line for Bot B baseline
    plt.axhline(pnl_bot_b, color='r', linestyle='--', label='Bot B (Fast Dumb) PnL')
    
    #Set axis labels and title
    plt.xlabel('Latency (ticks)')
    plt.ylabel('Final PnL')
    plt.title('Bot Performance Comparison')
    plt.legend()  #Show legend for lines
    plt.grid(True)  #Add grid for readability
    plt.show()     #Display the plot


if __name__ == "__main__":
    data_path = "../data/synthetic_ticks.csv"  
    print(f"Loading data from {data_path}")
    
    df = pd.read_csv(data_path)   #Load CSV data into pandas DataFrame
    prices = df['price'].values   #Extract price column as a numpy array
    
    evaluate_bots(prices)         #Run the evaluation function on the price data
