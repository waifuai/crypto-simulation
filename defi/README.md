# DeFi and Capital Allocation Simulation

*Token Economy Simulation Suite - DeFi Subsystem*

## Overview

This subsystem simulates decentralized finance (DeFi) protocols and agent capital allocation strategies. Agents participate in staking pools, automated market makers (AMMs), lending protocols, and arbitrage opportunities, creating a dynamic ecosystem of capital flows and yield optimization.

## Key Features

* **Staking Pools**: Token holders can stake assets to earn rewards and secure networks
* **AMM Liquidity Pools**: Constant product formula-based trading with impermanent loss modeling
* **Lending Protocol**: Collateralized lending and borrowing with liquidation mechanics
* **Agent Archetypes**: Yield farmers, arbitrageurs, and leveraged traders with distinct behaviors
* **Capital Allocation**: Multi-protocol yield optimization and risk assessment
* **Systemic Analysis**: TVL tracking, impermanent loss calculations, and protocol health metrics

## What the Code Does

The `main.py` script simulates DeFi interactions over time:

1. **Initialization**: Creates agents with different archetypes and initializes protocols
2. **Agent Actions**: Each time step, agents execute archetype-specific strategies
3. **Protocol Updates**: Staking rewards, AMM trades, lending activity, and arbitrage opportunities
4. **Metrics Collection**: Tracks TVL, agent performance, and protocol statistics
5. **Analysis**: Compares performance across agent types and protocol designs

## Agent Archetypes

### Yield Farmer
- **Behavior**: Optimizes capital allocation across staking and liquidity pools
- **Decision Making**: Calculates APR-effective considering fees and IL risk
- **Strategy**: Allocates to highest-yield opportunities meeting risk criteria

### Arbitrageur
- **Behavior**: Exploits price inefficiencies between AMM and external markets
- **Decision Making**: Detects profitable arbitrage with gas cost consideration
- **Strategy**: Executes triangular arbitrage and cross-protocol arbitrage

### Leveraged Trader
- **Behavior**: Uses collateral to borrow for amplified trading positions
- **Decision Making**: Optimizes leverage ratio based on volatility and liquidation risk
- **Strategy**: Balances return potential against margin call probability

## Protocol Models

### Staking Pools
```python
pool = StakingPool(pool_id=0, total_supply=100000)
pool.stake(agent, amount=1000)  # Stake tokens
rewards = list(pool.distribute_rewards())  # Daily reward distribution
```

### AMM Liquidity Pools
```python
pool = LiquidityPool(0, 0, 1, 1000, 1000)  # Token pair 0-1
pool.add_liquidity(agent, amount_a=100, amount_b=100)
output = pool.swap(asset=0, amount=50)  # Trade execution
```

### Lending Protocol
```python
lending = LendingProtocol()
lending.deposit_collateral(agent, asset_id=0, amount=1000)
lending.borrow_against_collateral(agent, collateral_value=1000, borrow_amount=600)
liquidations = lending.check_liquidations(agents, current_prices)
```

## Mathematical Foundation

See `docs/1-math.md` for the comprehensive mathematical formulation including:

- Agent decision models with unified probability framework
- Staking reward distribution formulas
- AMM constant product mechanics
- Impermanent loss calculations
- Lending protocol collateral dynamics

## Key Metrics

| Metric | Definition | Purpose |
|--------|------------|---------|
| TVL | Total Value Locked Across Protocols | Adoption measurement |
| Total IL | Aggregate Impermanent Loss | LP profitability assessment |
| Portfolio Volatility | Standard deviation of agent wealth | Risk analysis |
| Active Agents | Non-bankrupt agents | System health indicator |
| Protocol Utilization | Resource usage across protocols | Efficiency measurement |

## Integration Points

### With Governance (`../governance-dao/`)
- Treasury funds allocated to DeFi protocols based on DAO votes
- Proposal system can modify DeFi parameters (APR rates, fees)
- Governance tokens can be staked or locked for voting power

### With Affiliate (`../affiliate/`)
- Commission earnings automatically deployed to DeFi strategies
- Whale agents receive preferential DeFi opportunities
- Transaction fees used for liquidity mining programs

### With Bonding Curve (`../bonding-curve/`)
- Dual price discovery between bonding curves and AMM pools
- Arbitrage opportunities between protocol types
- Bonding curve purchases used to bootstrap AMM liquidity

