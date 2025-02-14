# bonding curve

This repository contains a Python simulation of a bonding curve mechanism with interacting agents, along with a mathematical formulation of the model. The primary goal is to explore the dynamics of bonding curves and optimize their parameters to achieve desired market behaviors, such as minimizing price volatility.

## Overview

This project consists of two main components:

1. **Python Simulation (`main.py`):** A Python script that simulates a market with a bonding curve and multiple trading agents. Agents make buy and sell decisions based on observed price trends. The simulation allows for experimentation with different bonding curve types and their parameters.
2. **Mathematical Formulation (`math.md`):** A document providing a formal mathematical description of the bonding curve model, agent behavior, and the optimization problem. This document serves as a theoretical foundation for the simulation.

## Key Features of the Simulation

*   **Multiple Bonding Curve Types:** The simulation supports several common bonding curve functions:
    *   Linear
    *   Exponential
    *   Sigmoid
    *   Multi-segment
*   **Agent-Based Modeling:** Simulates individual agents with capital and token holdings, making trading decisions based on:
    *   Trading frequency
    *   Trade size
    *   Memory of past prices
    *   Trend detection
*   **Parameter Optimization:** Implements a basic optimization routine to find bonding curve parameters that minimize token price volatility.
*   **Market Dynamics:** Simulates the interaction between agents and the bonding curve, showing how supply, price, and agent wealth evolve over time.
*   **Visualization:** Generates plots to visualize key metrics like token supply, token price, and agent capital/token distribution over the simulation period.

## Getting Started

### Prerequisites

*   Python 3.x
*   TensorFlow (`pip install tensorflow`)
*   NumPy (`pip install numpy`)
*   Matplotlib (`pip install matplotlib`)

### Running the Simulation

1. **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```
2. **Run the Python script:**
    ```bash
    python main.py
    ```

    The script will perform an optimization run for the specified `OPTIMIZE_CURVE_TYPE` and then simulate the market with the optimal parameters found.

### Understanding the Code

*   **Configuration:** The top section of `main.py` defines various parameters for the simulation, such as the number of agents, simulation steps, initial conditions, and agent trading behavior.
*   **Bonding Curve Functions:** The `calculate_bonding_curve_price` function implements the different bonding curve formulas.
*   **Agent Class:** The `Agent` class defines the state and behavior of individual trading agents.
*   **Simulation Logic:** The `simulation_step` function executes a single step of the simulation, handling agent trading and updating the market state.
*   **Optimization:** The `optimize_bonding_curve` function implements a randomized search to find optimal bonding curve parameters.
*   **Main Execution:** The `if __name__ == "__main__":` block orchestrates the optimization and simulation process.

## Understanding the Mathematical Model

For a detailed mathematical formulation of the bonding curve model, agent behavior, and the optimization problem, please refer to the `math.md` document. This document provides the formal definitions and equations that underpin the simulation.

## Customization

You can customize the simulation by modifying the parameters in the configuration section of `main.py`. This includes:

*   **Bonding Curve:** Changing the `BONDING_CURVE_TYPE` and the default parameters within the `calculate_bonding_curve_price` function.
*   **Agent Behavior:** Adjusting parameters like `AGENT_TRADE_FREQUENCY`, `AGENT_TRADE_SIZE_RANGE`, `AGENT_MEMORY_SIZE`, `AGENT_TREND_THRESHOLD`, and `AGENT_TREND_DELAY`.
*   **Simulation Settings:** Modifying `NUM_AGENTS`, `SIMULATION_STEPS`, and initial economic conditions.
*   **Optimization:** Changing the `OPTIMIZE_CURVE_TYPE` and the number of optimization trials (`n_trials`).

## Results and Visualization

After running the simulation, several `.png` files will be generated, visualizing the following:

*   `optimal_token_supply.png`: Token supply over time with optimal parameters.
*   `optimal_token_price.png`: Token price over time with optimal parameters.
*   `optimal_agent_capital.png`: Average agent capital over time with optimal parameters.
*   `optimal_agent_tokens.png`: Average agent tokens over time with optimal parameters.
*   `optimal_wealth_distribution.png`: Histograms showing the distribution of capital and tokens among agents at different time points.

These visualizations provide insights into the dynamics of the simulated market and the effects of the optimized bonding curve parameters.

## Contributing

Contributions to this project are welcome! If you have suggestions for improvements, new features, or bug fixes, please feel free to submit a pull request.

## License

MIT-0 License