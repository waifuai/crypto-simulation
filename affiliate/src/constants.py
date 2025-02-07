NUM_SIMULATION_STEPS: int = 100
NUM_TOKENS: int = 5
NUM_AFFILIATES: int = 5
INITIAL_SUPPLY: int = 10000
INITIAL_PRICE: float = 1.0
INITIAL_COMMISSION_RATE: float = 0.10
AFFILIATE_STARTING_POINT: int = 0
INITIAL_BASE_CURRENCY: int = 1000
INITIAL_TOKEN_INVESTMENT: int = 10
COMMISSION_DYNAMICS_STEP: int = 10
DYNAMIC_ADJUSTMENT_RATE: float = 0.0005  # Reduced adjustment rate
MOVING_AVERAGE_WINDOW: int = 50  # Increased window for smoother price adjustments
PRICE_IMPACT_FACTOR: float = 0.01  # Reduced impact factor
BONDING_CURVE_TYPE_CHANGE_INTERVAL: int = 80 # Increased interval
BONDING_CURVE_PARAM_CHANGE_INTERVAL: int = 20 # Reduced interval for more frequent parameter tweaks

# Variable bonding curve change intervals for each token
import numpy as np
bonding_curve_change_intervals = np.random.choice(
    range(500, 1001), size=NUM_TOKENS, replace=True
)