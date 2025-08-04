import time
import pandas as pd
from sklearn.linear_model import LogisticRegression
import numpy as np


# BOT B: Fast, simple momentum trading

#This guy reacts quickly to price movements by comparing each tick to the previous one
#she buys if price goes up, sells if it goes down
#a 1 millisecond delay simulates ultra-low latency (fast decision-making)
def bot_b_simple_momentum(prices):
    position = 0      #Current position: 1 = long (thinks it will increase), -1 = short (thinks it will decrease), 0 = flat
    cash = 0          #Total cash PnL (Profit and Loss)

    for i in range(1, len(prices)):
        #no latency here

        if prices[i] > prices[i - 1]:
            # Price rising — buy 1 unit
            cash -= prices[i]
            position += 1
        elif prices[i] < prices[i - 1]:
            # Price falling — sell 1 unit
            cash += prices[i]
            position -= 1
        # If price unchanged, do nothing

    #Exit any remaining position at the final price
    cash += position * prices[-1]

    return cash

def bot_a_smart_ml(prices, window_size=10, train_ratio=0.7, latency_ticks=100):
    position = 0  #Track the number of units currently held
    cash = 0  #Total profit/loss from trades
    trades = []  #List to store trade details for analysis

    #Build features (sliding windows of past prices) and labels (future direction)
    X = []  #Features: window of past prices
    y = []  #Labels: 1 if price goes up next, 0 if it goes down

    for i in range(window_size, len(prices) - 1):
        window = prices[i - window_size:i]  #Get the last `window_size` prices
        direction = 1 if prices[i + 1] > prices[i] else 0  #Predict up or down
        X.append(window)
        y.append(direction)

    X = np.array(X)
    y = np.array(y)

    #Split into training and testing datasets
    split_idx = int(len(X) * train_ratio)  #index where training ends and testing begins
    X_train, y_train = X[:split_idx], y[:split_idx]  #Training data
    X_test, y_test = X[split_idx:], y[split_idx:]  #Testing data
    test_start = split_idx + window_size  #Map test data back to original price index

    #Train logistic regression model on historical price windows
    model = LogisticRegression(max_iter=500)
    model.fit(X_train, y_train)

    #Simulate trading with latency
    i = 0  #Index into the test set
    while i < len(X_test) - latency_ticks:
        prediction = model.predict([X_test[i]])[0]  #Predict next move (1 = up, 0 = down)

        delayed_index = test_start + i + latency_ticks  #Index where trade is actually executed
        exec_price = prices[delayed_index]  #Price at execution time

        if prediction == 1:
            cash -= exec_price  #Buy one unit
            position += 1
        else:
            cash += exec_price  #Sell one unit
            position -= 1

        #Log trade details for analysis
        trades.append({
            'timestamp_index': delayed_index,
            'predicted_direction': prediction,
            'predict_price': prices[test_start + i],
            'exec_price': exec_price,
            'position': position,
        })

        i += 1  #Move to next example

    #Exit remaining position at most recent price
    if test_start + i < len(prices):
        final_price = prices[test_start + i]
        cash += position * final_price  #Close any open long/short positions

    return cash, trades  #Return final PnL and trade log



#test the bot on  data files

if __name__ == "__main__":
    #Load synthetic price data
    df = pd.read_csv("../data/synthetic_ticks.csv")
    prices = df['price'].values

    #Run Bot B on the data
    result = bot_b_simple_momentum(prices)

    #Show final cash result
    print(f"Bot B (Fast Simple Momentum) final cash: {result:.2f}")

    #Run Bot A on the same data and show result 
    result_a = bot_a_smart_ml(prices, latency_ticks=100)
    print(f"Bot A (Realistic ML) final cash: {result_a[0]:.2f}")



