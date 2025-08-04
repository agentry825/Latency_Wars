# Latency Wars: Modeling the Effects of Execution Delay on Trading Strategies

This project investigates the performance tradeoffs between high-frequency, rule-based trading strategies and predictive, machine learning-based approaches in the presence of execution latency. It simulates a synthetic trading environment and evaluates how the delay between signal generation and trade execution impacts profitability, decision quality, and consistency.

## Objective

The primary objective is to simulate and contrast two fundamentally different algorithmic trading strategies:

- **Reactive Momentum Trading (Bot B)**: A latency-free strategy that immediately responds to short-term price movements.
- **Predictive Machine Learning Trading (Bot A)**: A model-based strategy that predicts future price direction using historical data, but is subjected to configurable execution latency.

This framework provides a reproducible environment for analysing the latency-sensitivity of intelligent trading systems compared to simpler, speed-focused approaches.

## Strategy Descriptions

### Bot A: Predictive Model with Latency

- Implements a binary classification model (logistic regression) trained on sliding windows of historical price data.
- At each decision point, it forecasts whether the next price movement will be upward or downward.
- Each predicted trade is executed with a configurable delay (`latency_ticks`), emulating realistic conditions in which market conditions may change between signal and execution.
- Final cash position and a log of all executed trades are recorded for post-trade analysis.

### Bot B: Simple Momentum Logic

- Observes immediate price changes and reacts without delay:
  - Buys if the current price exceeds the previous price.
  - Sells if the current price is lower.
- This agent does not predict, it only reacts.
- Used as a latency-free baseline to assess the value and vulnerability of predictive intelligence in the presence of delay.

## Evaluation Framework

The project includes an evaluation module that:

- Runs both bots on a shared synthetic dataset of tick-level prices.
- Applies Bot A across multiple latency levels, ranging from negligible (1 tick) to extreme (1000 ticks).
- Collects key performance metrics:
  - Total profit/loss
  - Number of trades
  - Average profit per trade
  - Win rate (proportion of profitable trades)
- Outputs a performance curve showing degradation or improvement as a function of latency.

Trade logs are also exported at selected latencies to allow fine-grained inspection of decision dynamics under delay.

## Data

The simulation operates on synthetic financial tick data. Each tick represents a discrete market price sampled at a consistent interval. The data is stored in a flat CSV file containing a single column labeled `price`. This format ensures compatibility with the training logic and simplifies the integration of alternative data sources.

## Code Structure

```text
Latency_Wars/
├── data/
│   └── synthetic_ticks.csv         # Time-series price data for simulation
├── src/
│   ├── trading_bots.py             # Definitions of Bot A and Bot B
│   └── evaluate.py                 # Evaluation and comparison of strategies
├── interface.py                    # Callable module for external frontends
├── bot_a_trades_latency_100.csv   # Example output (trade log at 100-tick latency)
└── README.md                       # Project overview and documentation
```text

## Applications

This simulation framework may be used in:

- Academic coursework on algorithmic trading, reinforcement learning, or financial modeling.
- Research exploring the interaction of model accuracy and market latency.
- Benchmarking latency-optimised infrastructure or decision engines.
- Comparative studies of model-based vs. rule-based algorithmic agents under real-world constraints.
