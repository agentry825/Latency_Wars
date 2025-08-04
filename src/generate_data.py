import os
import numpy as np
import pandas as pd

# Ensure data folder exists
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
os.makedirs('../data', exist_ok=True)

def generate_synthetic_tick_data(num_ticks=10000, start_price=100):
    np.random.seed(90)  #So random number generation starts at the same number each time, leading to the same sequence
    
    price_changes = np.random.normal(loc=0, scale=0.1, size=num_ticks) 
    #Price changes are based on a normal distribution with small step size
    prices = start_price + np.cumsum(price_changes)
    #the price is the start price plus the cumulative sum of changes
    
    timestamps = pd.date_range(start='2025-08-04 09:30:00', periods=num_ticks, freq='ms')
    #makes the timetsamp to go with the price starting on the day this project started 
    
    df = pd.DataFrame({'timestamp': timestamps, 'price': prices})
    #makes a pandas data frame with the timestamp and corresponding price
    return df

if __name__ == "__main__":
    data = generate_synthetic_tick_data()
    output_path = os.path.join(data_dir, 'synthetic_ticks.csv')
    data.to_csv(output_path, index=False)
    print(f"Synthetic tick data saved to {output_path}")
