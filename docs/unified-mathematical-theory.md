# Unified Mathematical Theory of Token Economy Simulations

**Token Economy Simulation Suite - Mathematical Foundations**

*Version 1.0*

## Table of Contents

- [Chapter 1: Foundations & Meta-Framework](#chapter-1-foundations--meta-framework)
  - [1.1 Universal Notation Standard](#11-universal-notation-standard)
  - [1.2 Agent-Based Modeling Meta-Framework](#12-agent-based-modeling-meta-framework)
  - [1.3 Common Theoretical Assumptions](#13-common-theoretical-assumptions)
  - [1.4 Mathematical Equivalence Theorems](#14-mathematical-equivalence-theorems)

- [Chapter 2: Core Economic Units & Assets](#chapter-2-core-economic-units--assets)
- [Chapter 3: Price & Value Dynamics](#chapter-3-price--value-dynamics)
- [Chapter 4: Agent Behavior & Decision Making](#chapter-4-agent-behavior--decision-making)
- [Chapter 5: System Dynamics & Evolution](#chapter-5-system-dynamics--evolution)
- [Chapter 6: Optimization & Analysis Framework](#chapter-6-optimization--analysis-framework)
- [Chapter 7: Empirical Validation](#chapter-7-empirical-validation)
- [Chapter 8: Advanced Applications](#chapter-8-advanced-applications)

## Chapter 1: Foundations & Meta-Framework

### 1.1 Universal Notation Standard

#### 1.1.1 Core Notation Convention

The unified mathematical framework employs consistent notation to represent economic concepts across all simulation subsystems (Affiliate, Airdrop, Bonding Curve, and MCP). The notation convention follows a hierarchical structure:

```
Entity.Index[].Time[Parameter]
```

**Convention Rules:**
- **Entity Type**: Capital letters for system-level concepts (Tokens, Resources, Agents)
- **Individual Elements**: Lower case with subscripts (agent $i$, resource $j$, token $k$)
- **Time Dimension**: Parenthetical time notation $(\cdot(t))$ for temporal evolution
- **Parameter Variants**: Bracket notation $(\cdot[param])$ for parameter-dependent variants
- **Vector/Matrix Quantity**: Bold font $(\mathbf{V})$ for multi-dimensional quantities

#### 1.1.2 Universal Notation Glossary

| Symbol | Meaning | Context | Status |
|--------|---------|---------|--------|
| $t$ | Discrete time step | All systems | Universal |
| $i$ | Individual entity index (Agent $i$) | All systems | Universal |
| $j$ | Resource/Asset index | MCP, Affiliate | Adapter |
| $k$ | Token type index | Affiliate, Bonding | Adapter |
| $\mathbf{A}$ | Set of agents | All systems | Universal |
| $\mathcal{T}$ | Time horizon | All systems | Universal |
| $\mathbb{I}(\cdot)$ | Indicator function | All systems | Universal |
| $\mathbf{P}(X; \theta)$ | Probability of event $X$ given parameter $\theta$ | All systems | Universal |

#### 1.1.3 Subsystem-Specific Adaptations

**Affiliate System Adaptation:**
```
S_i(t) → Token i supply at time t
B_j(t) → Base currency balance of affiliate j
C_j(t) → Commission rate of affiliate j
W_{j,k}(t) → Token k holdings of affiliate j
```

**Airdrop System Adaptation:**
```
T_t → Total token supply (scalar)
H_i(t) → Holdings of agent i
α_i(t) → Demand multiplier of agent i
M(t) → Market sentiment factor
```

**Bonding Curve Laboratory Adaptation:**
```
S(t) → System supply (scalar focus)
C_i(t) → Capital of agent i
T_i(t) → Token holdings of agent i
M_i(t) → Price memory array of agent i
```

**MCP System Adaptation:**
```
C_j(t) → Capacity of resource j
L_j(t) → Load/current usage of resource j
Pr_j(t) → Price of resource j
B_i(t) → Balance of agent i
```

### 1.2 Agent-Based Modeling Meta-Framework

#### 1.2.1 Universal Agent Representation

Each simulation subsystem models autonomous agents that interact within an economic environment. The unified framework abstracts these agents into a universal representation characterized by behavioral parameters, decision-making mechanisms, and resource constraints.

**Formal Agent Definition:**

Let $\mathcal{A}$ be the set of all agents in a simulation system. Each agent $a \in \mathcal{A}$ is characterized by a tuple:

$$a = (\mathbf{State}(t), \mathbf{Params}, \mathbf{Behavior}, \mathbf{Constraints})$$

Where:

- $\mathbf{State}(t) \in \mathbb{R}^d$: Agent's current economic state (balances, holdings, etc.)
- $\mathbf{Params} \in \mathbb{R}^p$: Static behavioral parameters (risk tolerance, preferences)
- $\mathbf{Behavior}: \mathbb{R}^d \times \mathbb{R}^p \times \mathbb{R}^e \to \mathcal{Actions}$: Decision-making function
- $\mathbf{Constraints} \subset \mathbb{R}^d$: Feasibility set defining resource/capability limits

#### 1.2.2 Universal Simulation Loop

All subsystems follow a common discrete-time simulation paradigm that can be abstracted as Sequential Decision Process:

**Initialization:** $t = 0,\; \mathbf{State}(0) \sim \mathbf{p}_0$

**For** $t = 0, 1, \dots, T-1$:

1. **Environmental Update:** Global environment $\mathcal{E}(t)$
2. **Agent Perception:** Each agent observes relevant information $\mathbf{Obs}_i(t)$
3. **Decision Making:** Actions $\mathbf{A}_i(t) = \mathbf{Behavior}_i(\mathbf{Obs}_i(t), \mathbf{Params}_i)$
4. **Resource Allocation:** Conflicts resolved via allocation mechanism
5. **State Evolution:** $\mathbf{State}_i(t+1) = f(\mathbf{State}_i(t), \mathbf{A}_i(t), \mathcal{E}(t+1))$
6. **Performance Metrics:** Compute system-level indicators

**Termination Criteria:**
- Time horizon reached: $t = T$
- Convergence conditions met
- Bankruptcy thresholds exceeded

#### 1.2.3 Agent Interaction Primitives

**Communication Layer:** $\gamma: \mathcal{A} \times \mathcal{A} \to \{0,1\}$ indicating interaction possibility

**Trade Function:** $\tau: \mathbf{State}^2 \to \mathbf{State}^2$ atomic exchange mechanism

**Market Clearing:** $\phi: \mathbf{Actions}, \mathcal{E} \to \mathbf{Allocations}$ resource distribution algorithm

### 1.3 Common Theoretical Assumptions

#### 1.3.1 Economic Theory Foundations

1. **Rational Bounded Agency:** Agents act self-interestedly within cognitive and informational constraints
2. **Perfect Market Access:** Unless explicitly modeled, agents have unlimited access to market information
3. **Resource Conservation:** Economic resources follow conservation laws (supply/demand balance)
4. **Time Discretization:** All processes modeled as discrete-time for computational tractability
5. **Markov Property:** Future states depend only on current state, not historical path (unless explicit memory modeled)

#### 1.3.2 Computational Assumptions

1. **Numerical Stability:** All operations are implemented in finite-precision arithmetic
2. **Finite Horizon:** Simulations run for finite time periods $T < \infty$
3. **Finite Agent Population:** Set of agents $\mathcal{A}$ is countable and finite
4. **Finite State Spaces:** All economic quantities belong to bounded regions
5. **Deterministic Dynamics:** Given identical parameters and random seeds, simulations are reproducible

#### 1.3.3 Behavioral Assumptions

1. **Loss Aversion:** Agents exhibit asymmetric response to gains/losses
2. **Social Influence:** Agent behavior affected by system-level indicators
3. **Learning Capacity:** Agents can adjust behavior based on experience/memory
4. **Satiety Effects:** Marginal utility of resources diminishes with accumulation
5. **Network Effects:** Agent utility can depend on total system participation

### 1.4 Mathematical Equivalence Theorems

#### 1.4.1 Asset Token Equivalence Theorem

**Theorem 1 (Asset Equivalence):**
Token-based economic systems (Affine) and Resource-based systems (MCP) are mathematically isomorphic when considering equivalent economic observables.

**Formal Statement:**
Let $\mathcal{T} = (T, P)$ be a token system and $\mathcal{R} = (C, Pr)$ be a resource system. Then:

$$
\begin{pmatrix} S_i \\ P_i \end{pmatrix}
\cong
\begin{pmatrix} C_j(1-L_j/C_j) \\ Pr_j \end{pmatrix}
$$

Under the transformation mapping supply $S_i \mapsto$ available capacity $C_j\,(1-L_j/C_j)$ and price $P_i \mapsto$ resource price $Pr_j$.

**Implications:**
- Price elasticity relationships equivalent across systems
- Supply-demand dynamics follow identical mathematical forms
- Optimization problems can be translated between systems
- Cross-validation possible between token and resource models

#### 1.4.2 Decision Probability Equivalence

**Theorem 2 (Decision Unification):**
All agent decision probabilities across subsystems can be expressed in terms of unified sigmoid functions with equivalent parameter mappings.

**Mathematical Form:**
For any agent decision probability $\mathbf{P}(action|\input)$:

$$\mathbf{P}(action) = \sigma(\mathbf{w} \cdot \mathbf{z} + b)$$

Where:
- $\sigma$ is the logistic function
- $\mathbf{z}$ is the normalized input vector
- $\mathbf{w}$ is the influence vector
- $b$ is the bias term

**Subsystem Mappings:**
- **Affiliate:** $action \in \{buy, sell\}$, $input = (price_{\text{target}} - price_{\text{current}})/price_{\text{base}}, agent_{\text{balance}}$
- **Airdrop:** $action \in \{buy, sell\}$, $input = price_{\text{variation}}, market_{\text{sentiment}}, holdings$
- **Bonding:** $action \in \{hold, trade\}$, $input = price_{\text{trend}}, memory_{\text{analysis}}$
- **MCP:** $action \in \{request, hold\}$, $input = demand_{\text{preference}}, resource_{\text{availability}}, balance$

#### 1.4.3 Wealth Distribution Universality

**Theorem 3 (Gini Generalization):**
All subsystems employ equivalent wealth inequality metrics that can be unified under a generalized Gini coefficient framework.

**Unified Gini Formulation:**
For any wealth distribution $W = \{w_1, \dots, w_n\}$, the Gini coefficient can be computed as:

$$G(W) = \frac{\sum_{i}\sum_{j}|w_i - w_j|}{2n\sum_{i}w_i}$$

Where $n = |\mathcal{A}|$ and the wealth variable $w_i$ is mapped appropriately per subsystem:
---

## Chapter 2: Core Economic Units & Assets

### 2.1 Economic Assets: Universal Representation

All simulation subsystems model economic value through assets that can be traded, held, and accumulated. The unified framework represents these assets as stateful objects with supply-demand dynamics.

**Universal Asset Definition:**

An economic asset $\mathcal{A}$ is characterized by the tuple:

$$\mathcal{A} = (S(t), P(t), \theta, \mathcal{D}(t), \Phi)$$

Where:
- $S(t)$: Supply/availability at time $t$
- $P(t)$: Market price at time $t$
- $\theta$: Static structural parameters (e.g., curve types, maxima)
- $\mathcal{D}(t)$: Demand profile at time $t$
- $\Phi$: Transformation rules (e.g., regeneration, allocation)

### 2.2 Token-Based Assets (Affiliate System Perspective)

#### 2.2.1 Token Family Model

The affiliate system employs parallel token economies where each token constitutes an independent but interconnected economic asset.

**Token Definition:**
For each token $i$ in $\{1, \dots, N_T\}$:

$$\mathcal{T}_i = (S_i(t), P_i(t), f_i, \mathcal{D}_i(t), \Phi_{\text{trading}})$$

**Supply Dynamics:**
$$S_i(t+1) = S_i(t) + \sum_{j \in \mathcal{F}} \Delta T_{j,i}(t)$$

Where $\mathcal{F}$ is the set of affiliates actively trading token $i$.

**Price Determination:**
$$P_i(t) = f_i(S_i(t), \theta_i(t))$$

#### 2.2.2 Inter-Token Relationships

Tokens interact through correlation of affiliate behavior and economic disturbances.

**Cross-Token Influence:**
$$\rho_{i,j}(t) = \text{corr}(P_i(t), P_j(t))$$

Where correlation is measured over a sliding window of historical prices.

### 2.3 Resource-Based Assets (MCP System Perspective)

#### 2.3.1 Resource Capacity Model

The MCP system models assets as depletable but regenerable resources with capacity constraints.

**Resource Definition:**
For each resource $j$ in $\{1, \dots, R\}$:

$$\mathcal{R}_j = (C_j(t), L_j(t), Pr_j(t), \mathcal{U}_j(t), \Phi_{\text{maintenance}})$$

**Capacity Evolution:**
$$C_j(t+1) = \min(C_{\max}, C_j(t) \cdot (1 + \gamma_j + \eta_j \cdot \bar{B}(t)))$$

**Demand Relationship:**
$$L_j(t) = \sum_{i \in \mathcal{A}} A_{i,j}(t)$$

#### 2.3.2 Resource Utilization Patterns

**Utilization Ratio:**
$$u_j(t) = \frac{L_j(t)}{C_j(t)}$$

**Efficiency Metrics:**
$$\eta_j(t) = \frac{\sum_{i} U_{i,j}(t)}{L_j(t)}$$

### 2.4 Trading-Focused Assets (Bonding Curve Perspective)

#### 2.4.1 Market Asset Dynamics

The bonding curve system views assets through the lens of immediate market interactions.

**Asset State Representation:**
$$\mathcal{B} = (S(t), P(t), \mathbf{f}_{\mathcal{C}}, V(t), \Phi_{\text{curve}})$$

**Instantaneous Price Response:**
$$P(t) = \mathbf{f}_{\mathcal{C}}(S(t))$$

#### 2.4.2 Asset Volatility Modeling

**Volatility Measures:**
$$\sigma_P(t) = \sqrt{\frac{1}{M-1} \sum_{k=1}^{M} (P(t-k+1) - \bar{P}(t))^2}$$

Where $\bar{P}(t)$ is the mean price over the memory window of size M.

### 2.5 Distribution Pattern Assets (Airdrop System Perspective)

#### 2.5.1 Token Distribution Mechanics

The airdrop system integrates asset distribution as a fundamental property.

**Distribution-Enhanced Asset:**
$$\mathcal{A} = (\mathbf{abundance}, P(t), \mathbf{v}, \mathbf{h}, \Phi_{\text{distribution}})$$

**Vested Asset Accumulation:**
$$S^v_i(t) = \min(S^{\text{allocated}}_i, \mathbf{v}(t, \text{threshold}))$$

#### 2.5.2 Utility-Adjusted Asset Values

**Perceived Asset Value:**
$$V_i(t) = P(t) \cdot (1 + \alpha_i(t) \cdot u_i(t))$$

Where $u_i(t)$ represents utility modifier based on holdings.

### 2.6 Asset Equivalence Transformations

#### 2.6.1 Token ↔ Resource Mapping

**Theorem 4 (Resource Token Equivalence):**
Token supply $S_i$ and resource available capacity $C_j(1-L_j/C_j)$ are economically equivalent under proper scaling.

**Transformation Mapping:**
$$\varphi: S_i \mapsto C_j \cdot (1 - u_j) : \mathbb{R}^+ \to \mathbb{R}^+)$$

#### 2.6.2 Valuation Consistency

**Price Relationship:**
$$P_i \cong Pr_j \cdot \frac{S_i}{C_j \cdot (1 - u_j)}$$

For equivalent economic value per unit across systems.

### 2.7 Asset Dynamics Universals

#### 2.7.1 Supply Evolution Master Equation

**General Supply Dynamics:**
$$S(t+1) = S(t) + \Delta S^{\text{inflow}}(t) - \Delta S^{\text{outflow}}(t) + \Delta S^{\text{internal}}(t)$$

Where:
- $\Delta S^{\text{inflow}}$: External additions (airdrops, regeneration)
- $\Delta S^{\text{outflow}}$: External removals (burns, depreciation)
- $\Delta S^{\text{internal}}$: Internal reallocations (trading, redistribution)

#### 2.7.2 Cross-System Asset Parameters

**Universal Asset Parameters Table:**

| Parameter | Affiliate System | MCP System | Bonding System | Airdrop System |
|-----------|------------------|-------------|----------------|----------------|
| Supply | $S_i(t)$ | $C_j(t)$ | $S(t)$ | $T(t)$ |
| Price | $P_i(t)$ | $Pr_j(t)$ | $P(t)$ | $P(t)$ |
| Demand | $\mathcal{D}_i(t)$ | Aggregation | Instant | $\mathcal{D}(t)$ |
| Allocation | Commissions | Capacity | Curve | Vesting |

This chapter establishes the common ground for understanding how each subsystem represents economic value, enabling cross-system comparisons and theoretical developments in subsequent chapters.

---

## Chapter 3: Price & Value Dynamics

### 3.1 Bonding Curve Functions - Universal Formulation

#### 3.1.1 General Bonding Curve Definition

**Definition:** A bonding curve is a functional relationship $f: \mathbb{R}^+ \to \mathbb{R}^+$ between asset supply and price:

$$P(S) = f(S; \theta)$$

Where $\theta \in \Theta$ is the parameter set characterizing the curve's shape and characteristics.

#### 3.1.2 Universal Curve Family

The framework supports a generalized bonding curve family that encompasses the specific implementations from all subsystems:

**Linear Curves:**
$$f_L(S) = m S + b$$

**Exponential Curves:**
$$f_E(S) = a e^{k S}$$

**Sigmoid Curves:**
$$f_S(S) = K / (1 + e^{-k(S - S_0)}) + b$$

**Multi-Segment Curves:**
$$f_M(S) = \begin{cases}
  m_1 S & \text{if } S \le S_b \\
  m_1 S_b + f_E(S - S_b) & \text{if } S > S_b
\end{cases}$$

**Root Curves:**
$$f_R(S) = k \sqrt{S} + b$$

**Inverse Curves:**
$$f_I(S) = k / (S + \epsilon) + b$$

Where $\epsilon > 0$ prevents singularity.

#### 3.1.3 Curve Characteristics Analysis

**Elasticity Analysis:**
$$\varepsilon(S) = \frac{dP/dS}{P/S} = \frac{f'(S) \cdot S}{f(S)}$$

**Inflection Points:**
Points where curve curvature changes, determining price stability regions:
$$f''(S) = 0$$

**Asymptotic Behavior:**
$$\lim_{S \to \infty} P(S) = asymptote$$

### 3.2 Market Clearing Mechanisms

#### 3.2.1 Supply-Demand Equilibrium

**General Equilibrium Condition:**
$$\mathcal{S}(t) = \mathcal{D}(t)$$

Where supply and demand may be implicit functions of price.

#### 3.2.2 Price Adjustment Process

**Multiple System Approaches:**

1. **Direct Price Setting (Bonding Curves):**
   $$P(t+1) = f(S(t+1))$$

2. **Market Clearing (Airdrop/MCP):**
   $$P(t+1) = P_0 \cdot (1 + \alpha \cdot (D(t) - S(t))/V_0 + \noise)$$

3. **Agent-Based Equilibrium (Affiliate):**
   $$P(t+1) = f(S(t+1)) + \beta \cdot \mathcal{M}(t)$$

Where $\mathcal{M}(t)$ represents market sentiment or demand factors.

#### 3.2.3 Convergence Properties

**Fixed Point Analysis:**
Solutions to $P^* = f(S^*(P^*))$

**Stability Condition:**
$$|\partial P/\partial S| < 1$$
for stable price-supply relationship.

### 3.3 Volatility and Stability Analysis

#### 3.3.1 Price Volatility Measures

**Standard Volatility:**
$$\sigma_P = \sqrt{\frac{1}{T-1} \sum_t (P_t - \bar{P})^2}$$

**Logarithmic Volatility:**
$$\sigma_{\ln P} = \sqrt{\frac{1}{T-1} \sum_t (\ln P_t - \ln P_{t-1})^2}$$

#### 3.3.2 System Stability Regions

**Lyapunov Function for Stability:**
$$V(S, P) = (P - P^*)^2 + \delta (S - S^*)^2 + \gamma \dot{P}^2$$

Stability when $\dot{V} \le 0$.

### 3.4 External Price Influences

#### 3.4.1 Sentiment and Random Factors

**Market Sentiment Model:**
$$M(t+1) = \rho M(t) + (1-\rho) \mu + \sigma \epsilon_t$$
$$\epsilon_t \sim \mathcal{N}(0,1)$$

**Price Impact Integration:**
$$P(t+1) = f(S(t+1)) \cdot (1 + \eta M(t) + \epsilon_t)$$

#### 3.4.2 Cross-Asset Correlation

**Price Cross-Correlation:**
$$\rho_{i,j} = \frac{\text{Cov}(P_i, P_j)}{\sqrt{\text{Var}(P_i)\text{Var}(P_j)}}$$

This completes the foundational chapters establishing the unified theoretical framework. The subsequent chapters will integrate these foundations with specific analytical methods and optimization approaches.

---

*Continued in subsequent sections...*

| Subsystem | Wealth Measurement $w_i$ |
|-----------|------------------------|
| Affiliate | Base currency balance $B_j$ |
| Airdrop | Token holdings $H_i \cdot P(t)$ |
| Bonding | Portfolio value $C_i + T_i \cdot P(t)$ |
| MCP | Balance $B_i$ |

**Properties:**
- Scale invariant: $G(cW) = G(W)$ for constant $c > 0$
- Population invariant: Independent of agent count
- Lorenz curve representation possible in all systems

These foundational theorems establish the mathematical basis for cross-subsystem analysis and parameter mapping, enabling unified theoretical treatment of the diverse economic simulation approaches.

---

*This document provides the mathematical foundations for unifying the four simulation subsystems. Subsequent chapters will expand on the specific models while maintaining consistency with these foundational principles.*