# DeFi and Capital Allocation Simulation: Mathematical Formulation

*Token Economy Simulation Suite - DeFi Subsystem Mathematical Foundations*

## Problem Statement

Consider a decentralized finance (DeFi) ecosystem with $N$ autonomous agents engaging in various capital allocation strategies. Agents can participate in staking pools, automated market maker (AMM) liquidity pools, and lending protocols. The system evolves over discrete time steps $t = 0, 1, 2, \dots, T$, with agents optimizing their strategies to maximize returns subject to risk constraints.

The simulation models agent decision-making processes for:
- **Staking**: Locking tokens to earn rewards and secure networks
- **Liquidity Provision**: Pooling assets for AMM trading with fee earnings
- **Lending/Borrowing**: Depositing collateral and borrowing against it
- **Arbitrage**: Exploiting price inefficiencies between protocols
- **Yield Farming**: Optimizing capital allocation across multiple protocols

## Notation

Following the unified mathematical theory framework:

| Symbol | Definition |
|--------|------------|
| $i$ | Agent index ($i \in \{1, \dots, N\}$) |
| $t$ | Time step ($t \in \{0, 1, \dots, T\}$) |
| $\mathcal{A}_i$ | Agent $i$'s archetype (yield_farmer, arbitrageur, leveraged_trader) |
| $B_i(t)$ | Agent $i$'s base currency balance at time $t$ |
| $\mathbf{H}_i(t)$ | Agent $i$'s token holdings vector at time $t$ |
| $APR_r(t)$ | Annual percentage rate for resource $r$ at time $t$ |
| $TVL_p(t)$ | Total value locked in protocol $p$ at time $t$ |
| $IL_{i,p}(t)$ | Impermanent loss for agent $i$ in pool $p$ at time $t$ |

## Agent Archetypes and Decision Models

### 1. Yield Farmer Agent

**Objective Function:**
$$\max_{\theta} \mathbb{E}[U_i(\theta)] = \sum_{p \in \mathcal{P}} w_p \cdot APR_p \cdot (1 - IL_p) - c(\theta)$$

Where:
- $\theta$: Strategy allocation vector
- $\mathcal{P}$: Set of available protocols
- $w_p$: Allocation weight to protocol $p$
- $c(\theta)$: Transaction cost function

**Strategy Optimization:**
For each protocol $p$, calculate effective yields:
$$APR_{\text{effective},i,p} = APR_p \cdot (1 - IL_{i,p} - gas_i)$$

Select top $k$ strategies ordered by $APR_{\text{effective},i,p}$.

### 2. Arbitrageur Agent

**Arbitrage Detection:**
$$\Delta_p = |P_{AMM,p} - P_{\text{external},p}| / P_{\text{external},p}$$

**Profitability Condition:**
$$|P_{AMM,p} - P_{\text{external},p}| - C_{gas} > 0$$

**Arbitrage Execution:**
For profitable opportunities, execute:
$$\Delta profit = |P_{AMM,p} - P_{\text{external},p}| \cdot \Delta x - C_{gas}$$

### 3. Leveraged Trader Agent

**Optimal Leverage Calculation:**
$$\lambda^* = \arg\max_\lambda \mathbb{E}[R(\lambda \cdot V_i)] - \rho \cdot \mathbb{E}[L(\lambda)]$$

Where:
- $V_i$: Agent's current value
- $R(\lambda \cdot V_i)$: Leveraged returns
- $L(\lambda)$: Liquidation loss probability
- $\rho$: Risk aversion parameter

## Protocol Models

### 1. Staking Pools

**Staking Mechanics:**
For pool $p$ with total staked $S_p(t)$:

**Individual Agent Returns:**
$$R_{i,p}(t+1) = R_{i,p}(t) + \frac{APR_p}{365} \cdot \frac{H_{i,p}(t)}{S_p(t)}$$

**Pool Dynamics:**
$$S_p(t+1) = S_p(t) + \Delta S_p(t)$$
$$APR_p(t+1) = f(S_p(t), R_p(t))$$

### 2. Automated Market Maker (AMM) Pools

**Constant Product Formula:**
$$(R_{a,p} + \Delta a)(R_{b,p} + \Delta b) = R_{a,p} \cdot R_{b,p}$$

**Price Determination:**
$$P_{a/b,p}(t) = \frac{R_{b,p}(t)}{R_{a,p}(t)}$$

**Trading with Slippage:**
$$\Delta output = R_{b,p} - \frac{R_{a,p} \cdot R_{b,p}}{R_{a,p} + (1-fee) \cdot \Delta input}$$

**Liquidity Provision:**
$$LP_{tokens,i,p} = \sqrt{\Delta a \cdot \Delta b}$$
$$share_i = \frac{LP_{tokens,i,p}}{LP_{total,p}}$$

### 3. Impermanent Loss Calculation

