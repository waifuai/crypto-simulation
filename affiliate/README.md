# Token Economy Simulation with Bonding Curves and Affiliate Dynamics

## Overview

This project simulates a dynamic token economy with multiple cryptocurrencies, bonding curve mechanisms, and affiliate marketing dynamics. It demonstrates how token prices evolve based on supply/demand through different bonding curves, while affiliates earn commissions and adapt their strategies in real-time.

## Key Features

- **5 Bonding Curve Types**
  - Linear, Exponential, Sigmoid, Root, and Inverse curves
  - Automatic curve switching and parameter randomization
- **Dynamic Affiliate System**
  - Adaptive commission rates (0-20% range)
  - Whale affiliates with large investment capacity
  - Portfolio tracking and automated trading strategies
- **Economic Mechanics**
  - Transaction fees (0.25%) and token burns (0.02%)
  - Supply-dependent price calculations
  - Configurable simulation parameters
- **Simulation Analytics**
  - Step-by-step price/supply tracking
  - Affiliate earnings history
  - Comprehensive end-of-run summary reports

## Installation

1. **Requirements**
   - Python 3.8+
   - NumPy

2. **Setup**
   ```bash
   pip install numpy
   ```

## Usage

Run the simulation with default parameters:
```bash
python main.py
```

Customize the simulation:
```bash
python main.py \
  --num_simulation_steps 500 \
  --num_tokens 8 \
  --num_affiliates 10 \
  --initial_price 2.0 \
  --initial_commission_rate 0.15
```

## Configuration Options

### Command Line Arguments
| Parameter | Description | Default |
|-----------|-------------|---------|
| `--num_simulation_steps` | Total steps to simulate | 100 |
| `--num_tokens` | Number of distinct tokens | 5 |
| `--num_affiliates` | Number of affiliates | 5 |
| `--initial_price` | Starting price for all tokens | 1.0 |
| `--initial_commission_rate` | Base affiliate commission rate | 0.10 |

### Key Constants (constants.py)
```python
INITIAL_SUPPLY = 10000        # Starting token supply
TRANSACTION_FEE_RATE = 0.0025 # 0.25% per trade
BURN_RATE = 0.0002            # 0.02% token burn
COMMISSION_DYNAMICS_STEP = 10 # Commission adjustment interval
WHALE_INVESTMENT_RANGE = (5000, 10000) # Whale capacity bounds
```

## Simulation Mechanics

### Token Dynamics
1. **Price Calculation**
   ```python
   # Example exponential curve
   price = a * e^(k * supply)
   ```
2. **Supply Changes**
   - Buys increase supply, sells decrease supply
   - Automatic fee deduction and token burns

3. **Bonding Curve Evolution**
   - Random curve selection every 500-1000 steps
   - Parameter adjustments every 20 steps

### Affiliate Behavior
1. **Commission Adjustments**
   - Rates adjusted every 10 steps based on:
   ```python
   avg_investment > 50 ? rate += 0.0005 : rate -= 0.0005
   ```
2. **Trading Strategies**
   - Regular affiliates: 1-2 trades/step
   - Whale affiliates: Large bulk trades (5,000-10,000 base currency)
   - Automatic portfolio rebalancing (5% sell probability/step)

3. **Wallet Management**
   - Track multiple token balances
   - Base currency accounting
   - Historical earnings tracking

## Output Example

```text
--- Token Summary ---

Token: Token_3
  Final Price: 4.72
  Final Supply: 14256.32
  Final Bonding Curve: exponential_bonding_curve

--- Affiliate Summary ---

Affiliate: 4
  Final Base Currency: 3842.15
  Final Commission Rate: 0.1125
  Total Earned: 642.78
```
