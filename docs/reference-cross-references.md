# Mathematical Theory Cross-References

**Token Economy Simulation Suite - Mathematical Reference Guide**

This document provides cross-references between the unified mathematical framework and the subsystem-specific formulations.

## 1. Affine System Integration Points

### 1.1 Token Supply Dynamics
- **Unified Framework:** $S_i(t+1) = S_i(t) + \Delta S^{\text{inflow}}(t)$
- **Affine Specific:** Buy/sell transactions $\Delta T_{j,i}(t)$
- **Cross-Reference:** Chapter 2.2.1, Chapter 3.2.1

### 1.2 Commission Rate Dynamics
- **Unified Framework:** $C_j(t) \in [C_{\min}, C_{\max}]$
- **Affine Dynamics:** Based on holding average, market performance
- **Cross-Reference:** Chapter 1.4.2, Section A3.2 (Appendix)

## 2. Airdrop System Integration Points

### 2.1 Demand Multiplier Evolution
- **Unified Framework:** $\alpha_i(t+1) = \min(1, \alpha_i(t) + \delta)$
- **Airdrop Specific:** Vesting-dependent growth
- **Cross-Reference:** Chapter 4.2.1, Theorem 2

### 2.2 Market Sentiment Coupling
- **Unified Framework:** $M(t+1) = f(M(t), \epsilon_t)$
- **Airdrop Application:** Price signal modifier
- **Cross-Reference:** Chapter 3.4.1

## 3. Bonding Curve Laboratory Integration

### 3.1 Price Memory Representations
- **Unified Framework:** $M_{i,t} \in \mathbb{R}^W$
- **Bonding Specific:** Rolling price windows
- **Cross-Reference:** Chapter 4.3.1, Theorem 2

### 3.2 Trend Signal Processing
- **Unified Framework:** $\mathbf{P}(signal) = \sigma(\mathbf{w} \cdot \mathbf{z})$
- **Bonding Application:** Buy/sell decision probability
- **Cross-Reference:** Chapter 3.3.1

## 4. MCP System Integration

### 4.1 Resource Capacity Management
- **Unified Framework:** $C_j(t+1) = \min(C_{\max}, C_j(t) \cdot g(t))$
- **MCP Specific:** Base regeneration + economic feedback
- **Cross-Reference:** Chapter 2.3.1, Theorem 4

### 4.2 Allocation Priority Mechanisms
- **Unified Framework:** $\phi: \mathbf{Actions}, \mathcal{E} \to \mathbf{Allocations}$
- **MCP Implementation:** Random-ordered sequential allocation
- **Cross-Reference:** Chapter 5.2

## 5. Subsystem-Specific Mathematical Extensions

### 5.1 Affine-Derived Concepts
- **Whale Agent Classification:** Based on commission rate thresholds
- **Cross-Token Price Correlation:** Inter-dependent market dynamics
- **Dynamic Curve Parameters:** Time-varying bonding curve modifications

### 5.2 Airdrop-Derived Concepts
- **Tiered Distribution Logic:** Eligibility-weighted allocation
- **Vesting Schedule Mathematics:** Time-dependent accessibility functions
- **Activity Threshold Mechanics:** Performance-based qualification
- **Market Sentiment Feedback:** Auto-correlation and erosion factors

### 5.3 Bonding-Derived Concepts
- **Memory-Based Trend Analysis:** Historical price pattern recognition
- **Volatility-Driven Trading:** Risk-adjusted decision making
- **Multi-Segment Curve Dynamics:** Phase-transition pricing behavior

### 5.4 MCP-Derived Concepts
- **Capacity Regeneration Models:** Economic activity-dependent recovery
- **Load Distribution Functions:** Resource utilization balancing
- **Priority Allocation Schemes:** Competition resolution mechanisms
- **Maintenance Cost Functions:** Ongoing operational requirements

## 6. Mathematical Translations Between Systems

### 6.1 Concept Equivalences

| Universal Concept | Affine Terms | Airdrop Terms | Bonding Terms | MCP Terms |
|-------------------|--------------|---------------|---------------|-----------|
| Price Signal | $P_i(t)$ | $P(t) + M(t)$ | $f(S(t))$ | $Pr_j(t)$ |
| Supply Control | $\Delta T_{j,i}$ | $\Delta S^{\text{burn}}$ | $\Delta S$ | $L_j(t+1)-L_j(t)$ |
| Agent Utility | $B_j(t)$ | $H_i(t)P(t)$ | $C_i+T_i P(t)$ | $B_i(t)$ |
| Resource Allocation | Commission share | Distribution fraction | Curve dynamics | Capacity extension |

### 6.2 Parameter Mapping Functions

```
Φ_affine_to_mcp(b_j): Affiliate.balance → MCP.balance = b_j / scale_factor
Φ_mcp_to_affine(l_j): MCP.load → Affine.supply_projection = base_token * (1 + l_j/capacity)
Φ_bonding_to_affine(σ_p): Bonding.volatility → Affine.commission_rate = min(max_rate, σ_p * γ)
Φ_airdrop_to_all(t_t): Airdrop.vesting_period → Universal.time_window = t_t
```

These cross-references enable seamless translation between subsystems while preserving mathematical rigor and economic intuition. The mappings preserve the essential dynamics while accommodating system-specific implementation details.