**IL for Two-Asset Pool:**
$$IL(\alpha_{final}) = \frac{\alpha_{initial} + \beta_{initial} + 2\sqrt{\alpha_{initial} \cdot \beta_{initial} \cdot \alpha_{final}/\alpha_{initial}}}{1 + \alpha_{final}/\alpha_{initial}} - 1$$

For correlated assets with price ratio $\phi = P_{a}/P_{b}$:

$$IL(\phi_{final}, \phi_{initial}) = \frac{2\sqrt{\phi_{final} / \phi_{initial}}}{1 + \sqrt{\phi_{final} / \phi_{initial}}} - 1$$

### 4. Lending Protocol

**Collateralized Borrowing:**
$$CR_i = \frac{V_{collateral,i}}{V_{borrow,i}} \geq 1.5$$

**Liquidation Condition:**
$$\mathbb{I}(Liquidation_i) = \begin{cases}
1 & \text{if } CR_i < 1.5 \\
0 & \text{otherwise}
\end{cases}$$

**Interest Rate Model:**
$$APR_{lend}(t) = r_0 + k \cdot \frac{Utilization(t)}{1} \cdot max(0, 1 - Utilization(t))$$

Where $Utilization(t) = \frac{Loans(t)}{Deposits(t) + Reserves(t)}$

## System Dynamics

### Agent Behavior Decision Framework

**Universal Decision Model:**
$$\mathbf{P}(action) = \sigma(\mathbf{w} \cdot \mathbf{z} + b)$$

Where:
- $\sigma$: Logistic function for probability
- $\mathbf{z}$: Normalized input features vector
- $\mathbf{w}$: Learned weights
- $b$: Bias term

**Archetype-Specific Inputs:**

*Yield Farmer*:
$$\mathbf{z} = [APR_{\text{effective}}, gas_{\text{cost}}, IL_{\text{risk}}, diversification]$$

*Arbitrageur*:
$$\mathbf{z} = [\Delta P, C_{\text{gas}}, execution_{\text{time}}, competition_{\text{intensity}}]$$

*Leveraged Trader*:
$$\mathbf{z} = [\lambda_{\text{target}}, volatility_{\text{estimate}}, CR_{\text{current}}, liq_{\text{probability}}]$$

### Simulation Dynamics

**Universal Simulation Loop:**

```
For t = 0 to T-1:
    External Price Update: ℰ(t) = {P_external,j(t)}_{j=1}^M
    Agent Strategy Execution: A_i(t+1) = f_i(S_i(t), ℰ(t))
    Protocol State updates: P(t+1) = g(P(t), A(t), ℰ(t))
    Metric Collection: M(t+1) = h(S(t+1), P(t+1))
```

**State Evolution:**
$$\mathbf{S}_i(t+1) = f(\mathbf{S}_i(t), \mathbf{A}_i(t), \mathcal{E}(t))$$

## Key Metrics & Analysis

### Total Value Locked (TVL)
$$TVL(t) = \sum_{p \in \mathcal{P}} V_p(t)$$

Where:
- $\mathcal{P}$: Set of all protocols
- $V_p(t)$: Value locked in protocol $p$ at time $t$

### Protocol Health Score
$$H_p(t) = w_1 \cdot \frac{TVL_p(t)}{TVL_{max}} + w_2 \cdot APR_p(t) - w_3 \cdot IL_{avg,p}(t) - w_4 \cdot LiqRate_p(t)$$

### Capital Efficiency
$$\eta = \frac{\mathbb{E}[R]}{Risk + Regularization}$$

Where $R$ represents returns and Risk includes IL, liquidation, and volatility.

### Systemic Risk Measures

**Inter-Protocol Correlation:**
$$\rho_{p,q} = \frac{\text{Cov}(APR_p, APR_q)}{\sqrt{\text{Var}(APR_p) \cdot \text{Var}(APR_q)}}$$

**Cascade Liquidation Potential:**
$$C_p(t) = \sum_{i \in \mathcal{L}_p(t)} V_{collateral,i}(t)$$

## Integration with Existing Systems

### Bridge to Governance System
Treasury allocation from DAO votes:
$$Allocation_p = VoteShare_p \cdot Treasury(t)$$

### Bridge to Affiliate System
Commission-based staking rewards:
$$Reward_{affiliate,i} = Commission_i \cdot \alpha_{stake}$$

### Bridge to Bonding Curve System
Dual price discovery:
$$P_{hybrid} = \beta \cdot P_{AMM} + (1-\beta) \cdot f_{bonding}(S)$$

### Bridge to MCP System
Resource delegation to DeFi protocols:
$$Capacity_{delegated,j} = \eta_j \cdot C_j \cdot p_j$$

Where $p_j$ represents protocol participation preference.

## Implementation Notes

This mathematical formulation provides the theoretical foundation for the DeFi simulation, maintaining consistency with the unified mathematical framework while capturing the specific dynamics of decentralized finance protocols. The agent-based modeling approach allows for emergent behaviors arising from strategic interactions between protocols and diverse agent archetypes.

The implementation in `notebook/main.py` translates these mathematical concepts into executable Python code, enabling empirical testing and validation of the theoretical framework.