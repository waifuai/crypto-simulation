# --- Configuration ---
NUM_AGENTS = 100  # Reduced for faster optimization
SIMULATION_STEPS = 500  # Reduced for faster optimization
INITIAL_TOKEN_SUPPLY = 100.0
INITIAL_AGENT_CAPITAL = 100.0
INITIAL_TOKEN_PRICE = 1.0
TRADING_FEE = 0.001

BONDING_CURVE_TYPE = 'sigmoid'  # Default for initial setup

# Agent Trading Params (keeping these constant for now)
AGENT_TRADE_FREQUENCY = 0.1
AGENT_TRADE_SIZE_RANGE = [0.01, 0.1]
AGENT_MEMORY_SIZE = 10
AGENT_TREND_THRESHOLD = 0.01
AGENT_TREND_DELAY = 2