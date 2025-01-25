# affiliate

**Key Features:**

* **Token Creation:**  Simulates multiple tokens, each with its own supply and price.
* **Dynamic Bonding Curves:** Token prices are determined by bonding curves, which mathematically link the token's price to its supply. The simulation includes several types of bonding curves (linear, exponential, sigmoid, root, inverse), and the active bonding curve for each token can change periodically. The parameters of these curves can also be adjusted dynamically.
* **Affiliate Network:** Models a network of affiliates who can buy and sell tokens.
* **Commissions:** Affiliates earn commissions, and their commission rates can dynamically adjust based on their activity and earnings.
* **Simulation Steps:** The simulation progresses in discrete time steps, with actions and calculations performed at each step.
* **Data Logging and Analysis:** The simulation logs key metrics like token prices, supplies, affiliate balances, and commission rates over time. This data can be used for analysis and visualization.
* **Mathematical Foundation:** The code is based on the mathematical principles of bonding curves and economic modeling, as detailed in the accompanying `math.md` document.

**What the Code Does:**

The `main.py` script simulates the following process:

1. **Initialization:**
   - Sets up the simulation environment, including the number of tokens, affiliates, and initial parameters (supply, price, commission rates, etc.).
   - Creates instances of `Token` and `Affiliate` classes. Each token is initialized with a starting bonding curve function.

2. **Simulation Loop:**
   - Iterates through a specified number of simulation steps.
   - **Token Simulation Step:**
     - For each affiliate, simulates buying and selling tokens based on their available base currency and token holdings.
     - Recalculates token prices based on the current supply and the active bonding curve.
     - Periodically changes the bonding curve function or its parameters for each token.
   - **Affiliate Simulation Step:**
     - Simulates periodic selling of tokens by affiliates.
     - Tracks affiliate earnings and dynamically adjusts their commission rates based on their performance.

3. **Data Collection:**
   - At each step, records the price and supply of each token, the base currency and token holdings of each affiliate, and their commission rates.

4. **Analysis and Visualization:**
   - After the simulation completes, the script analyzes the collected data, calculating statistics like mean and standard deviation of prices and supplies.
   - It generates plots visualizing:
     - Token prices over time.
     - Token supply over time.
     - Token price vs. supply.
     - Average affiliate base currency over time.
     - Average affiliate commission rate over time.
     - Base currency of whale and non-whale affiliates.
     - Wallet composition of an example affiliate.
   - Includes more advanced plotting functions for analyzing token prices, supply, and affiliate base currency distributions using `matplotlib`.

**Mathematical Basis (`math.md`):**

The `math.md` file provides a mathematical formulation of the simulated token economy. It defines the key variables and relationships, including:

* **Token Price Function:**  $P_i(t) = f_i(S_i(t), \theta_i(t))$, where the price of token $i$ at time $t$ depends on its supply $S_i(t)$ and the parameters of the bonding curve $\theta_i(t)$.
* **Bonding Curve Formulas:**  Explicit mathematical expressions for the linear, exponential, sigmoid, root, and inverse bonding curves.
* **Transaction Dynamics:** Mathematical descriptions of how buying and selling tokens affect token supply and affiliate balances.
* **Commission Adjustment Rules:**  A logical or piecewise function describing how affiliate commission rates are adjusted dynamically based on their performance.

Referencing the math paper allows for a deeper understanding of the underlying economic principles and mathematical models that the Python code implements.

**How to Use the Code:**

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install Dependencies:**
   ```bash
   pip install pandas tensorflow numpy matplotlib
   ```

3. **Run the Simulation:**
   ```bash
   python code/kaggle/affiliate/main.py
   ```

4. **Analyze Results:**
   - The script will output logging information during the simulation.
   - After the simulation, it will print summary statistics and display various plots visualizing the simulation results.
   - You can further analyze the `token_histories` and `affiliate_histories` data structures in the code or save them to files for more detailed analysis.

**File Structure:**

* `main.py`: The main Python script containing the simulation code.
* `math.md`: The Markdown file detailing the mathematical formulation of the simulation.

**Potential Extensions:**

This simulation provides a foundation for exploring more complex token economic models. Potential extensions include:

* **More Sophisticated Affiliate Strategies:** Implement different buying and selling strategies for affiliates, including AI-driven agents.
* **External Factors:** Introduce external events or market conditions that can influence token prices and affiliate behavior.
* **Network Effects:** Model interactions and dependencies between different tokens or affiliates.
* **Governance Mechanisms:** Simulate the impact of voting or other governance mechanisms on the token economy.

This project utilizes TensorFlow for numerical computation, enabling efficient simulation of the dynamic system. By running and modifying this code, you can gain valuable insights into the behavior of token economies with evolving bonding curves and participant dynamics.
