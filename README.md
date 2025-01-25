# Token Economy Simulation Suite

## Overview
This repository contains four distinct but interrelated simulation systems for analyzing token economy dynamics. Each system addresses different aspects of crypto-economic mechanisms through agent-based modeling and discrete event simulation.

---

## 1. Affiliate Network Simulation (`affiliate/`)
**Core Mechanism:** Dynamic bonding curves with referral incentives

### Key Features:
- Multi-token system with 5 simultaneous bonding curves
- Whale agent detection and behavior modeling
- Adaptive commission rates (0-20% range)
- Moving average price stabilization
- Transaction fee/burn rate mechanisms

```python
# Custom bonding curve configuration example
from affiliate.bonding_curves import exponential_bonding_curve
token = Token("VIP", 10000, 1.0, 
    lambda s: exponential_bonding_curve(s, a=1.2, k=0.0007))
```

### Execution:
```bash
cd affiliate
python main.py --num_simulation_steps 500 --num_affiliates 10
```

---

## 2. Airdrop Strategy Engine (`airdrop/`)
**Core Mechanism:** Multi-parameter airdrop optimization

### Strategy Matrix:
| Parameter        | Options                              | Optimization Goal          |
|-------------------|--------------------------------------|----------------------------|
| Vesting Type      | Dynamic Price, Activity, Linear      | Price Stability            |
| Distribution      | Uniform, Tiered, Lottery             | Long-term Holder Retention |
| Criteria          | Holdings, Activity, Random           | Network Growth             |
| Vesting Periods   | 1-24 months                          | Token Velocity Reduction   |


### Execution:
```bash
cd airdrop
python main.py --strategy_type tiered --vesting dynamic_price
```

---

## 3. Bonding Curve Laboratory (`bonding-curve/`)
**Core Mechanism:** Evolutionary parameter optimization

### Curve Types:
1. **Linear:** `price = m*supply + b`
2. **Exponential:** `price = a*e^(k*supply)`
3. **Sigmoid:** `price = K/(1 + e^(-k(supply-S0)))`
4. **Multi-segment:** Hybrid linear-exponential

```python
# Parameter optimization example
optimal_params = optimize_bonding_curve('sigmoid', 
    param_ranges={
        'k': (0.01, 0.05),
        's0': (800, 1200),
        'k_max': (5, 15)
    })
```

### Execution:
```bash
cd bonding-curve
python main.py --curve_type sigmoid --optimize_params
```

---

## 4. Market Coordination Protocol (`mcp/`)
**Core Mechanism:** Resource-based market equilibrium

### Economic Mechanisms:
- Elastic resource pricing: `price = base * (1 + utilization^elasticity)`
- Progressive taxation system (0-5% adjustable)
- Bankruptcy detection (3σ balance threshold)
- Gini coefficient monitoring
- Resource capacity regeneration


### Execution:
```bash
cd mcp
python main.py --tax_rate 0.03 --price_elasticity 0.08
```

---

## Unified Installation
```bash
# Create virtual environment
python -m venv econ-sim
source econ-sim/bin/activate

# Install core dependencies
pip install numpy>=1.21 pandas>=1.3 scipy>=1.7 matplotlib>=3.4

# Install subsystem-specific requirements
pip install -r affiliate/requirements.txt
pip install -r airdrop/requirements.txt 
pip install -r bonding-curve/requirements.txt
pip install -r mcp/requirements.txt
```

---

## Cross-System Analysis
```python
# Compare simulation outputs
def analyze_results(affiliate_data, airdrop_data, bonding_data, mcp_data):
    fig, axs = plt.subplots(2, 2, figsize=(15,10))
    
    # Plot affiliate commission rates
    axs[0,0].plot(affiliate_data['commission_rates'])
    axs[0,0].set_title('Affiliate Commission Dynamics')
    
    # Plot airdrop price trajectories
    for strategy in airdrop_data:
        axs[0,1].plot(strategy['price_history'], label=strategy['name'])
    axs[0,1].set_title('Airdrop Price Performance')
    
    # Plot bonding curve parameter space
    plot_3d_surface(bonding_data, ax=axs[1,0])
    
    # Plot MCP wealth distribution
    plot_gini(mcp_data, ax=axs[1,1])
```