### With Airdrop (`../airdrop/`)
- Vested tokens automatically placed into optimized strategies
- Airdrop participants categorized and routed to appropriate protocols
- Time-locked tokens used for staking and governance participation

## Configuration Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `NUM_AGENTS` | 100 | Total number of simulation agents |
| `NUM_POOLS` | 5 | Number of AMM liquidity pools |
| `NUM_STAKING_POOLS` | 3 | Number of staking pools |
| `STAKING_REWARD_RATE` | 0.05 | Annual staking reward rate |
| `LIQUIDITY_FEE` | 0.003 | AMM trading fee (0.3%) |
| `COLLATERAL_RATIO_MIN` | 1.5 | Minimum collateral ratio |
| `INITIAL_BASE_CURRENCY` | 1000 | Starting agent balance |
| `INITIAL_TOKEN_HOLDINGS` | 100 | Starting token holdings per asset |

## Usage

### Basic Simulation
```bash
cd defi/notebook
python main.py
```

### Parameter Experimentation
```python
from defi.main import run_simulation

# Test different staking reward rates
results = run_simulation({
    'staking_reward_rate': 0.08,  # 8% vs default 5%
    'simulation_steps': 2000
})

print(f"Final TVL: {results['final_tvl']}")
```

### Cross-System Integration
```python
# Load results from other subsystems
from defi.integration import load_governance_tokens, load_affiliate_earnings

agents, protocols = initialize_simulation()
load_governance_tokens(agents)  # Apply governance bonuses
load_affiliate_earnings(agents)  # Boost affiliate earnings

# Run simulation with integrated data
results = run_simulation()
```

## Output Analysis

The simulation generates comprehensive performance metrics:

### Agent Performance by Archetype
- **Yield Farmers**: Average portfolio growth and strategy success rates
- **Arbitrageurs**: Profitability per trade and detection accuracy
- **Leveraged Traders**: Return on equity and liquidation frequency

### Protocol Metrics
- **Staking Pools**: Total staked value and reward distribution efficiency
- **AMM Pools**: Trading volume, slippage analysis, and LP profitability
- **Lending Protocol**: Utilization rates, liquidation events, and interest accrual

### System Health
- **TVL Growth**: Total capital deployment across protocols
- **Impermanent Loss**: Aggregate value loss for liquidity providers
- **Active Participants**: Number of agents maintaining solvency

## Potential Extensions

### Advanced Agent Behaviors
- **Flash Loan Arbitrage**: Atomic arbitrage using flash loans
- **Smart Contract Vulnerabilities**: Modeling exploitation strategies
- **Intertemporal Optimization**: Long-term yield farming strategies

### Protocol Developments
- **Yield Aggregators**: Multi-protocol yield optimization
- **Options Markets**: Derivative trading on underlying assets
- **Insurance Protocols**: Risk hedging and loss protection

### Systemic Enhancements
- **Network Effects**: Protocol popularity influencing user adoption
- **Governance Mechanisms**: On-chain parameter adjustments
- **Cross-Chain Functionality**: Multi-chain arbitrage opportunities

## Performance Considerations

- **Scalability**: Current implementation supports 100+ agents efficiently
- **Parallelization**: Protocol operations can be distributed across threads
- **Memory Usage**: Agent state tracking optimized for long simulations
- **Numerical Stability**: Price calculations use clipping to prevent extreme values

## Validation Approach

Each DeFi mechanism undergoes validation against:

- **Mathematical Correctness**: Formula verification against established DeFi literature
- **Behavioral Plausibility**: Agent strategies tested against observed market patterns
- **Empirical Correspondence**: Where possible, simulation outputs compared to real DeFi data
- **Integration Consistency**: Cross-system interactions maintain economic realism

## License

This subsystem is part of the Token Economy Simulation Suite, licensed under MIT-0.

## See Also

- **Mathematical Foundation**: `docs/1-math.md` - Detailed mathematical formulation
- **Output Data**: Results are suitable for integration with higher-level analysis scripts
- **Cross-System Analysis**: See main suite README for integrated simulation workflows

This DeFi subsystem transforms token economies from static holding mechanisms to dynamic capital allocation systems, enabling advanced analysis of decentralized finance interaction patterns and economic behaviors.