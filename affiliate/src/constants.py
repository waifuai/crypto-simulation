NUM_SIMULATION_STEPS = 100
NUM_TOKENS = 5
NUM_AFFILIATES = 5
INITIAL_SUPPLY = 10000
INITIAL_PRICE = 1.0
INITIAL_COMMISSION_RATE = 0.10
AFFILIATE_STARTING_POINT = 0
INITIAL_BASE_CURRENCY = 1000
INITIAL_TOKEN_INVESTMENT = 10
COMMISSION_DYNAMICS_STEP = 10
DYNAMIC_ADJUSTMENT_RATE = 0.0005  # Reduced adjustment rate
MOVING_AVERAGE_WINDOW = 50  # Increased window for smoother price adjustments
PRICE_IMPACT_FACTOR = 0.01  # Reduced impact factor
BONDING_CURVE_TYPE_CHANGE_INTERVAL = 80 # Increased interval
BONDING_CURVE_PARAM_CHANGE_INTERVAL = 20 # Reduced interval for more frequent parameter tweaks

# Variable bonding curve change intervals for each token
import numpy as np
bonding_curve_change_intervals = np.random.choice(
    range(500, 1001), size=NUM_TOKENS, replace=True
)